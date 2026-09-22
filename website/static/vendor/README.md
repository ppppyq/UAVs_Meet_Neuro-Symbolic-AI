# Vendored browser dependencies

- Liquid Glass JS `container.js`, commit
  `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`:
  https://github.com/dashersw/liquid-glass-js
  MIT, Copyright (c) 2025 Armagan Amcalar. License in `liquid-glass-js/LICENSE`.
- html2canvas 1.4.1, `dist/html2canvas.min.js`:
  https://github.com/niklasvh/html2canvas/tree/v1.4.1
  MIT. License in `html2canvas/LICENSE`.

These files are served locally. Builds do not download dependencies.

Local shader changes in `container.js` convert refraction offsets into CSS
pixels before normalizing them to the page texture. This keeps the glass edge
strength consistent when filtering changes the length of the paper archive.
The upstream multi-layer refraction, shape masks and blur remain in use.
An additional pointer-driven ripple refracts the background locally beneath the
navigation and hero buttons, with reduced-motion and touch-release handling.

`../liquid-glass.js` subclasses Container to attach its renderer beneath native
links and controls. It owns shared snapshots, texture refresh, responsive sizing,
render scheduling, and CSS fallback. Upstream demo UI and Button are not needed.

Scroll and pointer interactions redraw visible lenses at up to 30 fps. The page
shares one size-limited background texture; layout/filter changes refresh it.
The animated hero refreshes every 1.2 seconds while visible and idle. This is a
DOM snapshot renderer, not a live capture of arbitrary video or WebGL canvases.
Reduced-motion mode disables the idle refresh and animated distortion; missing
dependencies or WebGL keep the CSS glass and native controls usable.
