import json, datetime
trials = json.load(open('trials.json'))
papers = json.load(open('hub_papers.json'))
grants = [
 ("Disease specific foundations", [
  ("DIPG/DMG Collaborative","https://dipgcollaborative.org/","Joint grant calls funded by a coalition of family foundations; the largest dedicated DIPG and DMG funder."),
  ("The Cure Starts Now research grants","https://thecurestartsnow.org/research/research-and-grants/","Open calls for DIPG, DMG and homerun cancer research, with international chapters."),
  ("ChadTough Defeat DMG Foundation awards","https://chadtough.org/chadtough-defeat-dipg-award/","New investigator and fellowship awards in DIPG and DMG research."),
  ("Michael Mosier Defeat DIPG Foundation","https://defeatdipg.org/current-research/","Project grants to DIPG research programs."),
 ]),
 ("Canadian and general brain tumour funding", [
  ("Brain Tumour Foundation of Canada grants","https://www.braintumour.ca/grants/","Annual brain tumour research grant competition with published guidelines."),
  ("Cancer Research Society brain cancer grants","https://cancerresearchsociety.ca/funding-programs/brain-cancer-research-grants/","Targeted Canadian funding stream for brain cancer research."),
  ("Brain Cancer Canada","https://www.canadahelps.org/en/charities/braincancercanada/","Canadian charity funding brain cancer research; profile and donation page."),
 ]),
]
archives = [
 ("Preprints and unpublished work", [
  ("bioRxiv","https://www.biorxiv.org/","Search \u201cdiffuse midline glioma\u201d for preprints of primary research. Note that bioRxiv does not accept opinion or narrative review pieces."),
  ("medRxiv","https://www.medrxiv.org/","Clinical and trial related preprints, including early reports of DMG studies."),
  ("Research Square","https://www.researchsquare.com/","Preprints posted during journal review, often with reviewer comments attached."),
  ("Zenodo preprints","https://zenodo.org/search?q=diffuse%20midline%20glioma&f=resource_type%3Apublication","Preprints, posters and slides deposited with a DOI and no journal home; the link runs a DMG search limited to publications."),
  ("OSF Preprints","https://osf.io/preprints/","Multi-discipline preprint search across many community servers."),
 ]),
 ("Writing about the field", [
  ("Springer Nature Research Communities","https://communities.springernature.com/","Behind the paper posts and commentary written by authors of recent cancer and neuroscience papers."),
 ]),
]
resources = [
 ("Named DMG datasets", [
  ("CPTAC pediatric brain tumor proteogenomics","https://pdc.cancer.gov/pdc/browse","Proteome and phosphoproteome with matched genome and transcriptome for 218 pediatric brain tumours, 25 of them high grade glioma. Processed data are open through the Proteomic Data Commons."),
  ("OpenPBTA and the CBTN cohort","https://portal.kidsfirstdrc.org/","Harmonized genome and transcriptome for 1,074 pediatric brain tumours including H3 K27M altered DMG, analysable in the cloud through the Kids First portal."),
  ("EGAS00001005773, H3 K27M single cell and epigenomic cohort","https://ega-archive.org/studies/EGAS00001005773","The controlled access study behind Jessa et al., Nature Genetics 2022, on cell lineages in midline glioma. Access through an EGA data access committee."),
  ("CNS tumour methylation reference cohort","https://www.molecularneuropathology.org/mnp/","The reference set behind DNA methylation classification, including the DMG K27 class. The classifier runs online; reference data are requested from the authors."),
  ("DepMap and the pediatric dependency map","https://depmap.org/portal/","CRISPR and RNAi dependency data across cancer cell lines, with a pediatric panel of 82 lines. H3 K27M primary cultures are poorly represented, which is worth knowing before using it for DMG."),
 ]),
 ("Specimens, catalogues and browsers", [
  ("Children's Brain Tumor Network (CBTN)","https://cbtn.org/","Specimens, clinical annotation and harmonized sequencing from member institutions; specimen and data requests go through the CBTN platform."),
  ("PedcBioPortal","https://d3b.center/our-research/pedcbioportal/","Browser for pediatric cancer genomics, including the OpenPBTA and CBTN cohorts, for looking without downloading."),
  ("Childhood Cancer Data Catalog","https://datacatalog.ccdi.cancer.gov/","Index of childhood cancer datasets and the access route for each, wider than brain tumours."),
  ("Human Protein Atlas","https://www.proteinatlas.org/","Tissue, subcellular and single cell type protein localization in normal tissue, used as a reference rather than as tumour data."),
 ]),
 ("Search the archives for DMG data", [
  ("GEO","https://www.ncbi.nlm.nih.gov/gds/?term=diffuse+midline+glioma","Gene expression, single cell and methylation series. Most published DMG transcriptomic data lands here under a GSE accession."),
  ("European Genome-phenome Archive","https://ega-archive.org/studies","Controlled access human sequence data, including several DMG cohorts. Access needs a data access committee application."),
  ("PRIDE","https://www.ebi.ac.uk/pride/archive?keyword=glioma","Raw and processed mass spectrometry. Proteomic and PTM datasets appear here under a PXD accession."),
  ("dbGaP","https://www.ncbi.nlm.nih.gov/gap/?term=glioma","Controlled access genotype and sequence data from US funded studies, under phs accessions."),
  ("Sequence Read Archive","https://www.ncbi.nlm.nih.gov/sra/?term=diffuse+intrinsic+pontine+glioma","Raw sequencing reads where authors have deposited them openly."),
  ("Zenodo","https://zenodo.org/search?q=diffuse%20midline%20glioma","Code, processed matrices, figures and other outputs with a DOI and no journal or archive home; the link runs a DMG search."),
 ]),
]
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
cats = []
for t in trials:
    if t[3] not in cats: cats.append(t[3])
