# UNI project page

Project page for a paper under double-anonymous review at ICRA 2027.

Built on the [Nerfies](https://github.com/nerfies/nerfies.github.io) template
(CC BY-SA 4.0), with the template's analytics, author links, and third-party
CDN requests removed. Every CSS, JS, font, and media file is served from this
repo, so loading the page makes no third-party request at all &mdash; the
interactive coverage map was the one exception, since it fetched basemap tiles
from `tile.openstreetmap.org`, and it has been removed (see `ANONYMITY.md`).

## Preview locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Before adding any image, video, or PDF

All media must go through `tools/scrub-media.sh`, which strips EXIF (iPhone
media embeds GPS coordinates, device model, and timestamps) and container
metadata. See `ANONYMITY.md` for the full pre-publish checklist.

```sh
tools/scrub-media.sh path/to/asset.jpg path/to/asset.mp4
```

PDFs go through `tools/scrub-pdf.py` instead, which blanks the Info dictionary
in place. LaTeX rewrites that dictionary on every build, so re-run it on
`static/paper/universal-navigation-interface.pdf` after each re-upload — even
when `/Author` comes out empty, pdfTeX still leaves its own version banner and
the build timestamps.

```sh
tools/scrub-pdf.py static/paper/universal-navigation-interface.pdf
pdfinfo static/paper/universal-navigation-interface.pdf   # verify
```

Unlike ghostscript or qpdf, this edits bytes in place without re-encoding, so
the figures and link annotations are untouched. It refuses to write if the file
length would change.

## Placeholder assets

`static/videos/teaser.mp4` is real footage. The remaining files under
`static/videos/` and `static/images/` are generated grey placeholders labelled
`PLACEHOLDER`, present only so the layout can be reviewed. Each must be
replaced before publishing:

| File | Purpose |
| --- | --- |
| `static/videos/method.mp4` | Method video |
| `static/videos/session_01..03.mp4` | Sample sessions (3&ndash;5 total) |
| `static/videos/deploy_wheelchair.mp4` | Deployment, powered wheelchair |
| `static/images/feasibility_filter.png` | Feasibility-filter figure (paper Fig. 1, left) |
| `static/images/hardware.jpg` | Hardware photo |

`static/videos/deploy_quadruped.mp4` is no longer referenced by `index.html`:
the paper lists quadruped transfer as future work, so there is no result to
show. The file is kept in case that changes.

`index.html` marks every unfinished item with a `TODO` comment. Prose, dataset
statistics, and all result tables are taken from the submitted paper, which is
served from `static/paper/`; the outstanding TODOs are media replacements.
