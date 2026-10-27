# DMG Research Hub

A single-page reference for H3 K27M altered diffuse midline glioma: open clinical
trials, newly published papers, data and tissue resources, funders, preprint
servers, and a verified bibliography. One HTML file, no build step, no framework.

The trial table and the paper feed refresh themselves every morning through a
GitHub Action; everything else is curated by hand.

Maintained by Arun Kumar Anguraj Vadivel, Molecular Medicine, SPARC Innovation
Hub, The Hospital for Sick Children, Toronto. It is a research reference, not
medical advice.

## Putting it online (about ten minutes, free)

1. Create a new **public** repository on GitHub, for example `dmg-hub`.
2. Upload these files to it (or `git push` them): `index.html`, `refresh.py`,
   `.nojekyll`, `README.md` and the `.github/workflows/refresh.yml` workflow.
3. In the repository, open **Settings → Pages**, set *Source* to
   **Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
4. A minute later the site is live at `https://<your-github-name>.github.io/dmg-hub/`.
5. Optional: open **Actions**, select *Daily refresh*, and press **Run workflow**
   once to confirm the refresh works before leaving it to the schedule.

### Your own domain (optional, about $15 a year)

Buy a domain at any registrar, add a `CNAME` file to the repository containing
just the domain name, and point the domain's DNS at GitHub Pages following
GitHub's own instructions for custom domains. Nothing else changes.

## How the refresh works

`refresh.py` edits one block of `index.html`, the part between the
`DATA START` and `DATA END` markers, and nothing else. It:

- queries the ClinicalTrials.gov API v2 for interventional studies in diffuse
  midline glioma or diffuse intrinsic pontine glioma that are recruiting or not
  yet recruiting;
- keeps any study name and note you have edited by hand, updates the status,
  and marks a study that has left recruitment as *Closed to accrual* instead of
  deleting it;
- queries PubMed for records added in the last ten days matching diffuse midline
  glioma, diffuse intrinsic pontine glioma or H3K27M, and prepends the new ones
  to the feed, keeping the 60 most recent;
- rewrites the stamp line under the feed with the date and what changed.

The workflow commits the file only when something actually changed, so the
repository history doubles as a log of what appeared and when.

Run it yourself at any time:

```bash
python3 refresh.py --dry-run   # show what would change
python3 refresh.py             # write the change
```

Optional: set a repository secret named `NCBI_EMAIL` to your email address.
NCBI asks API users to identify themselves and grants a higher rate limit in
return. The script works without it.

## Editing the page

Trial names, categories and notes are deliberately editable. Open `index.html`,
find the `TRIALS` array in the data block, and rewrite any `name`, `cat` or
`note` field; the refresh will respect your wording from then on. Categories in
use: Immunotherapy and cell therapy, Targeted and metabolic, Delivery,
Radiation, Oncolytic virus, Platform and multi-arm.

Everything outside the data block, including the resource cards, the funders and
the bibliography, is plain HTML near the bottom of the file and can be edited
directly.

## Checking the links

The portal links for PRIDE, EGA, DepMap, the Proteomic Data Commons, the Human
Protein Atlas and the Heidelberg methylation classifier were written from their
canonical addresses and have not been verified by fetching them. Worth clicking
through once before the page is shared widely.