trial_js = json.dumps([{"id":t[0],"name":t[1],"phase":t[2],"cat":t[3],"sponsor":t[4],"status":t[5],"note":t[6]} for t in trials])
today = "26 October 2026"

paper_html = []
for g, rows in papers.items():
    items = []
    for p in rows:
        link = f"https://pubmed.ncbi.nlm.nih.gov/{p['p']}/"
        items.append(f'''<li><a class="paper" href="{link}" target="_blank" rel="noopener"><span class="ptitle">{esc(p['t'])}</span><span class="pmeta">{esc(p['a'])} et al. &middot; <em>{esc(p['j'])}</em> &middot; {p['y']} &middot; PMID {p['p']}</span></a></li>''')
    paper_html.append(f'<section class="pgroup"><h3>{esc(g)}</h3><ul class="plist">{"".join(items)}</ul></section>')

def cardsec(data):
    out = []
    for g, items in data:
        cards = "".join(f'''<li><a href="{u}" target="_blank" rel="noopener"><span class="rname">{esc(n)}</span><span class="rdesc">{esc(d)}</span></a></li>''' for n,u,d in items)
        out.append(f'<section class="rgroup"><h3>{esc(g)}</h3><ul class="rlist">{cards}</ul></section>')
    return "".join(out)
grants_html = cardsec(grants)
archives_html = cardsec(archives)
res_html = []
for g, items in resources:
    cards = "".join(f'''<li><a href="{u}" target="_blank" rel="noopener"><span class="rname">{esc(n)}</span><span class="rdesc">{esc(d)}</span></a></li>''' for n,u,d in items)
    res_html.append(f'<section class="rgroup"><h3>{esc(g)}</h3><ul class="rlist">{cards}</ul></section>')

import json as _json
_trials = _json.load(open('trials.json'))
_papers = _json.load(open('papers_feed.json'))
_tr = [{"id":x[0],"name":x[1],"phase":x[2],"cat":x[3],"sponsor":x[4],"status":x[5],"note":x[6]} for x in _trials]
_tr.sort(key=lambda z:(z["cat"], z["name"]))
DATA_BLOCK = ("<script>\n/* === DATA START: regenerated by the daily refresh; replace only between these markers === */\n"
  + "const TRIALS = " + _json.dumps(_tr, indent=1) + ";\n"
  + "const PAPERS = " + _json.dumps(_papers, indent=1) + ";\n"
  + "const STAMP = " + _json.dumps("Last automatic refresh: 26 October 2026. Seeded by hand; the daily task takes over from the next run.") + ";\n"
  + "/* === DATA END === */\n")

