#!/usr/bin/env python3
"""Cut the screen-share segments out of an AMA recording and split them into parts under 20 MB.

Usage: python3 tools/cut_ama.py <source.mp4> <out-prefix> <parts> <start-end> [<start-end> ...]
Times are seconds in the source. Each part is encoded at 720p/15 fps, CRF 30, mono AAC 48 kbps
(about 1.9 MB per minute for screen shares), so keep parts under ~9 minutes.
"""
import subprocess
import sys

src, prefix, nparts = sys.argv[1], sys.argv[2], int(sys.argv[3])
segs = [tuple(map(float, s.split("-"))) for s in sys.argv[4:]]
total = sum(b - a for a, b in segs)
target = total / nparts

parts, cur, left = [], [], target
for a, b in segs:
    while b - a > 0:
        take = min(b - a, left)
        cur.append((a, a + take))
        a += take
        left -= take
        if left <= 0.01 and len(parts) < nparts - 1:
            parts.append(cur); cur, left = [], target
if cur:
    parts.append(cur)

for i, p in enumerate(parts, 1):
    fc, labels = [], ""
    for j, (a, b) in enumerate(p):
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=15[v{j}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{j}]")
        labels += f"[v{j}][a{j}]"
    fc.append(f"{labels}concat=n={len(p)}:v=1:a=1[v][a]")
    out = f"{prefix}{'' if nparts == 1 else f'-part{i}'}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "30",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-ac", "1", "-b:a", "48k", "-movflags", "+faststart", out],
                   check=True)
    print(out, round(sum(b - a for a, b in p)), "s")
