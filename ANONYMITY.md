# Pre-publish checklist

Double-anonymous review. Deanonymization can get the paper desk-rejected, so
when in doubt, leave it out and restore it in the camera-ready.

## Never in this repo or on the rendered page

- Author names, initials, email addresses
- Institution, lab, department, building
- Funding agency, grant or agreement numbers
- Named repositories or app names attributable to the authors
- Links to personal or lab sites, Scholar, ORCID, LinkedIn, GitHub profiles, X
- An acknowledgements section
- Faces of team members, lab signage, whiteboards, name badges, building
  interiors, screens showing logged-in accounts
- Maps, GPS traces, or any other geographic rendering of where the corpus was
  collected. A coverage map was built and then removed for this reason: a
  per-session track layer names the metros outright and narrows the collectors
  to whoever works near those blocks, which no amount of smoothing undoes

## Before publishing

- [ ] `grep -ri` the whole repo for author surnames, institution, lab name, city
      names, grant number, app name
- [ ] `tools/scrub-media.sh` run on every image and video, and `exiftool` on
      each one returns no GPS, device, or timestamp data
- [ ] Every video watched start to finish for incidental identifying content:
      street signs naming the city, recognizable storefronts, campus buildings,
      license plates, bystander faces, transit branding
- [ ] Face and plate blurring applied to all sidewalk footage and spot-checked
      by hand. Automated blurring misses truncated, occluded, and side-profile
      faces, so do not trust the tool's output
- [ ] Hardware photos shot against a neutral background, none reused from
      inside the lab
- [ ] No analytics, no trackers, no third-party embeds or CDNs
- [ ] `git log --format='%an %ae'` shows only anonymous values
- [ ] Deployed URL contains no identifying string
- [ ] Any linked PDF has its document properties stripped with
      `tools/scrub-pdf.py`, verified with `pdfinfo` (LaTeX embeds author and
      institution fields, and pdfTeX leaves a version banner and build
      timestamps even when those come out empty)
- [ ] Every figure inside a linked PDF read at full zoom for incidental
      identifying content: legible shop or street signage, transit branding,
      and on-screen GPS coordinates in any app screenshot
- [ ] Final pass: open the site in a private window and read it as a hostile
      reviewer actively trying to identify the authors

## Claims discipline

- No numbers that are not final. The corpus is still growing; a dash beats an
  estimate that moves.
- Do not call the dataset "anonymized." Say faces and license plates are
  blurred, and acknowledge residual misses.
- No release date beyond "upon acceptance."
- No results the paper does not support, particularly around learned stop/go
  behavior at crossings.

## Hosting

Do not deploy from a repo under a personal or institutional account: account
name, repo URL, commit history, and commit author email all deanonymize. Use a
purpose-made anonymous account, a random Netlify/Vercel subdomain, or
anonymous.4open.science.

Repo-local git identity is set to anonymous values. Verify before every push:

```sh
git config user.name && git config user.email
git log --format='%an <%ae>'
```

If a commit ever lands carrying real identity, start a fresh repository rather
than rewriting history.