LABS_HTML = r'''<section class="block" id="labs"><div class="wrap">
<h2>Labs</h2>
<p class="note">Groups whose published work sits at the centre of DMG and DIPG research, with the lab or institutional page for each. Descriptions follow what each page states about its own work; this is a reading list of groups, not a ranking, and it is edited by hand rather than generated.</p>
<section class="rgroup"><h3>Canada</h3><ul class="rlist"><li><a href="https://www.sickkids.ca/en/staff/h/cynthia-hawkins" target="_blank" rel="noopener"><span class="rname">Hawkins lab — SickKids, Toronto</span><span class="rdesc">Cynthia Hawkins, neuropathologist and senior scientist at the Labatt Brain Tumour Research Centre; studies what drives paediatric glioma, including DIPG, to inform new therapies.</span></a></li><li><a href="https://jabadolab.com/" target="_blank" rel="noopener"><span class="rname">Jabado lab — RI-MUHC and McGill, Montreal</span><span class="rdesc">Nada Jabado; genetics and epigenetics of paediatric brain tumours, known for identifying histone mutations in human disease.</span></a></li></ul></section>
<section class="rgroup"><h3>United States</h3><ul class="rlist"><li><a href="https://med.stanford.edu/monje-lab" target="_blank" rel="noopener"><span class="rname">Monje lab — Stanford</span><span class="rdesc">Michelle Monje; how the neural environment shapes precursor cell fate, neuron-to-glioma interactions, and GD2 CAR T cell therapy for H3K27M DMG.</span></a></li><li><a href="https://labs.dana-farber.org/filbinlab/" target="_blank" rel="noopener"><span class="rname">Filbin lab — Dana-Farber and Boston Children's</span><span class="rdesc">Mariella Filbin; single-cell genetics and transcriptomics of lethal paediatric high-grade glioma, and therapies that force tumour cells to differentiate.</span></a></li><li><a href="https://www.stjude.org/research/labs/baker-lab-suzanne.html" target="_blank" rel="noopener"><span class="rname">Baker lab — St. Jude</span><span class="rdesc">Suzanne Baker; co-discovered histone H3 mutations in paediatric high-grade glioma, now working on chromatin regulation and developmental signalling in patient-derived and engineered models.</span></a></li><li><a href="https://medschool.umich.edu/profile/40/carl-koschmann" target="_blank" rel="noopener"><span class="rname">Koschmann lab — University of Michigan</span><span class="rdesc">Carl Koschmann, clinical research director of the Chad Carr Pediatric Brain Tumor Center; ATRX biology, ONC201, and early-phase trials with paired tumour and CSF analysis.</span></a></li><li><a href="https://www.seattlechildrens.org/research/centers-programs/childhood-cancer/our-labs/vitanza-lab/" target="_blank" rel="noopener"><span class="rname">Vitanza lab — Seattle Children's</span><span class="rdesc">Nicholas Vitanza, Ben Towne Center; biopsy and autopsy-derived DMG models, epigenetic vulnerabilities, and CAR T cells delivered directly into the brain.</span></a></li><li><a href="https://profiles.mountsinai.org/oren-becher" target="_blank" rel="noopener"><span class="rname">Becher lab — Mount Sinai, New York</span><span class="rdesc">Oren Becher; built the first genetically engineered mouse models of DIPG and co-discovered ACVR1/ALK2 mutations, now pursued as a target.</span></a></li><li><a href="https://braintumorcenter.ucsf.edu/people/sabine-mueller" target="_blank" rel="noopener"><span class="rname">Mueller group — UCSF Pediatric Brain Tumor Center</span><span class="rdesc">Sabine Mueller, co-founder of PNOC and medical lead of the Zurich DMG centre; international DMG trials and long-term neurocognitive outcomes.</span></a></li></ul></section>
<section class="rgroup"><h3>Europe and international</h3><ul class="rlist"><li><a href="https://www.icr.ac.uk/research-and-discoveries/icr-divisions/cancer-biology/glioma-team" target="_blank" rel="noopener"><span class="rname">Glioma Group — Institute of Cancer Research, London</span><span class="rdesc">Chris Jones; genomic and epigenomic profiling of childhood glioma, preclinical drug screening against ACVR1, H3.3 G34R/V and ATRX, and intratumoural heterogeneity.</span></a></li><li><a href="https://www.dkfz.de/en/pediatric-neurooncology" target="_blank" rel="noopener"><span class="rname">Pediatric Neurooncology — DKFZ, Heidelberg</span><span class="rdesc">Stefan Pfister; sequencing and biomarker discovery in childhood brain tumours, preclinical testing, and CSF and plasma markers for diagnosis and monitoring.</span></a></li><li><a href="https://www.kispi.uzh.ch/forschungszentrum/person/nazarian-javad" target="_blank" rel="noopener"><span class="rname">DMG/DIPG Center Zurich, translational program</span><span class="rdesc">Javad Nazarian; tumour biobank, molecular profiling and in vivo and in vitro models behind molecularly targeted therapy for DIPG and paediatric high-grade glioma. Page in German.</span></a></li><li><a href="https://www.newcastle.edu.au/profile/matt-dun" target="_blank" rel="noopener"><span class="rname">Dun lab — University of Newcastle and HMRI, Australia</span><span class="rdesc">Matt Dun; proteogenomics and phosphoproteomics of the signalling pathways driving DMG and DIPG, with findings taken into clinical trials.</span></a></li></ul></section>
</div></section>

'''

