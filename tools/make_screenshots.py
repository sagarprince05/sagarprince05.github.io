"""Convert project screenshots to optimised WebP + card thumbnails.

Source folders (outside the repo):
  C:\\Users\\Prince\\Desktop\\Portfolio Screenshots\\   (Site Onboarding)
  C:\\Users\\Prince\\Desktop\\project\\Slack bot\\         (Humyn Watcher)
Output: assets/screenshots/*.webp   — run:  python tools/make_screenshots.py
"""
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "screenshots")
SO = r"C:\Users\Prince\Desktop\Portfolio Screenshots"
HW = r"C:\Users\Prince\Desktop\project\Slack bot"
MAX_W = 1400
QUALITY = 82

SOURCES = {
    "so-01-site-id-form":        f"{SO}\\01-site-identification-form.png",
    "so-02-site-approved-email": f"{SO}\\08-site-approved-email-with-site-id.png",
    "so-03-recce-form":          f"{SO}\\02-site-recce-form-site-id-verified.png",
    "so-04-review-request-email":f"{SO}\\03-review-request-email.png",
    "so-05-review-page":         f"{SO}\\05-task-review-page-tasks-ticked.png",
    "so-06-decision-recorded":   f"{SO}\\06-decision-recorded.png",
    "so-07-dashboard-sign-in":   f"{SO}\\07-dashboard-sign-in.png",
    "so-08-flowchart":           f"{SO}\\09-system-flowchart.png",
    "hw-01-sql-receipt":         f"{HW}\\screenshot-1-sql-receipt.png",
    "hw-02-fuzzy-question":      f"{HW}\\screenshot-2-fuzzy-question.png",
}

os.makedirs(OUT, exist_ok=True)
sizes = {}

def save(img, name):
    path = os.path.join(OUT, name + ".webp")
    img.save(path, "WEBP", quality=QUALITY, method=6)
    sizes[name] = {"w": img.width, "h": img.height, "kb": round(os.path.getsize(path) / 1024)}

for name, src in SOURCES.items():
    im = Image.open(src).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    save(im, name)

# Card thumbnails (16:10, 640x400) for the home page
def thumb(src, box, name):
    im = Image.open(src).convert("RGB").crop(box)
    im = im.resize((640, 400), Image.LANCZOS)
    save(im, name)

# Site ID form: take the top 800px of the 1280x900 shot (16:10)
thumb(SOURCES["so-01-site-id-form"], (0, 0, 1280, 800), "thumb-site-onboarding")
# Slack fuzzy question: left 784px of the 1300x490 shot (16:10) — shows avatar, question and answer
thumb(SOURCES["hw-02-fuzzy-question"], (0, 0, 784, 490), "thumb-humyn-watcher")

print(json.dumps(sizes, indent=2))
