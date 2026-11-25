# Rayls demo videos

Source for the demo videos embedded on the **Demos** page at the bottom of each product section on
docs.rayls.com. The repo is private; the files are served publicly by the DigitalOcean static site
`rayls-demo-videos` (App Platform, deploys on every push to `main`).

- `videos/` — MP4 (H.264 + AAC, `+faststart`), named `YYYY-MM-DD-<product>-<topic>.mp4`
- `posters/` — first-frame JPEGs with the same names, used as `poster=` on the docs pages
- `demos.json` — the timeline: date, product section, title, description, file or Loom link

To add a demo: drop the MP4 (re-mux with `ffmpeg -i in.mov -c:v libx264 -crf 23 -c:a aac -movflags +faststart out.mp4`),
add a poster and a `demos.json` entry, push, then update the section's Demos page in ReadMe.
Keep each file under 100 MB (GitHub limit).