SCRIPT = DATA_BLOCK + r'''const $ = id => document.getElementById(id);
let active = "All";

function renderTrials() {
  const term = $('q').value.trim().toLowerCase();
  const rows = TRIALS
    .filter(t => active === 'All' || t.cat === active)
    .filter(t => !term || ((t.name || '') + ' ' + (t.sponsor || '') + ' ' + (t.id || '') + ' ' + (t.note || '')).toLowerCase().includes(term));
  $('rows').innerHTML = rows.length ? rows.map(t => `
    <tr>
      <td class="name">${esc(t.name)}<small>${esc(t.note || '')}</small></td>
      <td>${esc(t.phase || '')}</td>
      <td>${esc(t.cat || '')}</td>
      <td>${esc(t.sponsor || '')}</td>
      <td><span class="status ${/not yet/i.test(t.status || '') ? 'nyr' : 'rec'}">${esc(t.status || '')}</span></td>
      <td><a class="nct" href="https://clinicaltrials.gov/study/${encodeURIComponent(t.id)}" target="_blank" rel="noopener">${esc(t.id)}</a></td>
    </tr>`).join('') : '<tr><td colspan="6" class="empty">No studies match that filter.</td></tr>';
  $('count').textContent = rows.length + ' of ' + TRIALS.length + ' studies shown';
}
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function buildFilters() {
  const cats = [];
  TRIALS.forEach(t => { if (t.cat && !cats.includes(t.cat)) cats.push(t.cat); });
  cats.sort();
  const f = $('filters'); f.innerHTML = '';
  ['All'].concat(cats).forEach(c => {
    const b = document.createElement('button');
    b.className = 'chip'; b.type = 'button'; b.textContent = c;
    b.setAttribute('aria-pressed', c === active ? 'true' : 'false');
    b.addEventListener('click', () => { active = c; [...f.children].forEach(x => x.setAttribute('aria-pressed', x.textContent === c ? 'true' : 'false')); renderTrials(); });
    f.appendChild(b);
  });
}
$('q').addEventListener('input', renderTrials);

function visibleTrials() {
  const term = $('q').value.trim().toLowerCase();
  return TRIALS
    .filter(t => active === 'All' || t.cat === active)
    .filter(t => !term || ((t.name || '') + ' ' + (t.sponsor || '') + ' ' + (t.id || '') + ' ' + (t.note || '')).toLowerCase().includes(term));
}
const csvBtn = $('csv');
if (csvBtn) csvBtn.addEventListener('click', () => {
  const cols = ['id', 'name', 'phase', 'cat', 'sponsor', 'status', 'note'];
  const head = ['NCT number', 'Study', 'Phase', 'Approach', 'Sponsor', 'Status', 'Note', 'Record'];
  const cell = v => '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"';
  const rows = visibleTrials().map(t => cols.map(c => cell(t[c])).concat(cell('https://clinicaltrials.gov/study/' + t.id)).join(','));
  const csv = '\ufeff' + [head.map(cell).join(',')].concat(rows).join('\r\n');
  const stamp = new Date().toISOString().slice(0, 10);
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'dmg-trials-' + stamp + '.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);
});


function renderFeed(papers) {
  if (!papers.length) { $('feed').innerHTML = '<li class="empty">No new papers recorded yet. The next daily refresh will fill this in.</li>'; return; }
  $('feed').innerHTML = papers.map(p => `<li><a class="paper" href="https://pubmed.ncbi.nlm.nih.gov/${encodeURIComponent(p.pmid)}/" target="_blank" rel="noopener">
    <span class="ptitle">${esc(p.title)}</span>
    <span class="pmeta">${esc(p.authors || '')} &middot; <em>${esc(p.journal || '')}</em> &middot; ${esc(p.date || '')} &middot; PMID ${esc(p.pmid)}</span></a></li>`).join('');
}

buildFilters();
renderTrials();
renderFeed(PAPERS);
$('stamp').textContent = STAMP;

/* Collapsible sections. Each viewer's open and closed sections are remembered in
   their own browser where that is allowed, and the page works the same if it is not. */
const SECT_KEY = 'dmghub.sections';
const sects = () => [...document.querySelectorAll('details.sect')];
function saveSects() {
  try {
    const o = {};
    sects().forEach(d => { o[d.dataset.sect] = d.open; });
    localStorage.setItem(SECT_KEY, JSON.stringify(o));
  } catch (e) { /* private window or blocked storage: nothing to remember */ }
}
try {
  const saved = JSON.parse(localStorage.getItem(SECT_KEY) || 'null');
  if (saved) sects().forEach(d => { if (d.dataset.sect in saved) d.open = !!saved[d.dataset.sect]; });
} catch (e) { /* ignore unreadable storage */ }
sects().forEach(d => d.addEventListener('toggle', saveSects));
function openFromHash() {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id) return;
  const s = document.getElementById(id);
  if (!s) return;
  const d = s.querySelector('details.sect');
  if (d && !d.open) { d.open = true; saveSects(); }
  requestAnimationFrame(() => s.scrollIntoView());
}
window.addEventListener('hashchange', openFromHash);
openFromHash();
$('expand').addEventListener('click', () => { sects().forEach(d => { d.open = true; }); saveSects(); });
$('collapse').addEventListener('click', () => { sects().forEach(d => { d.open = false; }); saveSects(); });

const hintTrials = $('hint-trials');
if (hintTrials) hintTrials.textContent = TRIALS.length + ' studies';
const hintLatest = $('hint-latest');
if (hintLatest) hintLatest.textContent = PAPERS.length + ' recent papers';
</script>
'''


