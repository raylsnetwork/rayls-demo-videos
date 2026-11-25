# Rayls demo videos

Source for the demo videos embedded on the **Demos** page at the bottom of each product section on
docs.rayls.com. The repo is public and the docs load the files from raw.githubusercontent.com, pinned to a
commit: `https://raw.githubusercontent.com/raylsnetwork/rayls-demo-videos/<sha>/videos/<file>.mp4`.
GitHub Pages is off for the org, and jsDelivr refuses repos over 50 MB. raw serves MP4 as `application/octet-stream`;
Chrome, Firefox and Safari (WebKit, tested 2026-11-25) still play it.

- `videos/` — MP4 (H.264 + AAC, `+faststart`), named `YYYY-MM-DD-<product>-<topic>.mp4`
- `posters/` — first-frame JPEGs with the same names, used as `poster=` on the docs pages
- `demos.json` — the timeline: date, product section, title, description, file or Loom link

To add a demo: drop the MP4 (re-mux with `ffmpeg -i in.mov -c:v libx264 -crf 23 -c:a aac -movflags +faststart out.mp4`),
add a poster and a `demos.json` entry, push, then update the section's Demos page in ReadMe.
Keep each file around **20 MB or less** so it starts quickly. For a 60 s 1080p clip,
`-c:v libx264 -preset slow -crf 25 -maxrate 2200k -bufsize 4400k -c:a aac -b:a 128k` lands around 16 MB.
For AMA recordings, `tools/cut_ama.py` keeps only the screen-share segments and splits them into ~8 min parts.

To publish: merge to `main` (PR required), then
`python3 tools/build_pages.py https://raw.githubusercontent.com/raylsnetwork/rayls-demo-videos/$(git rev-parse --short HEAD)`
and `README_API_KEY=… python3 tools/upload_pages.py <ReadMe branch>`.
