# UNI project page

Project page for a paper under double-anonymous review at ICRA 2027.

Built on the [Nerfies](https://github.com/nerfies/nerfies.github.io) template
(CC BY-SA 4.0), with the template's analytics, author links, and third-party
CDN requests removed. Every CSS, JS, font, and media file is served from this
repo, so loading the page makes no third-party request.

## Preview locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Before adding any image or video

All media must go through `tools/scrub-media.sh`, which strips EXIF (iPhone
media embeds GPS coordinates, device model, and timestamps) and container
metadata. See `ANONYMITY.md` for the full pre-publish checklist.

```sh
tools/scrub-media.sh path/to/asset.jpg path/to/asset.mp4
```

## Placeholder assets

The files under `static/videos/` and `static/images/` are generated grey
placeholders labelled `PLACEHOLDER`, present only so the layout can be
reviewed. Every one must be replaced before publishing:

| File | Purpose |
| --- | --- |
| `static/videos/teaser.mp4` | Hero teaser |
| `static/videos/method.mp4` | Method video |
| `static/videos/session_01..03.mp4` | Sample sessions (3&ndash;5 total) |
| `static/videos/deploy_wheelchair.mp4` | Deployment, wheelchair base |
| `static/videos/deploy_quadruped.mp4` | Deployment, quadruped |
| `static/images/feasibility_filter.png` | Feasibility-filter figure |
| `static/images/hardware.jpg` | Hardware photo |

`index.html` marks every unfinished item with a `TODO` comment, including the
dataset statistics table and the hardware component and cost table.