html = f'''<title>DMG Research Hub</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: single column reading width, with a sticky section nav and dense data rows for trials. */
:root {{
  --bg:#FFFFFF; --surface:#FCFCFB; --fg:#16181D; --muted:#5A6170; --line:#E2E1DC;
  --accent:#2F4C6B; --accent-soft:#E8EDF2; --ok:#2E6B4F; --warn:#8A5B14;
  --font-display:"Newsreader", Georgia, "Times New Roman", serif;
  --font-body:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono:"IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg:#13151A; --surface:#1B1E25; --fg:#ECEDF0; --muted:#9BA3B2; --line:#2B2F39;
    --accent:#8FB4D8; --accent-soft:#222B36; --ok:#6FC79B; --warn:#D8A85A; color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --bg:#13151A; --surface:#1B1E25; --fg:#ECEDF0; --muted:#9BA3B2; --line:#2B2F39;
  --accent:#8FB4D8; --accent-soft:#222B36; --ok:#6FC79B; --warn:#D8A85A; color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--font-body); line-height:1.55; }}
body::before {{ content:""; position:fixed; inset:0 0 auto; height: env(safe-area-inset-top, 0px); z-index:10; background: var(--bg); }}
.wrap {{ width: 100%; margin: 0 auto; padding-left: max(28px, env(safe-area-inset-left, 0px)); padding-right: max(28px, env(safe-area-inset-right, 0px)); }}
header.brandbar {{ padding-block: 22px 14px; }}
header.brandbar .wrap {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 18px; }}
.tagline {{ color: var(--muted); font-size:0.95rem; margin:0; max-width:70ch; }}
h1 {{ font-family: var(--font-display); font-weight:600; font-size: clamp(1.5rem, 2.6vw, 2rem); line-height:1.15; margin:0; letter-spacing:-0.01em; white-space:nowrap; }}
.lede {{ font-family: var(--font-display); font-size: clamp(1.05rem,2.4vw,1.25rem); color: var(--fg); max-width: 62ch; margin:0 0 16px; }}
nav.sections {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index:9; background: var(--bg); border-bottom:1px solid var(--line); }}
nav.sections .wrap {{ display:flex; gap:26px; overflow-x:auto; padding-block:14px; }}
nav.sections a {{ color: var(--fg); text-decoration:none; font-weight:700; font-size:0.98rem; letter-spacing:0.04em; text-transform:uppercase; white-space:nowrap; }}
nav.sections a:hover, nav.sections a:focus-visible {{ color: var(--accent); }}
section.block {{ padding-block: 44px; border-bottom:1px solid var(--line); }}
details.sect {{ border:0; }}
section.block:has(details.sect:not([open])) {{ padding-block: 20px; }}
details.sect > summary {{ display:flex; align-items:baseline; gap:10px; cursor:pointer; list-style:none; padding:2px 0 4px; }}
details.sect > summary::-webkit-details-marker {{ display:none; }}
details.sect > summary::before {{ content:"▸"; color: var(--muted); font-size:0.95rem; line-height:1.5; }}
details.sect[open] > summary::before {{ content:"▾"; }}
details.sect > summary:hover h2, details.sect > summary:focus-visible h2 {{ color: var(--accent); }}
details.sect > summary h2 {{ margin:0; }}
.shint {{ color: var(--muted); font-size:0.85rem; white-space:nowrap; font-variant-numeric: tabular-nums; }}
.sbody {{ padding-top:12px; }}
.sectbar {{ border-bottom:1px solid var(--line); }}
.sectbar .wrap {{ display:flex; gap:8px; padding-block:10px; }}
h2 {{ font-family: var(--font-display); font-weight:600; font-size: clamp(1.5rem,3.5vw,2rem); margin:0 0 6px; letter-spacing:-0.01em; }}
h3 {{ font-size:0.86rem; letter-spacing:0.08em; text-transform:uppercase; color: var(--fg); margin:28px 0 12px; font-weight:700; }}
p.note {{ color: var(--muted); max-width:70ch; margin:0 0 20px; font-size:0.95rem; }}
.controls {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:18px; }}
button.chip {{ font:inherit; font-size:0.84rem; padding:6px 12px; border-radius:999px; border:1px solid var(--line); background: var(--surface); color: var(--muted); cursor:pointer; }}
button.chip[aria-pressed="true"] {{ background: var(--accent-soft); border-color: var(--accent); color: var(--accent); font-weight:600; }}
input[type="search"] {{ font:inherit; font-size:0.9rem; padding:7px 12px; border-radius:8px; border:1px solid var(--line); background: var(--surface); color: var(--fg); min-width:min(260px, 100%); flex:1; }}
.tablewrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:12px; background: var(--surface); }}
table {{ border-collapse: collapse; width:100%; font-size:0.9rem; }}
th, td {{ text-align:left; padding:11px 14px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ font-size:0.76rem; letter-spacing:0.07em; text-transform:uppercase; color: var(--fg); font-weight:700; white-space:nowrap; }}
tbody tr:last-child td {{ border-bottom:0; }}
td.name {{ min-width:230px; }}
td.name small {{ display:block; color: var(--muted); font-size:0.82rem; margin-top:3px; }}
a.nct {{ font-family: var(--font-mono); font-size:0.82rem; color: var(--accent); text-decoration:none; white-space:nowrap; }}
a.nct:hover {{ text-decoration: underline; }}
.status {{ font-size:0.78rem; font-weight:600; white-space:nowrap; }}
.status.rec {{ color: var(--ok); }}
.status.nyr {{ color: var(--warn); }}
.count {{ color: var(--muted); font-size:0.85rem; }}
.empty {{ color: var(--muted); font-size:0.9rem; padding:16px 14px; display:block; }}
td.empty {{ display:table-cell; }}
.rlist, .plist {{ list-style:none; margin:0; padding:0; display:grid; gap:10px; }}
.rlist {{ grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }}
.plist {{ grid-template-columns: repeat(auto-fit, minmax(430px, 1fr)); column-gap:36px; }}
.plist li {{ min-width:0; }}
.rlist a {{ display:block; min-width:0; padding:14px 16px; border:1px solid var(--line); border-radius:12px; background: var(--surface); text-decoration:none; color:inherit; height:100%; }}
.rlist a:hover {{ border-color: var(--accent); }}
.rname {{ display:block; font-weight:600; color: var(--accent); margin-bottom:4px; }}
.rdesc {{ display:block; color: var(--muted); font-size:0.88rem; }}
.plist a {{ display:block; min-width:0; text-decoration:none; color:inherit; padding:9px 0; border-bottom:1px dotted var(--line); }}
.plist li:last-child a {{ border-bottom:0; }}
.ptitle {{ display:block; color: var(--accent); font-weight:600; }}
.plist a:hover .ptitle {{ text-decoration: underline; }}
.pmeta {{ display:block; color: var(--muted); font-size:0.84rem; font-variant-numeric: tabular-nums; margin-top:2px; }}
footer {{ padding-block: 32px 56px; color: var(--muted); font-size:0.86rem; }}
footer p {{ max-width:72ch; }}
a {{ color: var(--accent); }}
:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; border-radius:4px; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; transition:none !important; }} }}
</style>

<header class="brandbar"><div class="wrap">
<h1>DMG Research Hub</h1>
<p class="tagline">Open trials, data resources and primary literature for H3 K27M altered diffuse midline glioma.</p>
</div></header>

<nav class="sections"><div class="wrap">
<a href="#intro">What is DMG</a><a href="#resources">Data and datasets</a><a href="#latest">New papers</a><a href="#grants">Grants and foundations</a><a href="#trials">Open trials</a><a href="#labs">Labs</a><a href="#archives">Preprints and blogs</a><a href="#literature">Literature</a><a href="#about">About</a>
</div></nav>

<div class="sectbar"><div class="wrap">
<button class="chip" type="button" id="expand">Expand all</button><button class="chip" type="button" id="collapse">Collapse all</button>
</div></div>

<section class="block" id="intro"><div class="wrap">
<h2>What is diffuse midline glioma</h2>
<p class="note">This is not medical advice, and decisions about a particular child belong with that child's own care team.</p>

<section class="rgroup"><h3>The disease</h3>
<p class="note">Diffuse midline glioma, often shortened to DMG, is a tumour that grows in the middle structures of the brain and spinal cord: most often the pons, which is part of the brainstem, and also the thalamus and the spinal cord. When it arises in the pons it is also called diffuse intrinsic pontine glioma, or DIPG. The word diffuse matters. The tumour cells spread between normal brain cells rather than forming a lump with a clean edge, which is why surgery to remove it is not possible in the way it often is for other tumours.</p>
<p class="note">Most of these tumours carry a single change in a protein that packages DNA, a histone. The change is called H3 K27M, and the current classification names the disease after it: diffuse midline glioma, H3 K27-altered. That one change alters how thousands of genes are switched on and off, which is why the disease behaves so differently from adult brain tumours.</p></section>

<section class="rgroup"><h3>Who it affects, and what the numbers say</h3>
<p class="note">DMG is mainly a disease of children, although it also occurs in teenagers and adults. In the most complete population based analysis, covering every brainstem high grade glioma recorded in the United States between 2000 and 2017, incidence was highest in children aged one to nine years and lower in older children (<a href="https://pubmed.ncbi.nlm.nih.gov/33346835/" target="_blank" rel="noopener">Patil et al., 2021</a>). It is a rare disease, and because many of these tumours are diagnosed on imaging rather than biopsy, published counts vary with how cases are defined; the registry figures above are the ones to work from rather than a single global number. In the largest registry series, covering 1,008 children with diffuse intrinsic pontine glioma, median survival was 11 months from diagnosis and about one in ten children were alive at two years (<a href="https://pubmed.ncbi.nlm.nih.gov/29746225/" target="_blank" rel="noopener">Hoffman et al., 2018</a>). Those numbers describe a group, not an individual, and they predate the treatments now in trials.</p></section>

<section class="rgroup"><h3>How it is diagnosed and treated today</h3>
<p class="note">Diagnosis usually begins with an MRI, which in a typical pontine tumour is characteristic enough that the picture alone can make the diagnosis. Many centres now also take a small biopsy, which carries risk but allows the tumour's molecular type to be established and makes trial entry possible. Radiotherapy is the one treatment with a reliable effect on survival, usually given over about six weeks, and it often brings a period of improvement in symptoms. Chemotherapy as used in other childhood cancers has not been shown to help.</p>
<p class="note">In August 2025 the US Food and Drug Administration granted accelerated approval to dordaviprone, also known as ONC201, for diffuse midline glioma with an H3 K27M mutation and progressive disease after prior therapy, in adults and children aged one year and older (<a href="https://www.fda.gov/drugs/resources-information-approved-drugs/fda-grants-accelerated-approval-dordaviprone-diffuse-midline-glioma" target="_blank" rel="noopener">FDA announcement</a>). Accelerated approval means the drug was approved on tumour response rather than on proven survival benefit, and a confirmatory trial is under way (<a href="https://pubmed.ncbi.nlm.nih.gov/38335473/" target="_blank" rel="noopener">Arrillaga-Romany et al., 2024</a>). Early trials of CAR T cells, immune cells engineered to recognise the tumour, have produced measurable tumour shrinkage in some patients, with serious side effects that required intensive care (<a href="https://pubmed.ncbi.nlm.nih.gov/39537919/" target="_blank" rel="noopener">Monje et al.</a>, <a href="https://pubmed.ncbi.nlm.nih.gov/39775044/" target="_blank" rel="noopener">Vitanza et al.</a>). These are early phase studies, which means they are testing safety and signal, not proving benefit.</p></section>

<section class="rgroup"><h3>Why it is hard, and what is changing</h3>
<p class="note">Three things make DMG difficult. Its location rules out surgical removal. The blood brain barrier keeps many drugs out of the brain, which is why trials now test delivery directly into the tumour or through focused ultrasound that opens the barrier temporarily. And the tumour is driven by a change in how genes are regulated rather than by a single faulty protein that a drug can switch off.</p>
<p class="note">What has changed in the last few years is measurement. Tumour DNA can now be detected in cerebrospinal fluid, so response can be tracked without repeated surgery (<a href="https://pubmed.ncbi.nlm.nih.gov/42294888/" target="_blank" rel="noopener">Nobre et al., 2026</a>). Tumours can be described at the level of proteins and their modifications, not only genes. And the research community has agreed a shared road map for how trials and data sharing should work (<a href="https://pubmed.ncbi.nlm.nih.gov/38039965/" target="_blank" rel="noopener">Koschmann et al.</a>).</p></section>

<section class="rgroup"><h3>Where to find help</h3>
<p class="note">For families, the most useful first contacts are the treating centre's neuro-oncology team and the family support services run by the disease foundations, which can explain options and trials in person. <a href="https://chadtough.org/my-dipg-navigator/about-us/chadtough-defeat-dipg-foundation/" target="_blank" rel="noopener">My DIPG Navigator</a> at the ChadTough Defeat DMG Foundation offers one to one support, and <a href="https://dipg.org/research/overview/" target="_blank" rel="noopener">dipg.org</a> keeps plain language summaries of current research. The trial table on this page lists studies that are open, but eligibility is decided by the trial team and a referral normally comes through the treating oncologist.</p></section>
</div></section>

<section class="block" id="resources"><div class="wrap">
<h2>Data and datasets</h2>
<p class="note">Where DMG tissue and molecular data actually live, how to reach each one, and where to search for the rest. Access terms differ: some are open, some controlled, and some need a data access committee or a project application. Accession numbers are listed only where they have been verified, since a paper's own data availability statement is the authoritative source and the archive searches are the reliable route to everything else.</p>
<p class="note">Research funders and family foundations are listed under Grants and foundations.</p>
{''.join(res_html)}
<p class="note" style="margin-top:18px">If you publish a DMG dataset and would like its accession listed here, send it and it will be added with a line on what it contains and how access works.</p>
</div></section>

<section class="block" id="latest"><div class="wrap">
<h2>New papers</h2>
<p class="note">Everything indexed on PubMed in the last weeks matching diffuse midline glioma, diffuse intrinsic pontine glioma or H3K27M, newest first, added automatically each day. This is a raw feed: case reports and reviews sit beside primary research, and nothing here has been filtered for quality.</p>
<ul class="plist" id="feed"><li class="empty">Loading the feed.</li></ul>
<p class="note" id="stamp" style="margin-top:14px"></p>
</div></section>

<section class="block" id="grants"><div class="wrap">
<h2>Grants and foundations</h2>
<p class="note">Where DMG specific research money comes from, and the Canadian brain tumour funders that also support this work. Deadlines move each year, so check each call directly.</p>
{grants_html}
</div></section>

<section class="block" id="trials"><div class="wrap">
<h2>Open trials</h2>
<p class="note">Interventional studies open or opening to accrual that list diffuse midline glioma or diffuse intrinsic pontine glioma among their conditions. Each row links to its ClinicalTrials.gov record, which is the authoritative source for eligibility and sites.</p>
<div class="controls" id="filters"></div>
<div class="controls"><input type="search" id="q" placeholder="Search by agent, sponsor or NCT number" aria-label="Search trials"><button class="chip" type="button" id="csv">Download CSV</button><span class="count" id="count"></span></div>
<div class="tablewrap"><table>
<thead><tr><th>Study</th><th>Phase</th><th>Approach</th><th>Sponsor</th><th>Status</th><th>Record</th></tr></thead>
<tbody id="rows"><tr><td colspan="6" class="empty">Loading the trial table.</td></tr></tbody>
</table></div>
<p class="note" style="margin-top:14px">The table is rebuilt each morning from <a href="https://clinicaltrials.gov/search?cond=Diffuse%20Midline%20Glioma&aggFilters=status:rec%20not" target="_blank" rel="noopener">ClinicalTrials.gov</a>, which is the authoritative record for eligibility, sites and status.</p>
</div></section>

{LABS_HTML}<section class="block" id="archives"><div class="wrap">
<h2>Preprints and blogs</h2>
<p class="note">Work that has not been through a journal yet, and the places where people write about the field between papers. Preprints are not peer reviewed; read them as claims rather than conclusions.</p>
{archives_html}
</div></section>

<section class="block" id="literature"><div class="wrap">
<h2>Literature</h2>
<p class="note">A working bibliography of {sum(len(v) for v in papers.values())} papers, each verified against its PubMed record. Grouped by what the paper is for rather than by date.</p>
{''.join(paper_html)}
</div></section>

<section class="block" id="about"><div class="wrap">
<h2>About this page</h2>
<p class="note">Compiled by Arun Kumaran Anguraj Vadivel, Molecular Medicine, The Hospital for Sick Children, Toronto. Open trials and newly published papers refresh automatically each day from ClinicalTrials.gov and PubMed; the curated sections are reviewed by hand. It is a research reference, not medical advice, and treatment decisions belong with a patient's own care team.</p>
<p class="note">This is a personal research reference maintained alongside work on DMG proteomics and functional omics at SickKids. It is not affiliated with any consortium, registry or sponsor, and inclusion here is not an endorsement of a trial or a product. Trial status changes constantly, so treat the ClinicalTrials.gov record as current and this table as a snapshot.</p>
<p class="note">Corrections, additions and links worth including are welcome: <span style="font-family:var(--font-mono)">arun.angurajvadivel@sickkids.ca</span></p>
</div></section>

<footer><div class="wrap">
<p>Trial data from ClinicalTrials.gov and literature metadata from PubMed, both refreshed each day. Families looking for support and current treatment options should start with their treating centre and with the foundations listed above.</p>
</div></footer>

{SCRIPT}'''
import sys as _sys, os as _os, re as _re

