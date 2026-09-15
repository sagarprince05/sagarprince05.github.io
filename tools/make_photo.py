"""Cut the headshot out of its plain wall background → assets/prince.webp (RGBA).

Flood-fills the near-uniform wall from the image border, cleans the mask with
min/max filters, feathers the edge, then crops to the subject.
Run:  python tools/make_photo.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SRC = r"C:\Users\Prince\Pictures\WhatsApp Image 2026-09-08 at 2.33.52 AM.jpeg"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "prince.webp")
THRESH = 150         # summed RGB distance tolerated while flood-filling the wall (skin is ~300 away)
KEY = (255, 0, 255)  # fill colour that cannot occur in the photo

im = Image.open(SRC).convert("RGB")
W, H = im.size

# 1. Flood-fill the wall from many points along the top / left / right edges
work = im.copy()
seeds = ([(x, 2) for x in range(2, W, 30)] + [(x, H - 3) for x in range(2, W, 30)]
         + [(2, y) for y in range(2, H, 30)] + [(W - 3, y) for y in range(2, H, 30)])
for xy in seeds:
    r, g, b = work.getpixel(xy)[:3]
    if (r, g, b) != KEY and (r + g + b) / 3 > 150:   # only seed on light (wall) pixels
        ImageDraw.floodfill(work, xy, KEY, thresh=THRESH)

# 2. Mask: 255 = subject, 0 = wall
mask = Image.new("L", (W, H), 255)
px_work, px_mask = work.load(), mask.load()
for y in range(H):
    for x in range(W):
        if px_work[x, y] == KEY:
            px_mask[x, y] = 0

# 3. Clean: remove speckles, then pull the edge in slightly and feather it
mask = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(7))
mask = mask.filter(ImageFilter.GaussianBlur(1.6))

# 4. Compose RGBA and crop to the subject with a little headroom
rgba = im.copy(); rgba.putalpha(mask)
bbox = mask.point(lambda v: 255 if v > 8 else 0).getbbox()
x0, y0, x1, y1 = bbox
pad = 24
rgba = rgba.crop((max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), H))  # keep bottom edge flush

# 5. Resize to 1000px wide max and save
if rgba.width > 1000:
    rgba = rgba.resize((1000, round(rgba.height * 1000 / rgba.width)), Image.LANCZOS)
rgba.save(OUT, "WEBP", quality=88, method=6)
print("wrote", OUT, rgba.size, round(os.path.getsize(OUT) / 1024), "KB")
