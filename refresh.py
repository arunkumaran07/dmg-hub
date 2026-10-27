#!/usr/bin/env python3
"""Refresh the DMG Research Hub data block in index.html.

Reads the current page, queries ClinicalTrials.gov (API v2) and PubMed
(E-utilities), rewrites only the block between the DATA START and DATA END
markers, and leaves the rest of the page untouched.

Run locally with:  python3 refresh.py
Dry run (no write): python3 refresh.py --dry-run
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

PAGE = os.environ.get("HUB_PAGE", "index.html")
# NCBI asks API users to identify themselves. Set NCBI_EMAIL in the workflow or
# leave it empty; the script works either way, just with a lower rate limit.
CONTACT_EMAIL = os.environ.get("NCBI_EMAIL", "")
TOOL = "dmg-research-hub"

CT_URL = "https://clinicaltrials.gov/api/v2/studies"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PM_TERM = ("(diffuse midline glioma[Title/Abstract] OR "
           "diffuse intrinsic pontine glioma[Title/Abstract] OR "
           "H3K27M[Title/Abstract])")

FEED_MAX = 60          # papers kept in the feed
PM_WINDOW_DAYS = 10    # how far back to look for new papers each run

CATEGORIES = [
    ("Immunotherapy and cell therapy",
     ["car t", "car-t", "chimeric antigen", "cart", "vaccine", "immunotherap",
      "checkpoint", "nivolumab", "pembrolizumab", "gd2", "b7-h3", "b7h3",
      "t cell", "t-cell", "nk cell", "dendritic"]),
    ("Oncolytic virus",
     ["oncolytic", "adenovir", "herpes", "hsv", "virotherapy", "dnx-2401",
      "reovirus", "poliovirus"]),
    ("Delivery",
     ["focused ultrasound", "convection", "ced", "intrathecal", "intranasal",
      "intra-arterial", "blood-brain barrier", "blood brain barrier",
      "intraventricular", "intracerebroventricular"]),
    ("Radiation",
     ["radiotherapy", "radiation", "re-irradiation", "reirradiation",
      "proton", "photon", "radiosurgery"]),
    ("Platform and multi-arm",
     ["platform", "multi-arm", "multiarm", "umbrella", "basket", "adaptive"]),
]
DEFAULT_CATEGORY = "Targeted and metabolic"

DATA_START = "/* === DATA START"
DATA_END = "/* === DATA END"


def fetch_json(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": TOOL})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as exc:  # noqa: BLE001 - any failure is retried then raised
            if attempt == tries - 1:
                raise
            print(f"  retry {attempt + 1} after {exc}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    return None


# ---------------------------------------------------------------- trials

def categorize(text):
    low = text.lower()
    for name, words in CATEGORIES:
        if any(w in low for w in words):
            return name
    return DEFAULT_CATEGORY


def phase_label(phases):
    if not phases:
        return "Not applicable"
    nice = {"EARLY_PHASE1": "Early phase 1", "PHASE1": "Phase 1",
            "PHASE2": "Phase 2", "PHASE3": "Phase 3", "PHASE4": "Phase 4",
            "NA": "Not applicable"}
    parts = [nice.get(p, p) for p in phases]
    if len(parts) == 2 and parts[0].startswith("Phase") and parts[1].startswith("Phase"):
        return parts[0] + "/" + parts[1].split()[-1]
    return parts[0]


def short_name(study):
    ident = study.get("protocolSection", {}).get("identificationModule", {})
    arms = study.get("protocolSection", {}).get("armsInterventionsModule", {})
    names = [i.get("name", "") for i in arms.get("interventions", []) if i.get("name")]
    names = [n for n in names if len(n) < 60][:2]
    if names:
        return " with ".join(names)
    brief = ident.get("briefTitle", "")
    return brief if len(brief) <= 90 else brief[:87].rstrip() + "..."


def fetch_trials():
    params = {
        "query.cond": "diffuse midline glioma OR diffuse intrinsic pontine glioma",
        "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING",
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
        "pageSize": "100",
        "countTotal": "true",
    }
    out = {}
    token = None
    while True:
        q = dict(params)
        if token:
            q["pageToken"] = token
        data = fetch_json(CT_URL + "?" + urllib.parse.urlencode(q))
        for study in data.get("studies", []):
            ps = study.get("protocolSection", {})
            ident = ps.get("identificationModule", {})
            status = ps.get("statusModule", {}).get("overallStatus", "")
            design = ps.get("designModule", {})
            sponsor = (ps.get("sponsorCollaboratorsModule", {})
                         .get("leadSponsor", {}).get("name", ""))
            nct = ident.get("nctId")
            if not nct:
                continue
            arms = ps.get("armsInterventionsModule", {})
            blob = " ".join([ident.get("briefTitle", ""),
                             ident.get("officialTitle", "")] +
                            [i.get("name", "") for i in arms.get("interventions", [])])
            sites = len(ps.get("contactsLocationsModule", {}).get("locations", []) or [])
            out[nct] = {
                "id": nct,
                "name": short_name(study),
                "phase": phase_label(design.get("phases")),
                "cat": categorize(blob),
                "sponsor": sponsor,
                "status": "Recruiting" if status == "RECRUITING" else "Not yet recruiting",
                "note": (f"{sites} site{'s' if sites != 1 else ''}" if sites else ""),
            }
        token = data.get("nextPageToken")
        if not token:
            break
    return out


def merge_trials(existing, fresh):
    """Keep hand-written names and notes; update status; mark the rest closed."""
    merged = []
    seen = set()
    for row in existing:
        nct = row.get("id")
        seen.add(nct)
        new = fresh.get(nct)
        if new:
            row = dict(row)
            row["status"] = new["status"]
            if not row.get("sponsor"):
                row["sponsor"] = new["sponsor"]
        elif row.get("status") not in ("Closed to accrual",):
            row = dict(row)
            row["status"] = "Closed to accrual"
        merged.append(row)
    added = [v for k, v in fresh.items() if k not in seen]
    merged.extend(added)
    merged.sort(key=lambda r: (r.get("cat", ""), r.get("name", "")))
    return merged, len(added)


# ---------------------------------------------------------------- papers

def eutils_params(extra):
    p = {"tool": TOOL, "retmode": "json"}
    if CONTACT_EMAIL:
        p["email"] = CONTACT_EMAIL
    p.update(extra)
    return urllib.parse.urlencode(p)


def fetch_papers(known):
    url = EUTILS + "/esearch.fcgi?" + eutils_params({
        "db": "pubmed", "term": PM_TERM, "sort": "pub_date",
        "retmax": "30", "datetype": "edat", "reldate": str(PM_WINDOW_DAYS)})
    ids = fetch_json(url).get("esearchresult", {}).get("idlist", [])
    new_ids = [i for i in ids if i not in known]
    if not new_ids:
        return []
    time.sleep(0.5)
    url = EUTILS + "/esummary.fcgi?" + eutils_params(
        {"db": "pubmed", "id": ",".join(new_ids)})
    result = fetch_json(url).get("result", {})
    papers = []
    for pmid in new_ids:
        rec = result.get(pmid)
        if not isinstance(rec, dict):
            continue
        authors = rec.get("authors") or []
        who = ""
        if authors:
            who = authors[0].get("name", "")
            if len(authors) > 1:
                who += " et al."
        doi = ""
        for aid in rec.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
        title = (rec.get("title") or "").strip().rstrip(".")
        title = re.sub(r"<[^>]+>", "", title)
        papers.append({
            "pmid": pmid,
            "title": title,
            "authors": who,
            "journal": rec.get("source", ""),
            "date": (rec.get("sortpubdate") or rec.get("pubdate") or "")[:10].replace("/", "-"),
            "doi": doi,
        })
    return papers


# ---------------------------------------------------------------- page I/O

def read_block(html):
    i = html.index(DATA_START)
    j = html.index(DATA_END, i)
    j = html.index("\n", j) + 1
    block = html[i:j]
    trials = json.loads(re.search(r"const TRIALS = (\[.*?\]);\n", block, re.S).group(1))
    papers = json.loads(re.search(r"const PAPERS = (\[.*?\]);\n", block, re.S).group(1))
    return i, j, trials, papers


def write_block(html, i, j, trials, papers, stamp):
    block = (DATA_START + ": regenerated by the daily refresh; replace only between these markers === */\n"
             + "const TRIALS = " + json.dumps(trials, indent=1) + ";\n"
             + "const PAPERS = " + json.dumps(papers, indent=1) + ";\n"
             + "const STAMP = " + json.dumps(stamp) + ";\n"
             + DATA_END + " === */\n")
    return html[:i] + block + html[j:]


def main():
    dry = "--dry-run" in sys.argv
    html = open(PAGE, encoding="utf-8").read()
    i, j, trials, papers = read_block(html)

    print(f"current: {len(trials)} trials, {len(papers)} papers")
    fresh = fetch_trials()
    print(f"registry: {len(fresh)} open studies")
    trials, added_trials = merge_trials(trials, fresh)

    known = {p["pmid"] for p in papers}
    new_papers = fetch_papers(known)
    papers = sorted(new_papers + papers, key=lambda p: p.get("date", ""), reverse=True)[:FEED_MAX]
    print(f"pubmed: {len(new_papers)} new")

    today = date.today().strftime("%-d %B %Y") if os.name != "nt" else date.today().strftime("%d %B %Y")
    bits = []
    if new_papers:
        bits.append(f"{len(new_papers)} paper{'s' if len(new_papers) != 1 else ''}")
    if added_trials:
        bits.append(f"{added_trials} trial{'s' if added_trials != 1 else ''}")
    stamp = (f"Last automatic refresh: {today}. "
             + (f"Added {' and '.join(bits)}." if bits else "No new entries."))

    out = write_block(html, i, j, trials, papers, stamp)
    if dry:
        print(stamp)
        print("dry run: nothing written")
        return
    if out != html:
        open(PAGE, "w", encoding="utf-8").write(out)
        print("page updated:", stamp)
    else:
        print("no change")


if __name__ == "__main__":
    main()