_OPEN = {'intro'}
_HINT = {'literature': 'papers', 'labs': 'labs'}
def _collapse(h):
    def fix(m):
        sid, inner = m.group(1), m.group(2)
        hm = _re.search(r'<h2>(.*?)</h2>', inner, _re.S)
        if not hm: return m.group(0)
        title, body = hm.group(1), inner[hm.end():]
        if sid in ('trials', 'latest'):
            hint = f'<span class="shint" id="hint-{sid}"></span>'
        else:
            n = body.count('<li>')
            word = _HINT.get(sid, 'links')
            hint = f'<span class="shint">{n} {word}</span>' if n else ''
        op = ' open' if sid in _OPEN else ''
        return (f'<section class="block" id="{sid}"><div class="wrap">\n'
                f'<details class="sect" data-sect="{sid}"{op}><summary><h2>{title}</h2>{hint}</summary>\n'
                f'<div class="sbody">{body}</div></details>\n</div></section>')
    return _re.sub(r'<section class="block" id="([^"]+)"><div class="wrap">(.*?)</div></section>', fix, h, flags=_re.S)
html = _collapse(html)

if '--standalone' in _sys.argv:
    _m = _re.search(r'<title>(.*?)</title>', html)
    _title = _m.group(1) if _m else 'DMG Research Hub'
    _body = html.replace(_m.group(0), '', 1) if _m else html
    _reset = (":root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}"
              "body{margin:0;font:14px system-ui,-apple-system,'Segoe UI',sans-serif}img{max-width:100%}[hidden]{display:none!important}")
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           '<title>' + _title + '</title>\n'
           '<meta name="description" content="Open trials, new papers, data resources, funders and literature for H3 K27M altered diffuse midline glioma.">\n'
           '<style>' + _reset + '</style>\n'
           '</head>\n<body>\n' + _body + '\n</body>\n</html>\n')
    _os.makedirs('site', exist_ok=True)
    open('site/index.html','w').write(doc)
    print('site/index.html', len(doc))
else:
    # the artifact viewer does not grant pages download permission, so the CSV button
    # would be dead there; it stays in the GitHub Pages build only.
    open('index.html','w').write(html.replace('<button class="chip" type="button" id="csv">Download CSV</button>', ''))
print(len(html))
