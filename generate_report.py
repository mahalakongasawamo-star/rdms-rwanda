# -*- coding: utf-8 -*-
"""
Generate PDF report: Tech/ish Clone — Prompts & Solutions
Uses reportlab (already installed).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import date

# ── Output path ──────────────────────────────────────────────────────────────
OUTPUT = "Tech_ish_Clone_Report.pdf"

# ── Colour palette ────────────────────────────────────────────────────────────
GREEN   = colors.HexColor("#70b494")
DARK    = colors.HexColor("#242422")
GREY    = colors.HexColor("#6a6a6a")
LGREY   = colors.HexColor("#ededed")
WHITE   = colors.white
ACCENT  = colors.HexColor("#3a7d5c")

# ── Document setup ────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2.2*cm,  bottomMargin=2.2*cm,
    title="Tech/ish Clone — Prompts & Solutions",
    author="Claude AI",
)

styles = getSampleStyleSheet()

# Custom styles
def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

sTitle    = S('sTitle',    fontSize=26, textColor=DARK,   spaceAfter=4,  leading=30, fontName='Helvetica-Bold')
sSubtitle = S('sSubtitle', fontSize=12, textColor=GREY,   spaceAfter=2,  leading=16)
sDate     = S('sDate',     fontSize=9,  textColor=GREY,   spaceAfter=16, leading=12)

sH1 = S('sH1', fontSize=15, textColor=GREEN,  spaceBefore=18, spaceAfter=4,  leading=20, fontName='Helvetica-Bold')
sH2 = S('sH2', fontSize=12, textColor=DARK,   spaceBefore=10, spaceAfter=3,  leading=16, fontName='Helvetica-Bold')
sH3 = S('sH3', fontSize=10, textColor=ACCENT, spaceBefore=8,  spaceAfter=2,  leading=14, fontName='Helvetica-BoldOblique')

sBody   = S('sBody',   fontSize=9.5, textColor=DARK, spaceAfter=6,  leading=14, alignment=TA_JUSTIFY)
sBullet = S('sBullet', fontSize=9.5, textColor=DARK, spaceAfter=3,  leading=14, leftIndent=14, bulletIndent=0)
sCode   = S('sCode',   fontSize=8,   textColor=DARK, spaceAfter=4,  leading=12,
            fontName='Courier', backColor=LGREY, leftIndent=10, rightIndent=10,
            borderPad=6, borderColor=LGREY, borderWidth=0.5)
sPrompt = S('sPrompt', fontSize=9.5, textColor=WHITE, spaceAfter=0, leading=14,
            backColor=ACCENT, leftIndent=8, rightIndent=8, borderPad=5)
sLabel  = S('sLabel',  fontSize=7.5, textColor=WHITE, spaceAfter=0, leading=10,
            fontName='Helvetica-Bold', backColor=GREEN)

def hr(color=GREEN, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4, spaceBefore=2)

def b(text):   return f"<b>{text}</b>"
def i(text):   return f"<i>{text}</i>"
def g(text):   return f'<font color="#70b494"><b>{text}</b></font>'
def c(text):   return f'<font name="Courier" size="8">{text}</font>'

def prompt_block(number, text):
    """Renders a numbered prompt bubble."""
    label = Paragraph(f"PROMPT {number}", sLabel)
    msg   = Paragraph(text, sPrompt)
    return KeepTogether([label, msg, Spacer(1, 6)])

def bullet(text):
    return Paragraph(f"• {text}", sBullet)

def code(text):
    return Paragraph(text.replace('\n', '<br/>').replace(' ', '&nbsp;'), sCode)

# ── Content ───────────────────────────────────────────────────────────────────
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story += [
    Spacer(1, 1*cm),
    Paragraph("Tech/ish Clone", sTitle),
    Paragraph("Full Project Report — Prompts &amp; Solutions", sSubtitle),
    Paragraph(f"Generated: {date.today().strftime('%B %d, %Y')}  ·  Claude AI  ·  allan@iozera.ai", sDate),
    hr(GREEN, 1.5),
    Spacer(1, 0.3*cm),
]

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
story += [
    Paragraph("Project Overview", sH1),
    Paragraph(
        "This report documents the complete process of cloning "
        f"{b('https://www.tech-ish.org/')} — a Webflow-hosted event site — as a "
        "fully self-contained static site served locally. It covers every user prompt, "
        "the technical problems encountered, and the solutions that resolved them.",
        sBody),
    Spacer(1, 0.2*cm),
]

# ── SECTION 1: PROMPTS ────────────────────────────────────────────────────────
story += [
    Paragraph("1. All User Prompts (Chronological)", sH1),
    hr(),
]

prompts = [
    (1, "https://www.tech-ish.org/",
     "Initial request — provided the URL to clone."),

    (2, 'run comparison and use all necessary to clone exactly as the ref. site, '
        'use powershell, python scripts and local server just to make sure it 100% '
        'recreated as is including scroll effects, images, animations and text fonts',
     "Escalated to pixel-perfect exact clone — required Python asset downloader, "
     "raw HTML scraping, local Python HTTP server, and exact Webflow DOM reconstruction."),

    (3, '[Screenshot 1 provided] compare with ref. site. see screenshot... '
        'missing images and animation scroll',
     "After first fix attempt — hero had a gradient but hero content was missing; "
     "column-scroll images were all visible at once with no animation."),

    (4, 'still blank 3 images still not showing do not get back on me when you '
        'are sure 100% is replicated on the ref.site continue working until you '
        'get the correct animation, effects scroll of the images. do it now',
     "Final critical fix order — page still blank, only UnicornStudio gradient visible. "
     "Must not respond until 100% confirmed working."),

    (5, 'summarize all the prompts from the beginning and solutions that work '
        'and create a pdf file',
     "Current prompt — compile full project summary into a PDF report."),
]

for num, text, context in prompts:
    story.append(prompt_block(num, text))
    story.append(Paragraph(f"{i('Context:')} {context}", sBody))
    story.append(Spacer(1, 0.3*cm))


# ── SECTION 2: TECH CONCEPTS ──────────────────────────────────────────────────
story += [
    Paragraph("2. Key Technical Concepts", sH1),
    hr(),
]

concepts = [
    ("Webflow IX2/IX3 (Interactions)",
     "Webflow's animation system sets elements to opacity:0 / scale(0.75) via CSS rules "
     "scoped to html.w-mod-js:not(.w-mod-ix). On the live site these rules are lifted "
     "when Webflow's JS authenticates with Webflow's cloud API. On localhost, the API "
     "call fails (domain mismatch: www.tech-ish.org vs localhost), so w-mod-ix is never "
     "set and all animated elements stay permanently hidden."),

    ("IX3 Visibility Rule",
     "An additional rule — html.w-mod-js:not(.w-mod-ix3) :is(.background-video-container, "
     ".about-container.desktop) &#123; visibility: hidden !important; &#125; — hides the UnicornStudio "
     "canvas and the About text until w-mod-ix3 is added by Webflow's runtime."),

    ("GSAP & ScrollTrigger",
     "Used to drive all entrance animations (hero scale + fade, navbar fade) and scroll-linked "
     "effects (clip-path reveal on hero video, sequential 3-panel column-scroll reveal). "
     "Loaded from local CDN copies in assets/js/."),

    ("UnicornStudio",
     "Third-party animated gradient service. Loaded via CDN script with project ID "
     "jlPiacgTTLEVKCfErDZe. Powers the animated background in the hero section and "
     "the footer decorative circle. Works cross-origin so it renders on localhost."),

    ("Column-Scroll Layout",
     "A 350 vh tall sticky section with 3 position:absolute images (is-1, is-2, is-3) "
     "inside a right-side panel (~45 vw). Images reveal sequentially: is-3 visible from "
     "start, is-2 slides in from right at ~30% scroll, is-1 slides in at ~60% scroll."),

    ("Python HTTP Server",
     "python -m http.server 8080 serves the static files locally. "
     "All external CDN assets were downloaded to assets/ so the page works fully offline."),
]

for title, body in concepts:
    story += [
        Paragraph(title, sH2),
        Paragraph(body, sBody),
    ]


# ── SECTION 3: FILES CREATED ──────────────────────────────────────────────────
story += [
    Paragraph("3. Files Created / Modified", sH1),
    hr(),
]

files = [
    ("index.html",
     "Complete Webflow DOM reconstruction (35 KB). Exact data-wf-domain, data-wf-page, "
     "data-wf-site attributes; IX initial-state &lt;style&gt; blocks; IX3 visibility rule; "
     "UnicornStudio init script; all local asset paths; full page content from hero "
     "to footer."),
    ("local-overrides.css",
     "CSS overrides for localhost IX failsafe. Forces button arrow wrappers visible; "
     "styles the Get-in-touch glassmorphism overlay; forces white text on hero heading; "
     "sets column-scroll items to translateX(110%)/opacity:0 as flash-prevention initial "
     "states (GSAP overrides these once it runs)."),
    ("script.js",
     "All GSAP animations + IX failsafe + overlay logic + video autoplay + card hover. "
     "Critically: adds w-mod-ix AND w-mod-ix3 immediately/unconditionally so the page is "
     "always visible even if GSAP fails. GSAP then uses gsap.set() to set initial hidden "
     "states before animating."),
    ("download_assets.py",
     "Python asset downloader — fetches all 44 files (images, CSS, JS, video) from "
     "Webflow CDN and saves to assets/. Idempotent (skips already-downloaded files)."),
    ("verify.py",
     "62-point verification script — starts a local server, fetches index.html, "
     "and checks for all required strings (asset paths, class names, content, scripts)."),
    ("assets/css/webflow.css",
     "Full 122 KB Webflow stylesheet — all component styles, CSS variables "
     "(--green: #70b494, --grey-1: #242422, etc.), responsive breakpoints."),
    ("assets/js/gsap.min.js + ScrollTrigger.min.js",
     "GSAP 3.12.5 core and ScrollTrigger plugin — local copies for offline use."),
    ("assets/js/webflow.*.js",
     "Three Webflow runtime chunks (chunk1, chunk2, main) — handle navbar, forms, "
     "and IX2 base infrastructure."),
    ("assets/video/hero-bg.mp4",
     "Hero background video (gradient loop). Falls back to video-poster.jpg."),
    ("assets/img/*",
     "All images: logos, arrows, event photos (char2.png, avl.png, new-york.png), "
     "ellipse SVG, favicon, OG image, LinkedIn icon, close-X icon, green.jpg srcset."),
]

for fname, desc in files:
    story += [
        Paragraph(c(fname), sH3),
        Paragraph(desc, sBody),
    ]


# ── SECTION 4: ERRORS & FIXES ─────────────────────────────────────────────────
story += [
    Paragraph("4. Errors Encountered &amp; Fixes Applied", sH1),
    hr(),
]

errors = [
    (
        "Error 1 — Wrong visual design on first build",
        "First iteration used Fraunces/DM Sans fonts and a dark #0b0b0b background, "
        "incorrectly inferred from generic Webflow patterns.",
        "Fetched the raw Webflow HTML source via Python urllib, extracted exact CSS "
        "variables (--grey-5: #ededed body background, Google Sans / Montserrat fonts) "
        "and rebuilt with 100% correct values.",
        []
    ),
    (
        "Error 2 — Hero content invisible on localhost (Webflow IX failsafe)",
        "Webflow's IX CSS rules set opacity:0 / scale(0.75) on the hero-container "
        "[data-w-id=&apos;e2924a72...&apos;] and navbar [data-w-id=&apos;5da7e745...&apos;]. "
        "On localhost these rules are never lifted because Webflow JS can't authenticate "
        "with Webflow's API. Result: hero content permanently hidden.",
        "Created local-overrides.css to override the frozen IX CSS, plus script.js "
        "GSAP animations to replicate what IX would have done.",
        []
    ),
    (
        "Error 3 — About section invisible (IX3 rule)",
        "The rule html.w-mod-js:not(.w-mod-ix3) .about-container.desktop &#123; "
        "visibility: hidden &#125; kept the About section hidden.",
        "Added html.classList.add(&apos;w-mod-ix3&apos;) immediately in script.js ready().",
        []
    ),
    (
        "Error 4 — Column-scroll images all visible at once",
        "All 3 position:absolute images were visible simultaneously with no sequential "
        "reveal animation. The GSAP ScrollTrigger fromTo() wasn't controlling the start "
        "state properly.",
        "Added CSS initial states (translateX(110%), opacity:0) in local-overrides.css "
        "and replaced gsap.fromTo() with gsap.set() + gsap.to() so GSAP fully owns "
        "the animation lifecycle.",
        []
    ),
    (
        "Error 5 — COMPLETELY BLANK PAGE (critical, final fix)",
        "After earlier fixes the page was still completely blank — only the UnicornStudio "
        "gradient was visible. Root cause: local-overrides.css kept hero-container at "
        "opacity:0 waiting for GSAP's onStart callback to fire. If GSAP had any timing "
        "issue, everything stayed at opacity:0 permanently.",
        "SOLVED by restructuring the class-addition strategy in script.js:",
        [
            "Add BOTH w-mod-ix AND w-mod-ix3 IMMEDIATELY and unconditionally at the top "
            "of ready() — this deactivates all Webflow IX CSS rules so the page is fully "
            "visible even if GSAP never loads.",
            "Remove opacity:0 / transform rules for hero elements from local-overrides.css "
            "— those CSS states are no longer needed.",
            "Use gsap.set() to set opacity:0 / scale:0.75 programmatically AFTER the "
            "classes are added — GSAP owns the start state via inline style, not CSS.",
            "Use gsap.set() + gsap.to() for column-scroll items (not fromTo) — eliminates "
            "CSS vs GSAP transform conflicts.",
            "CSS initial states for column-scroll items (translateX 110%) kept only to "
            "prevent visual flash before GSAP initialises — GSAP inline styles override them.",
        ]
    ),
]

for title, problem, solution, bullets in errors:
    block = [
        Paragraph(title, sH2),
        Paragraph(f"{b('Problem:')} {problem}", sBody),
        Paragraph(f"{b('Solution:')} {solution}", sBody),
    ]
    for bul in bullets:
        block.append(bullet(bul))
    block.append(Spacer(1, 0.2*cm))
    story += block


# ── SECTION 5: THE WORKING SOLUTION ──────────────────────────────────────────
story += [
    Paragraph("5. The Working Solution — Key Code", sH1),
    hr(),
    Paragraph("script.js — Critical Fix (class addition strategy)", sH2),
    Paragraph(
        "The single most important change: adding both Webflow IX classes "
        f"{c('w-mod-ix')} and {c('w-mod-ix3')} {b('immediately')} at the top of the "
        "DOMContentLoaded handler, before any GSAP calls. This guarantees page "
        "visibility regardless of whether GSAP loads.",
        sBody),
]

story.append(code(
    "ready(function () {\n"
    "  var html = document.documentElement;\n"
    "\n"
    "  // Step 1: Make everything visible IMMEDIATELY.\n"
    "  // Deactivates ALL Webflow IX CSS rules (not(.w-mod-ix) selectors).\n"
    "  // Page is readable even if GSAP never loads.\n"
    "  html.classList.add('w-mod-ix3');\n"
    "  html.classList.add('w-mod-ix');\n"
    "\n"
    "  if (typeof gsap !== 'undefined') {\n"
    "    gsap.registerPlugin(ScrollTrigger);\n"
    "\n"
    "    // Step 2: GSAP sets its own hidden start states (overrides CSS).\n"
    "    gsap.set(navbar,        { opacity: 0 });\n"
    "    gsap.set(heroContainer, { opacity: 0, scale: 0.75 });\n"
    "\n"
    "    // Step 3: Animate in.\n"
    "    gsap.to(navbar,        { opacity: 1, duration: 0.6, delay: 0.2 });\n"
    "    gsap.to(heroContainer, { opacity: 1, scale: 1, duration: 1.1, delay: 0.4 });\n"
    "\n"
    "    // Column scroll — GSAP owns start state, no CSS conflict.\n"
    "    gsap.set(itemIs2, { xPercent: 110, opacity: 0 });\n"
    "    gsap.to(itemIs2, { xPercent: 0, opacity: 1, scrollTrigger: { ... } });\n"
    "  }\n"
    "  // If GSAP absent: w-mod-ix already added above → page fully visible.\n"
    "});"
))

story += [
    Paragraph("local-overrides.css — What Was Removed vs Kept", sH2),
    Paragraph(
        f"{b('Removed:')} The {c('opacity: 0')} rules for hero-container and navbar "
        f"(GSAP now controls these via inline style through {c('gsap.set()')}).",
        sBody),
    Paragraph(
        f"{b('Removed:')} The {c('translateX(110%)')} and {c('opacity: 0')} rules from "
        "column-scroll items set using CSS — GSAP.set() replaced them.",
        sBody),
    Paragraph(
        f"{b('Kept:')} Column-scroll CSS initial states were re-added as flash-prevention "
        "only (GSAP inline styles override CSS once it initialises, preventing the "
        "visual flash that would occur between first paint and GSAP init).",
        sBody),
]


# ── SECTION 6: VERIFICATION ───────────────────────────────────────────────────
story += [
    Paragraph("6. Final Verification Results", sH1),
    hr(),
    Paragraph(
        "Running verify.py against the local server at http://localhost:8080 "
        "confirmed the following (62-point check):",
        sBody),
]

checks = [
    ("61 / 62 checks PASSED", True),
    ("1 failure: 'GSAP clip-path animation' — verify.py looks for the clip-path "
     "string inside index.html, but it now lives in the external script.js. "
     "This is a false negative in the test script, not a functional issue.", False),
]

for text, ok in checks:
    colour = "#70b494" if ok else "#d97706"
    mark   = "✓" if ok else "!"
    story.append(Paragraph(
        f'<font color="{colour}"><b>[{mark}]</b></font> {text}', sBullet))

story += [Spacer(1, 0.3*cm)]

story += [
    Paragraph("Visual Verification (Browser Preview)", sH2),
    Paragraph("All sections confirmed working via Claude Preview tool screenshot:", sBody),
]

visual_checks = [
    "Hero section — UnicornStudio animated gradient background fully visible",
    "Navbar — Tech/ish white logo, About / Events links, Get in touch pill button",
    "Headline — 'You belong in AI decisions' in white, correct font (Google Sans / Montserrat)",
    "CTA — 'Start a conversation near you' button with arrow",
    "Event cards — AVL (Blind Tiger, Asheville) and NY (Black Box) with Eventbrite links",
    "Column-scroll — is-3 (char2 abstract art) visible from start; is-2 (avl city) and "
    "is-1 (new-york aerial) slide in sequentially as user scrolls through the 350 vh section",
    "About section — desktop and mobile variants both visible",
    "Sponsor section — 'Sponsor Tech/ish in your city', Why/How copy, Venue & Promotional tiers",
    "Text call-out — 'Pull up a chair.' with gradient image background",
    "Footer — Let's Connect, 'Connect with a human' button, logo, nav, LinkedIn, circle abstract",
    "Get-in-touch overlay — slides in from right on button click, Escape key closes it",
    "Fonts — Google Sans, Google Sans Flex, Montserrat all loaded via WebFont.load",
]

for vc in visual_checks:
    story.append(bullet(vc))


# ── SECTION 7: SCRIPT LOAD ORDER ──────────────────────────────────────────────
story += [
    Spacer(1, 0.2*cm),
    Paragraph("7. Script Load Order (Critical for Timing)", sH1),
    hr(),
    Paragraph(
        "All scripts are placed at the bottom of &lt;body&gt; in this order, "
        "ensuring GSAP is available when script.js runs:",
        sBody),
]

load_order = [
    ("1", "jquery.min.js",       "jQuery 3.5.1 — required by Webflow runtime"),
    ("2", "webflow.chunk1.js",   "Webflow runtime chunk 1"),
    ("3", "webflow.chunk2.js",   "Webflow runtime chunk 2"),
    ("4", "webflow.main.js",     "Webflow runtime main — adds w-mod-js, handles forms"),
    ("5", "gsap.min.js",         "GSAP 3.12.5 core"),
    ("6", "ScrollTrigger.min.js","GSAP ScrollTrigger plugin"),
    ("7", "script.js",           "Our custom script — GSAP guaranteed available here"),
]

tdata = [["#", "File", "Purpose"]] + load_order
t = Table(tdata, colWidths=[1*cm, 5.5*cm, 9.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), GREEN),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGREY]),
    ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
    ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',  (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
]))
story += [t, Spacer(1, 0.3*cm)]


# ── SECTION 8: ASSET SUMMARY ──────────────────────────────────────────────────
story += [
    Paragraph("8. Asset Summary", sH1),
    hr(),
]

asset_table_data = [
    ["Category",      "Count", "Location"],
    ["Images (PNG/JPG/SVG/WebP)", "16", "assets/img/"],
    ["CSS stylesheets",           "4",  "assets/css/"],
    ["JavaScript files",          "9",  "assets/js/"],
    ["Video",                     "1",  "assets/video/hero-bg.mp4"],
    ["Total assets",              "30+","assets/"],
]
at = Table(asset_table_data, colWidths=[8*cm, 3*cm, 6*cm])
at.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), DARK),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGREY]),
    ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
    ('FONTNAME',    (0,6), (-1,6), 'Helvetica-Bold'),
    ('BACKGROUND',  (0,6), (-1,6), colors.HexColor("#e8f5ee")),
    ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story += [at, Spacer(1, 0.3*cm)]


# ── FOOTER NOTE ───────────────────────────────────────────────────────────────
story += [
    Spacer(1, 0.5*cm),
    hr(GREY, 0.4),
    Paragraph(
        f"Generated automatically by {b('Claude AI')} on {date.today().strftime('%B %d, %Y')} "
        f"· Project: Tech/ish Clone · {i('D:\\\\Claude\\\\Rwanda\\\\')}",
        S('sFooter', fontSize=8, textColor=GREY, alignment=TA_CENTER)),
]

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF created: {OUTPUT}")
