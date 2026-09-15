# Prince Sagar — Portfolio

A fast, accessible, dark-minimal portfolio for an AI deployment engineer. Hand-coded in HTML, CSS and vanilla JavaScript — no build step, no frameworks, no trackers.

Design is inspired by the best-in-class portfolios of Brittany Chiang (sticky sidebar, spotlight hover), Lee Robinson (typographic restraint), Josh Comeau (micro-interactions, theme toggle), Bruno Simon (an interactive touch — the cursor spotlight) and Rauno Freiberg (craft in every hover state).

## Files

```
index.html                       Home: about, experience, projects, skills, contact
projects/
  site-onboarding.html           Case study — Site Onboarding & Approval Automation
  humyn-watcher.html             Case study — Humyn Watcher (AI Slack assistant)
  voucher-price-tracker.html     Case study — Voucher Price Tracker
styles.css                       Design tokens (:root) + layout + case-study styles
script.js                        Theme toggle, spotlight, active nav, scroll reveal, copy email
assets/
  favicon.svg                    "P" mark — change the letter/colours here
  resume.pdf                     ADD: your résumé (linked from the Experience section)
  og.png                         ADD: 1200×630 social preview image (referenced in <head>)
```

## Run locally

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 4173
```

then visit http://localhost:4173.

## Editing

| What | Where |
|---|---|
| Name, title, tagline, socials | `index.html` → `<header class="sidebar">` |
| About paragraphs | `index.html` → `<section id="about">` |
| Jobs | `index.html` → `<section id="experience">` — duplicate a `<li class="item job">` |
| Project cards | `index.html` → `<section id="projects">` — duplicate a `<li class="item project">` |
| Case studies | `projects/*.html` — copy one to add a new case study, then link it from a card |
| Skills | `index.html` → `<section id="skills">` |
| Contact email | `index.html` → `mailto:` link, `data-email`, and the JSON-LD block in `<head>` |
| Accent colour | `styles.css` → `--accent`, `--accent-strong`, `--accent-soft` in `:root` (dark) and `html[data-theme="light"]` |

To use a real screenshot instead of the gradient thumbnail on a card:

```html
<div class="project-thumb"><img src="assets/humyn-watcher.png" alt="Humyn Watcher answering a question in Slack"></div>
```

## Deploy (free)

**GitHub Pages (recommended — matches the URLs already in the `<head>`)**
1. Create a repo named `sagarprince05.github.io` and push this folder to `main`.
2. Settings → Pages → Source: `main`, root folder.
3. Live at https://sagarprince05.github.io within a minute.

**Netlify / Vercel** — drag-and-drop the folder, no build command, publish directory `.`. Then update `og:url` and `canonical` in every HTML file.

## Before going live

- [ ] Add `assets/resume.pdf`
- [ ] Add `assets/og.png` (1200×630) — a screenshot of the hero works well
- [ ] Optionally replace gradient thumbnails with real screenshots
- [ ] Run Lighthouse in Chrome DevTools (Performance / Accessibility / Best Practices / SEO)
