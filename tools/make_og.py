"""Generate assets/og.png (1200x630) in the site's lime style, with the photo cutout.
Run:  python tools/make_og.py   (after tools/make_photo.py)"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H = 1200, 630
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "og.png")
PHOTO = os.path.join(ROOT, "assets", "prince.webp")
FONTS = r"C:\Windows\Fonts"

LIME, LIME_2, INK, MUTED = (201, 255, 79), (214, 255, 110), (13, 17, 16), (60, 68, 64)
bold = lambda s: ImageFont.truetype(f"{FONTS}\\segoeuib.ttf", s)
reg = lambda s: ImageFont.truetype(f"{FONTS}\\segoeui.ttf", s)
serif_i = lambda s: ImageFont.truetype(f"{FONTS}\\georgiai.ttf", s)

# Background: lime with a white glow behind the photo
img = Image.new("RGB", (W, H), LIME)
glow = Image.new("RGB", (W, H), LIME)
g = ImageDraw.Draw(glow)
g.ellipse((640, 60, 1240, 700), fill=(255, 255, 255))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.blend(img, glow, 0.55)

# Photo cutout, grayscale, anchored bottom-right
photo = Image.open(PHOTO).convert("RGBA")
ph = 600
photo = photo.resize((round(photo.width * ph / photo.height), ph), Image.LANCZOS)
gray = ImageOps.grayscale(photo).convert("RGBA"); gray.putalpha(photo.getchannel("A"))
img = img.convert("RGBA")
img.alpha_composite(gray, (W - gray.width - 40, H - gray.height))
img = img.convert("RGB")

d = ImageDraw.Draw(img)
PAD = 72

# Badge
badge = "Forward Deployed Engineer  ·  KGeN"
bf = reg(20); bw = d.textlength(badge, font=bf)
d.rounded_rectangle((PAD, 70, PAD + bw + 36, 70 + 40), radius=20, fill=(255, 255, 255, 200), outline=(255, 255, 255))
d.text((PAD + 18, 77), badge, font=bf, fill=INK)

# Headline
d.text((PAD - 4, 138), "Hi, I'm Prince", font=bold(84), fill=INK)
d.text((PAD - 2, 236), "Forward Deployed", font=serif_i(76), fill=INK)
d.text((PAD - 2, 318), "Engineer", font=serif_i(76), fill=INK)

# Blurb (wrapped to the left 55%)
tf = reg(24)
blurb = ("I go close to the real problem, build the solution, deploy it into "
         "your environment, and make sure it actually works.")
words, lines, cur = blurb.split(), [], ""
for w in words:
    t = (cur + " " + w).strip()
    if d.textlength(t, font=tf) > 560: lines.append(cur); cur = w
    else: cur = t
lines.append(cur)
y = 440
for ln in lines:
    d.text((PAD, y), ln, font=tf, fill=MUTED); y += 33

# URL
d.text((PAD, 566), "sagarprince05.github.io", font=bold(20), fill=INK)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, round(os.path.getsize(OUT) / 1024), "KB")
