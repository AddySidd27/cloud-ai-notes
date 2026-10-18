# AdnanSiddiqui.com source

Source for [adnanasiddiqui.com](https://adnanasiddiqui.com), a technical publication on Azure Virtual Desktop, Windows 365, Azure landing zones and cloud infrastructure. Built with [Eleventy](https://www.11ty.dev/).

This is an independent personal project. It is not affiliated with or endorsed by Microsoft.

## Build locally

Requires Node.js 22 or later.

```
npm ci
npm run build     # writes the site to _site
npm start         # local server with live reload
```

## Layout

- `src/posts/` article Markdown (front matter sets title, series, order and permalink)
- `src/diagrams/` redrawn SVG diagrams (not official Microsoft diagrams)
- `src/img/` screenshots; only images referenced by a post are copied to the build
- `tools/check-output.py` read-only check of a built site (`python3 tools/check-output.py _site`)
- `.github/workflows/pages.yml` builds and deploys to GitHub Pages on push to `main`

## Screenshots and privacy

Lab screenshots must be redacted before they are added. The build copies only images referenced by a post, and `tools/check-output.py` checks the output against the approved list in `tools/approved-screenshots.txt`.
