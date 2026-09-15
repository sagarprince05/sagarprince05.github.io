"""Generate assets/og.png (1200x630) matching the portfolio's dark theme."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
OUT = r"C:\Users\Prince\Desktop\project\Portfolio Websites\assets\og.png"
FONTS = r"C:\Windows\Fonts"

BG = (15, 23, 42)          # slate-900
HEADING = (241, 245, 249)  # slate-100
STRONG = (226, 232, 240)   # slate-200
TEXT = (148, 163, 184)     # slate-400
ACCENT = (94, 234, 212)    # teal-300
CHIP_BG = (25, 60, 70)     # teal @ ~10% over bg
BORDER = (38, 48, 70)

bold = lambda s: ImageFont.truetype(f"{FONTS}\\segoeuib.ttf", s)
reg = lambda s: ImageFont.truetype(f"{FONTS}\\segoeui.ttf", s)
mono = lambda s: ImageFont.truetype(f"{FONTS}\\consola.ttf", s)

img = Image.new("RGB", (W, H), BG)

# Soft blue-teal glow (echoes the cursor spotlight) — drawn on a separate layer and blurred
glow = Image.new("RGB", (W, H), BG)
g = ImageDraw.Draw(glow)
g.ellipse((700, -250, 1500, 450), fill=(29, 78, 216))
glow = glow.filter(ImageFilter.GaussianBlur(160))
img = Image.blend(img, glow, 0.35)

d = ImageDraw.Draw(img)
PAD = 80

# Eyebrow (mono, letter-spaced, accent)
eyebrow = "sagarprince05.github.io  ·  portfolio"
d.text((PAD, 78), eyebrow, font=mono(18), fill=ACCENT)

# Name + title
d.text((PAD - 4, 118), "Prince Sagar", font=bold(96), fill=HEADING)
d.text((PAD, 238), "AI Deployment Engineer", font=reg(40), fill=STRONG)

# Tagline, wrapped
tag_font = reg(28)
tagline = ("AI assistants, automations and data pipelines that run 24/7 in "
           "production — on infrastructure that costs nothing.")
words, lines, cur = tagline.split(), [], ""
for w in words:
    t = (cur + " " + w).strip()
    if d.textlength(t, font=tag_font) > W - 2 * PAD - 260:
        lines.append(cur); cur = w
    else:
        cur = t
lines.append(cur)
y = 312
for ln in lines:
    d.text((PAD, y), ln, font=tag_font, fill=TEXT)
    y += 40

# Tag chips
chips = ["Python", "Claude Code", "Cloudflare Workers", "Supabase", "Google Apps Script", "Slack & Telegram bots"]
cf = mono(18)
x, cy = PAD, 470
for c in chips:
    tw = d.textlength(c, font=cf)
    d.rounded_rectangle((x, cy, x + tw + 28, cy + 36), radius=18, fill=CHIP_BG)
    d.text((x + 14, cy + 8), c, font=cf, fill=ACCENT)
    x += tw + 28 + 12

# Footer line + status
d.line((PAD, 548, W - PAD, 548), fill=BORDER, width=1)
d.ellipse((PAD, 573, PAD + 12, 585), fill=ACCENT)
d.text((PAD + 22, 566), "Software Developer Intern · Kratos Gaming Network (KGeN)", font=reg(20), fill=TEXT)

# "P" mark bottom-right (matches favicon.svg)
mx, my, ms = W - PAD - 64, 556, 64
d.rounded_rectangle((mx, my, mx + ms, my + ms), radius=14, fill=(11, 18, 34), outline=ACCENT, width=2)
pf = bold(34)
pw = d.textlength("P", font=pf)
d.text((mx + (ms - pw) / 2, my + 10), "P", font=pf, fill=ACCENT)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
