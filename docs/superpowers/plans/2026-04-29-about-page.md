# /about Page + Homepage Teaser Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a new dedicated `about.html` page (long-form RDMS story, vision, mission, values, credibility) and refresh the homepage `#about` block into a short teaser that links to it.

**Architecture:** Static HTML/CSS site (Webflow export, no build system, no SSR, no test framework). The new page reuses the existing navbar + footer markup verbatim and is themed via a new page-scoped stylesheet `assets/css/about.css`. A small page-scoped script `assets/js/about.js` provides scroll-reveal via `IntersectionObserver` with `prefers-reduced-motion` support. The homepage teaser refresh edits `index.html` + `local-overrides.css` only.

**Tech Stack:** HTML5 · CSS (custom properties + `clamp()` fluid typography) · vanilla JS · Google Sans / Google Sans Flex / Georgia (system fallback) · existing Webflow runtime (untouched).

**Spec reference:** `docs/superpowers/specs/2026-04-29-about-page-design.md`

**Verification model:** No automated test framework exists in this project. Each task ends with a **manual browser verification step** plus a `git diff` review. The verification step lists exactly what to look for so the engineer doesn't ship broken visuals.

**Browser to use for verification:** Open files directly with `file://` URLs (e.g. `file:///d:/Claude/Rwanda/about.html`) in any modern browser. Use the browser's DevTools responsive mode at widths `1280px` (desktop), `768px` (tablet), and `390px` (mobile) for each verification step.

---

## File Plan

| Path | Action | Responsibility |
|---|---|---|
| `about.html` | **Create** | Full /about page markup. Reuses navbar + footer from `index.html` verbatim. |
| `assets/css/about.css` | **Create** | All `/about`-only styles. CSS custom-property tokens at top, then block-by-block sections. |
| `assets/js/about.js` | **Create** | `IntersectionObserver` scroll-reveal + reduced-motion check. ~30 lines. |
| `index.html` | **Modify** | Replace lines ~265–277 (existing `.about-container` desktop + mobile) with teaser markup. Update two `/about` links → `about.html` (line ~192 nav, line ~417 footer). |
| `local-overrides.css` | **Modify** | Append teaser-specific styles for the new homepage `#about` block. |

---

## Token Reference (used throughout)

```css
/* CSS custom properties on :root in about.css */
--cream-bg:        #f6f3ec;
--cream-tint:      #ece6d6;
--card-bg:         #ffffff;
--card-border:     #e3ddd1;
--text-primary:    #0a0a0a;
--text-body:       #2a2a2a;
--text-secondary:  #4a4a4a;
--text-muted:      #7a7a7a;
--green-on-light:  #1f6b3a;
--green-on-dark:   #a9e0b6;
--green-accent:    #58cc6f;
--dark-band:       #0a0a0a;
--vision-overlay:  linear-gradient(135deg, #1c3a2c, #3d6b52);
--mission-overlay: linear-gradient(135deg, #3d3a32, #1f1d18);
```

---

### Task 1: Create `about.html` skeleton with navbar + footer + cream body

**Files:**
- Create: `about.html`
- Create: `assets/css/about.css`

- [ ] **Step 1: Create `assets/css/about.css` with custom-property tokens and base body styles**

Create `assets/css/about.css` with this content:

```css
/* ============================================================
   /about page styles — cream palette, flush-left typography
   ============================================================ */

:root {
  --cream-bg:        #f6f3ec;
  --cream-tint:      #ece6d6;
  --card-bg:         #ffffff;
  --card-border:     #e3ddd1;
  --text-primary:    #0a0a0a;
  --text-body:       #2a2a2a;
  --text-secondary:  #4a4a4a;
  --text-muted:      #7a7a7a;
  --green-on-light:  #1f6b3a;
  --green-on-dark:   #a9e0b6;
  --green-accent:    #58cc6f;
  --dark-band:       #0a0a0a;
  --vision-overlay:  linear-gradient(135deg, #1c3a2c, #3d6b52);
  --mission-overlay: linear-gradient(135deg, #3d3a32, #1f1d18);
}

body.page-about {
  background: var(--cream-bg);
  color: var(--text-primary);
  font-family: 'Google Sans', sans-serif;
  text-align: left;
  margin: 0;
}

body.page-about main {
  display: block;
}

/* All text on this page is flush-left. Project-wide rule. */
body.page-about h1,
body.page-about h2,
body.page-about h3,
body.page-about p,
body.page-about li,
body.page-about blockquote {
  text-align: left;
}

/* Page section container — applies to most blocks except full-bleed bands */
.about-section {
  padding: clamp(48px, 7vw, 80px) clamp(20px, 4vw, 36px);
  max-width: 1200px;
  margin: 0 auto;
}

/* Eyebrow label — used across most blocks */
.about-eyebrow {
  font-family: 'Google Sans', sans-serif;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--green-on-light);
  margin: 0 0 14px;
  font-weight: 500;
}

.about-eyebrow.on-dark {
  color: var(--green-on-dark);
}

/* Navbar override — flip to dark text on cream */
body.page-about .navbar {
  background: var(--cream-bg) !important;
}
body.page-about .nav-link,
body.page-about .nav-link-2,
body.page-about .brand-name,
body.page-about .brand-acronym {
  color: var(--text-primary) !important;
}
body.page-about .navbar {
  border-bottom: 1px solid var(--card-border);
}
```

- [ ] **Step 2: Create `about.html` with `<head>`, navbar, empty `<main>`, footer**

Create `about.html`. The `<head>` is a trimmed-down version of `index.html`'s `<head>` (same fonts + favicon + viewport). The body has class `page-about`. The navbar is **copied verbatim from `index.html` lines 182–207**. The footer is **copied verbatim from `index.html` lines 367–428** (the `<div class="footer-div">` block). Between navbar and footer, leave a placeholder `<main></main>` — block content arrives in later tasks.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>About RDMS | Rwanda's Dento-Medical Society</title>
  <meta content="RDMS Rwanda is a nonprofit professional society advancing oral and public health through education, research, and outreach." name="description"/>
  <meta content="About RDMS | Rwanda's Dento-Medical Society" property="og:title"/>
  <meta content="A nonprofit professional society advancing oral and public health in Rwanda." property="og:description"/>
  <meta content="assets/img/og-image.png" property="og:image"/>
  <meta property="og:type" content="website"/>
  <meta content="summary_large_image" name="twitter:card"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>

  <link href="assets/css/webflow.css" rel="stylesheet" type="text/css"/>
  <link href="local-overrides.css" rel="stylesheet" type="text/css"/>
  <link href="assets/css/about.css" rel="stylesheet" type="text/css"/>

  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous"/>
  <script src="assets/js/webfont.js" type="text/javascript"></script>
  <script type="text/javascript">WebFont.load({google:{families:["Google Sans:300,400,500,600,700","Google Sans Flex:300,400,500,600,700"]}});</script>

  <link href="assets/img/favicon.png" rel="shortcut icon" type="image/x-icon"/>
  <link href="assets/img/favicon-large.webp" rel="apple-touch-icon"/>
</head>
<body class="page-about">

  <!-- ============================
       NAVBAR  (copied verbatim from index.html lines 182–207)
  ============================= -->
  <!-- PASTE INDEX.HTML LINES 182–207 HERE -->

  <main>
    <!-- /about content blocks added in subsequent tasks -->
  </main>

  <!-- ============================
       FOOTER  (copied verbatim from index.html lines 367–428)
  ============================= -->
  <!-- PASTE INDEX.HTML LINES 367–428 HERE -->

  <!-- Webflow runtime — same load order as index.html -->
  <script src="assets/js/jquery.min.js" type="text/javascript"></script>
  <script src="assets/js/webflow.chunk1.js" type="text/javascript"></script>
  <script src="assets/js/webflow.chunk2.js" type="text/javascript"></script>
  <script src="assets/js/webflow.main.js" type="text/javascript"></script>

  <!-- Page-scoped scroll-reveal (added in Task 9) -->
  <script src="assets/js/about.js" defer></script>
</body>
</html>
```

After pasting, **inside the navbar**, change line 192's `href="/about"` to `href="about.html"` so the link is correct on the new page too. **Inside the footer**, change the line ~417 `<a href="/about" class="link-3">About</a>` to `href="about.html"`.

- [ ] **Step 3: Verify in browser**

Open `file:///d:/Claude/Rwanda/about.html` in your browser at desktop width (1280px).

Expected:
- Cream `#f6f3ec` background fills the viewport
- Navbar visible at top with **dark text** (RDMS brand + About + Events links readable on cream)
- Footer at bottom (dark, unchanged from homepage)
- Empty space between navbar and footer (this is correct — content arrives in next tasks)
- No console errors in DevTools (font 404s for Webflow's exact font URLs are acceptable for now)

If navbar text is white/invisible: check that `body.page-about` class is set on `<body>` and that `assets/css/about.css` is loaded after `local-overrides.css`.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "Add /about skeleton: navbar, footer, cream body, css tokens"
```

---

### Task 2: Implement Block 1 — Header (eyebrow + title + subtitle)

**Files:**
- Modify: `about.html` (inside `<main>`)
- Modify: `assets/css/about.css` (append)

- [ ] **Step 1: Add Header markup to `about.html` inside `<main>`**

Replace `<!-- /about content blocks added in subsequent tasks -->` with:

```html
    <!-- 1. HEADER -->
    <section class="about-header about-section">
      <p class="about-eyebrow">Who We Are</p>
      <h1 class="about-title">Rwanda's Dento-Medical Society</h1>
      <p class="about-subtitle">A nonprofit professional organization uniting dental and medical students and professionals to advance oral and public health across Rwanda and beyond.</p>
    </section>
```

- [ ] **Step 2: Append Header styles to `assets/css/about.css`**

Append:

```css
/* -------- 1. HEADER -------- */

.about-header {
  padding-top: clamp(54px, 7vw, 88px);
  padding-bottom: clamp(40px, 5vw, 56px);
  border-bottom: 1px solid var(--card-border);
}

.about-title {
  font-family: 'Google Sans', sans-serif;
  font-size: clamp(28px, 4vw, 38px);
  line-height: 1.05;
  letter-spacing: -0.01em;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 780px;
  margin: 0;
}

.about-subtitle {
  font-size: clamp(14px, 1.1vw, 15px);
  line-height: 1.5;
  color: var(--text-secondary);
  max-width: 680px;
  margin: 14px 0 0;
}
```

- [ ] **Step 3: Verify in browser**

Reload `about.html` at 1280px.

Expected:
- Eyebrow `WHO WE ARE` appears in dark green, uppercase, letterspaced
- Title `Rwanda's Dento-Medical Society` appears below it, ~38px
- Subtitle below title, ~15px, muted secondary colour
- All three are flush-left
- 1px subtle bottom border separates this from the empty space below

Check at 390px mobile width: text should reflow, no horizontal scroll.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: implement header block (eyebrow + title + subtitle)"
```

---

### Task 3: Implement Block 2 — Vision Banner (full-bleed photo with overlay)

**Files:**
- Modify: `about.html`
- Modify: `assets/css/about.css`

- [ ] **Step 1: Add Vision Banner markup to `about.html` after the Header section**

After the closing `</section>` of `.about-header`, add:

```html
    <!-- 2. VISION BANNER (full-bleed photo + overlay) -->
    <section class="about-vision" aria-labelledby="vision-heading">
      <img class="about-vision__img" src="assets/img/hero-bg-rwanda-vivid.jpg" alt="" aria-hidden="true"/>
      <div class="about-vision__overlay" aria-hidden="true"></div>
      <div class="about-vision__inner">
        <p class="about-eyebrow on-dark">Our Vision</p>
        <h2 class="about-vision__headline" id="vision-heading">Advancing Oral &amp; Public Health Through Innovation and Partnership</h2>
        <p class="about-vision__body">We envision a Rwanda where oral health is recognized as foundational to general well-being &mdash; where every community, regardless of geography or income, has access to preventive care, modern clinical practice, and the research and education that drive both forward. Our work bridges dentistry and medicine, students and professionals, urban centres and rural districts, to make that vision a reality.</p>
      </div>
    </section>
```

- [ ] **Step 2: Append Vision Banner styles**

Append to `assets/css/about.css`:

```css
/* -------- 2. VISION BANNER (full-bleed photo) -------- */

.about-vision {
  position: relative;
  padding: clamp(56px, 8vw, 96px) clamp(20px, 4vw, 36px);
  color: #fff;
  overflow: hidden;
  isolation: isolate;
}

.about-vision__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -2;
}

.about-vision__overlay {
  position: absolute;
  inset: 0;
  background:
    var(--vision-overlay),
    rgba(0, 0, 0, 0.32);
  background-blend-mode: multiply;
  opacity: 0.85;
  z-index: -1;
}

.about-vision__inner {
  max-width: 1200px;
  margin: 0 auto;
}

.about-vision__headline {
  font-family: 'Google Sans', sans-serif;
  font-size: clamp(24px, 3.4vw, 32px);
  line-height: 1.1;
  letter-spacing: -0.01em;
  font-weight: 500;
  color: #fff;
  max-width: 760px;
  margin: 0;
}

.about-vision__body {
  font-size: clamp(13px, 1.05vw, 14px);
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  max-width: 680px;
  margin: 16px 0 0;
}
```

- [ ] **Step 3: Verify in browser**

Reload at 1280px. Expected:
- Full-bleed dark green band below the header
- Background image visible through the overlay (slightly muted, greenish)
- Eyebrow `OUR VISION` in light-green
- Big white headline `Advancing Oral & Public Health Through Innovation and Partnership`
- Body paragraph in muted-white below

At 390px mobile: padding shrinks but overlay + text stay legible.

If the image isn't covering the full band, check `object-fit: cover` and that `position: absolute; inset: 0` is applied.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: vision banner with picture-shaped backdrop"
```

---

### Task 4: Implement Block 3 — Story (2-col with mobile stack)

**Files:**
- Modify: `about.html`
- Modify: `assets/css/about.css`

- [ ] **Step 1: Add Story markup after the Vision Banner**

```html
    <!-- 3. STORY -->
    <section class="about-story about-section">
      <aside class="about-story__label">
        <p class="about-eyebrow">Our Story</p>
        <p class="about-story__meta">Founded 2024 &middot; Ngoma, Huye &middot; Southern Province</p>
      </aside>
      <div class="about-story__body">
        <p>In Rwanda, oral health has long existed at the margins of the national healthcare system &mdash; underfunded, underrepresented, and often invisible to the communities that need it most. Dental disease, though largely preventable, continues to affect children, adults, and vulnerable populations who lack access to even the most basic oral care.</p>
        <p>RDMS was founded in 2024 to confront this reality head-on. Driven by a shared belief that oral health is inseparable from general health, our founders built a society that bridges the gap between dentistry and medicine &mdash; bringing professionals, students, and communities together under one mission.</p>
        <p>Registered under RDB as a Non-Profit Limited by Guarantee (Code: 143885158), RDMS operates from Huye and reaches communities across Rwanda through field programs, research, education, and policy engagement.</p>
      </div>
    </section>
```

- [ ] **Step 2: Append Story styles**

```css
/* -------- 3. STORY -------- */

.about-story {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 48px;
  align-items: start;
  border-bottom: 1px solid var(--card-border);
}

.about-story__label {
  margin: 0;
}

.about-story__meta {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.4;
  margin: 0;
}

.about-story__body {
  max-width: 640px;
  margin: 0;
}

.about-story__body p {
  font-size: 16px;
  line-height: 1.65;
  color: var(--text-body);
  margin: 0 0 18px;
}

.about-story__body p:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .about-story {
    grid-template-columns: 1fr;
    gap: 18px;
  }
}
```

- [ ] **Step 3: Verify in browser**

At 1280px: 2-col layout, label on left (240px), paragraphs on right.
At 390px: single column, label stacks above body, all paragraphs visible.
Story body text is dark grey (`#2a2a2a`), 16px, line-height 1.65.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: story block (2-col with mobile stack)"
```

---

### Task 5: Implement Block 4 — Mission Quote (full-bleed, second photo moment)

**Files:**
- Modify: `about.html`
- Modify: `assets/css/about.css`

- [ ] **Step 1: Add Mission Quote markup after the Story section**

```html
    <!-- 4. MISSION QUOTE (full-bleed photo + overlay) -->
    <section class="about-mission" aria-labelledby="mission-heading">
      <img class="about-mission__img" src="assets/img/doctor4.jpeg" alt="" aria-hidden="true"/>
      <div class="about-mission__overlay" aria-hidden="true"></div>
      <div class="about-mission__inner">
        <p class="about-eyebrow on-dark" id="mission-heading">Our Mission</p>
        <blockquote class="about-mission__quote">&ldquo;To unite dental surgeons, dental therapists, and public health professionals in advancing oral-systemic health through collaborative education, research, outreach, and policy advocacy.&rdquo;</blockquote>
      </div>
    </section>
```

- [ ] **Step 2: Append Mission Quote styles**

```css
/* -------- 4. MISSION QUOTE -------- */

.about-mission {
  position: relative;
  padding: clamp(64px, 9vw, 96px) clamp(20px, 4vw, 36px);
  color: #fff;
  overflow: hidden;
  isolation: isolate;
}

.about-mission__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -2;
}

.about-mission__overlay {
  position: absolute;
  inset: 0;
  background:
    var(--mission-overlay),
    rgba(0, 0, 0, 0.40);
  background-blend-mode: multiply;
  opacity: 0.88;
  z-index: -1;
}

.about-mission__inner {
  max-width: 1200px;
  margin: 0 auto;
}

.about-mission__quote {
  font-family: Georgia, 'Times New Roman', serif;
  font-style: italic;
  font-weight: 400;
  font-size: clamp(20px, 2.4vw, 26px);
  line-height: 1.4;
  color: #fff;
  max-width: 820px;
  margin: 24px 0 0;
  padding: 0;
}
```

- [ ] **Step 3: Verify in browser**

At 1280px: dark band below Story. Photo backdrop visible through dark overlay (heavier than Vision Banner). Eyebrow `OUR MISSION` in light-green; serif italic quote with curly quotes, flush-left, max-width ~820px.

At 390px: padding shrinks, text reflows, still readable.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: mission quote block (serif pull-quote on photo backdrop)"
```

---

### Task 6: Implement Block 5 — Info Cards (Where / Who / Reach)

**Files:**
- Modify: `about.html`
- Modify: `assets/css/about.css`

- [ ] **Step 1: Add Info Cards markup after the Mission Quote section**

```html
    <!-- 5. INFO CARDS -->
    <section class="about-info about-section">
      <div class="about-info__grid">
        <article class="about-info__card">
          <div class="about-info__icon" aria-hidden="true">📍</div>
          <h3 class="about-info__title">Where We Operate</h3>
          <p class="about-info__body">Headquartered in Ngoma, Huye (Southern Province), RDMS conducts programs across Rwanda &mdash; from urban clinics and university campuses to rural schools and underserved communities.</p>
        </article>
        <article class="about-info__card">
          <div class="about-info__icon" aria-hidden="true">🤝</div>
          <h3 class="about-info__title">Who We Bring Together</h3>
          <p class="about-info__body">Our members include dental surgeons, dental therapists, medical doctors, public health professionals, and students from across Rwanda's health sciences community &mdash; all united by one purpose.</p>
        </article>
        <article class="about-info__card">
          <div class="about-info__icon" aria-hidden="true">🌍</div>
          <h3 class="about-info__title">Our Reach</h3>
          <p class="about-info__body">While rooted in Rwanda, RDMS engages with global oral health networks, international awareness days, and cross-border partnerships &mdash; contributing to healthcare advancement beyond Rwanda's borders.</p>
        </article>
      </div>
    </section>
```

- [ ] **Step 2: Append Info Cards styles**

```css
/* -------- 5. INFO CARDS -------- */

.about-info {
  border-bottom: 1px solid var(--card-border);
}

.about-info__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.about-info__card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.about-info__icon {
  font-size: 22px;
  line-height: 1;
  margin-bottom: 10px;
}

.about-info__title {
  font-family: 'Google Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px;
}

.about-info__body {
  font-size: 13px;
  line-height: 1.55;
  color: var(--text-secondary);
  margin: 0;
}

@media (max-width: 768px) {
  .about-info__grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 3: Verify in browser**

At 1280px: 3 white cards in a row on cream, each with emoji top-left, title, body. Cards have subtle border and tiny shadow.

At 390px: cards stack vertically, full-width.

Emoji rendering: depends on OS. Acceptable.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: 3-up info cards (where/who/reach)"
```

---

### Task 7: Implement Block 6 — Values (5-entry numbered manifesto)

**Files:**
- Modify: `about.html`
- Modify: `assets/css/about.css`

- [ ] **Step 1: Add Values markup after the Info Cards section**

```html
    <!-- 6. VALUES -->
    <section class="about-values about-section">
      <p class="about-eyebrow">What Guides Us</p>
      <h2 class="about-values__title">Our Core Values</h2>
      <ol class="about-values__list">
        <li class="about-values__item">
          <span class="about-values__num" aria-hidden="true">01</span>
          <div class="about-values__content">
            <h3 class="about-values__name">Transparency &amp; Accountability</h3>
            <p class="about-values__desc">We operate with openness in all our activities &mdash; from governance and finance to research and community engagement. Trust is the foundation of everything we do.</p>
          </div>
        </li>
        <li class="about-values__item">
          <span class="about-values__num" aria-hidden="true">02</span>
          <div class="about-values__content">
            <h3 class="about-values__name">Teamwork &amp; Collaboration</h3>
            <p class="about-values__desc">Progress in oral health requires collective effort. We unite professionals across disciplines, institutions, and borders to achieve outcomes no single actor could accomplish alone.</p>
          </div>
        </li>
        <li class="about-values__item">
          <span class="about-values__num" aria-hidden="true">03</span>
          <div class="about-values__content">
            <h3 class="about-values__name">Selflessness &amp; Compassion</h3>
            <p class="about-values__desc">Our work is driven by genuine care for the communities we serve. We place patients and populations at the heart of every decision we make.</p>
          </div>
        </li>
        <li class="about-values__item">
          <span class="about-values__num" aria-hidden="true">04</span>
          <div class="about-values__content">
            <h3 class="about-values__name">Equity &amp; Equality</h3>
            <p class="about-values__desc">Quality oral healthcare is a right, not a privilege. We actively work to eliminate disparities &mdash; ensuring geography, income, or background never determines the care someone receives.</p>
          </div>
        </li>
        <li class="about-values__item about-values__item--span-half">
          <span class="about-values__num" aria-hidden="true">05</span>
          <div class="about-values__content">
            <h3 class="about-values__name">Human Rights &amp; Environment</h3>
            <p class="about-values__desc">We uphold the dignity and rights of every individual we serve, and recognise that human health and environmental health are deeply interconnected.</p>
          </div>
        </li>
      </ol>
    </section>
```

- [ ] **Step 2: Append Values styles**

```css
/* -------- 6. VALUES -------- */

.about-values {
  border-bottom: 1px solid var(--card-border);
}

.about-values__title {
  font-family: 'Google Sans', sans-serif;
  font-size: clamp(24px, 3.2vw, 30px);
  line-height: 1.05;
  letter-spacing: -0.01em;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 0 36px;
}

.about-values__list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px 48px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.about-values__item {
  display: flex;
  gap: 18px;
  align-items: flex-start;
}

/* Item 5: span column 1 of row 3 only — left half, intentionally asymmetric */
.about-values__item--span-half {
  grid-column: 1 / span 1;
}

.about-values__num {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 32px;
  font-weight: 300;
  line-height: 1;
  color: var(--green-on-light);
  flex: none;
  min-width: 48px;
}

.about-values__name {
  font-family: 'Google Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px;
}

.about-values__desc {
  font-size: 13px;
  line-height: 1.55;
  color: var(--text-secondary);
  margin: 0;
}

@media (max-width: 768px) {
  .about-values__list {
    grid-template-columns: 1fr;
  }
  .about-values__item--span-half {
    grid-column: auto;
  }
}
```

- [ ] **Step 3: Verify in browser**

At 1280px: 2-col grid. Items 1–4 fill rows 1 + 2. Item 5 sits in row 3 column 1 only (left half). Each has a thin serif numeral (01–05) in dark green to the left, and a bold name + grey description on the right.

At 390px: single column, all 5 items stack.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: values block (5-entry numbered manifesto, 2-col with asymmetric last)"
```

---

### Task 8: Implement Block 7 — Credibility band (dark closer)

**Files:**
- Modify: `about.html`
- Modify: `assets/css/about.css`

- [ ] **Step 1: Add Credibility band markup after the Values section**

```html
    <!-- 7. CREDIBILITY BAND -->
    <section class="about-credibility" aria-labelledby="credibility-heading">
      <div class="about-credibility__inner">
        <p class="about-eyebrow on-accent" id="credibility-heading">RDMS at a Glance</p>
        <div class="about-credibility__kpis">
          <div class="about-credibility__kpi">
            <p class="about-credibility__label">Founded</p>
            <p class="about-credibility__value">1 July 2024</p>
          </div>
          <div class="about-credibility__kpi">
            <p class="about-credibility__label">RDB Code</p>
            <p class="about-credibility__value">143885158</p>
          </div>
          <div class="about-credibility__kpi">
            <p class="about-credibility__label">Headquarters</p>
            <p class="about-credibility__value">Ngoma, Huye</p>
          </div>
          <div class="about-credibility__kpi">
            <p class="about-credibility__label">Members</p>
            <p class="about-credibility__value">30+</p>
          </div>
        </div>
        <ul class="about-credibility__facts">
          <li><span aria-hidden="true">📞</span> +250 791 853 120</li>
          <li><span aria-hidden="true">📍</span> Southern Province, Rwanda</li>
          <li>5+ Core Services</li>
        </ul>
      </div>
    </section>
```

- [ ] **Step 2: Append Credibility band styles**

```css
/* -------- 7. CREDIBILITY BAND -------- */

.about-credibility {
  background: var(--dark-band);
  color: #fff;
  padding: clamp(40px, 6vw, 56px) clamp(20px, 4vw, 36px);
}

.about-credibility__inner {
  max-width: 1200px;
  margin: 0 auto;
}

/* Eyebrow variant on the dark band uses the existing site green accent */
.about-eyebrow.on-accent {
  color: var(--green-accent);
}

.about-credibility__kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.about-credibility__kpi {
  margin: 0;
}

.about-credibility__label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 4px;
}

.about-credibility__value {
  font-family: 'Google Sans', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.about-credibility__facts {
  list-style: none;
  padding: 24px 0 0;
  margin: 24px 0 0;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.75);
}

.about-credibility__facts li {
  margin: 0;
}

@media (max-width: 768px) {
  .about-credibility__kpis {
    grid-template-columns: 1fr 1fr;
  }
}
```

- [ ] **Step 3: Verify in browser**

At 1280px: dark band below Values, just before the global footer. Eyebrow `RDMS AT A GLANCE` in bright green. 4 KPIs in a row. Dim divider line, then 3 supplementary facts in a flex row.

At 390px: KPIs become 2×2 grid, supplementary facts wrap to multiple lines.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/about.css
git commit -m "About page: credibility band (dark closer with KPIs + facts)"
```

---

### Task 9: Add scroll-reveal animations + reduced-motion support

**Files:**
- Create: `assets/js/about.js`
- Modify: `assets/css/about.css` (append animation rules)

- [ ] **Step 1: Create `assets/js/about.js`**

```js
/* /about page scroll-reveal — IntersectionObserver with reduced-motion. */
(function () {
  'use strict';

  var prefersReduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var targets = document.querySelectorAll(
    '.about-header, .about-vision__inner, .about-story__label, ' +
    '.about-story__body, .about-mission__inner, .about-info__card, ' +
    '.about-values__title, .about-values__item, .about-credibility__inner'
  );

  if (prefersReduced || !('IntersectionObserver' in window)) {
    // No animation: mark everything visible immediately.
    targets.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

  targets.forEach(function (el) { observer.observe(el); });
})();
```

- [ ] **Step 2: Append reveal animation rules to `assets/css/about.css`**

```css
/* -------- Scroll reveal (paired with assets/js/about.js) -------- */

.about-header,
.about-vision__inner,
.about-story__label,
.about-story__body,
.about-mission__inner,
.about-info__card,
.about-values__title,
.about-values__item,
.about-credibility__inner {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 600ms ease-out, transform 600ms ease-out;
}

.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger value items slightly so they cascade in. */
.about-values__item:nth-child(1) { transition-delay: 0ms; }
.about-values__item:nth-child(2) { transition-delay: 80ms; }
.about-values__item:nth-child(3) { transition-delay: 160ms; }
.about-values__item:nth-child(4) { transition-delay: 240ms; }
.about-values__item:nth-child(5) { transition-delay: 320ms; }

/* Stagger info cards. */
.about-info__card:nth-child(1) { transition-delay: 0ms; }
.about-info__card:nth-child(2) { transition-delay: 100ms; }
.about-info__card:nth-child(3) { transition-delay: 200ms; }

/* Reduced motion — hard reset. */
@media (prefers-reduced-motion: reduce) {
  .about-header,
  .about-vision__inner,
  .about-story__label,
  .about-story__body,
  .about-mission__inner,
  .about-info__card,
  .about-values__title,
  .about-values__item,
  .about-credibility__inner {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

- [ ] **Step 3: Verify in browser**

Reload `about.html` and scroll from top to bottom slowly. Each block should fade-in + slide-up by ~24px when it enters the viewport. Info cards and Value items should cascade with a slight stagger.

Then in DevTools, toggle "Emulate CSS prefers-reduced-motion: reduce" (Rendering tab). Reload the page. Everything should be visible immediately with no transform animation.

If a block stays invisible: confirm it's in the JS selector list and that `assets/js/about.js` is loading (check Network tab).

- [ ] **Step 4: Commit**

```bash
git add assets/js/about.js assets/css/about.css about.html
git commit -m "About page: scroll-reveal animations with reduced-motion support"
```

---

### Task 10: Refresh homepage `#about` teaser + fix `/about` nav links

**Files:**
- Modify: `index.html`
- Modify: `local-overrides.css`

- [ ] **Step 1: Replace the existing `.about-container` desktop block in `index.html`**

Find lines ~265–270 in `index.html` (the `<div class="w-layout-blockcontainer about-container desktop w-container" id="about">` block) and replace the entire block with:

```html
  <!-- ============================
       ABOUT TEASER — Desktop
       Short hook on the homepage. Long-form content lives on /about.html.
  ============================= -->
  <div class="w-layout-blockcontainer about-container desktop about-teaser w-container" id="about">
    <p class="eyebrow light what-is-techish">About RDMS</p>
    <h2 class="about-teaser__title">Uniting dental and medical professionals for healthier communities.</h2>
    <p class="about-teaser__body">RDMS Rwanda is a nonprofit professional society advancing oral and public health through education, research, and outreach. Founded in 2024 in Ngoma, Huye, we bring dental surgeons, therapists, doctors, and students together under one mission.</p>
    <a href="about.html" class="rdms-cta secondary about-teaser__cta">Read our story <span class="arrow">&rarr;</span></a>
  </div>
```

- [ ] **Step 2: Replace the existing `.about-container.mobile` block in `index.html`**

Find lines ~273–277 (the `<div class="w-layout-blockcontainer about-container mobile w-container">` block) and replace with:

```html
  <!-- ABOUT TEASER — Mobile -->
  <div class="w-layout-blockcontainer about-container mobile about-teaser w-container">
    <p class="eyebrow light what-is-techish">About RDMS</p>
    <h2 class="about-teaser__title">Uniting dental and medical professionals for healthier communities.</h2>
    <p class="about-teaser__body">RDMS Rwanda is a nonprofit professional society advancing oral and public health through education, research, and outreach. Founded in 2024 in Ngoma, Huye, we bring dental surgeons, therapists, doctors, and students together under one mission.</p>
    <a href="about.html" class="rdms-cta secondary about-teaser__cta">Read our story <span class="arrow">&rarr;</span></a>
  </div>
```

- [ ] **Step 3: Update the two `/about` links in `index.html`**

Find line ~192:

```html
<a href="/about" class="nav-link w-nav-link">About</a>
```

Change to:

```html
<a href="about.html" class="nav-link w-nav-link">About</a>
```

Find line ~417 (in the footer):

```html
<a href="/about" class="link-3">About</a>
```

Change to:

```html
<a href="about.html" class="link-3">About</a>
```

- [ ] **Step 4: Append teaser styles to `local-overrides.css`**

Append at the end of `local-overrides.css`:

```css
/* ---------------------------------------------------------------
   ABOUT TEASER (homepage) — refresh of the legacy .about-container
   block. Sits over the dark hero video on mobile and over the dark
   hero gradient on desktop, so all text is white and the CTA uses
   the existing .rdms-cta.secondary glassmorphic styling.
   --------------------------------------------------------------- */

.about-teaser__title {
  font-family: 'Google Sans', sans-serif;
  font-size: clamp(24px, 3.4vw, 36px);
  line-height: 1.1;
  letter-spacing: -0.01em;
  font-weight: 500;
  color: #fff;
  margin: 16px 0 14px;
  max-width: 720px;
  text-align: left;
}

.about-teaser__body {
  font-family: 'Google Sans', sans-serif;
  font-size: clamp(14px, 1.1vw, 16px);
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  max-width: 640px;
  margin: 0 0 22px;
  text-align: left;
}

.about-teaser__cta {
  /* Inherits .rdms-cta.secondary base; this just locks alignment. */
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.about-teaser__cta .arrow {
  display: inline-block;
  transition: transform 0.25s ease;
}

.about-teaser__cta:hover .arrow {
  transform: translateX(3px);
}
```

- [ ] **Step 5: Verify in browser**

Reload `file:///d:/Claude/Rwanda/index.html` at 1280px.

Expected:
- Below the hero, the about block now shows: eyebrow `ABOUT RDMS`, white title (~36px) starting "Uniting dental and medical professionals…", muted-white body, and a "Read our story →" pill button.
- All text flush-left.
- Button hover: arrow nudges right.
- Click "Read our story →" → loads `about.html` correctly.
- Click navbar `About` link → loads `about.html`.
- Scroll to footer, click `About` link → loads `about.html`.

At 390px mobile: same content, scaled down typography. No horizontal scroll.

- [ ] **Step 6: Commit**

```bash
git add index.html local-overrides.css
git commit -m "Homepage: replace about block with teaser, fix /about nav + footer links"
```

---

### Task 11: Final responsive QA across `about.html` and `index.html`

**Files:** none (verification only — no code changes unless bugs found)

- [ ] **Step 1: Desktop pass on `about.html`**

Open `about.html` at 1280px. Scroll top to bottom. Check:
- Header → cream, dark text, eyebrow + title + subtitle stacked
- Vision Banner → full-bleed dark, white headline + body legible
- Story → 2-col, label left, body right
- Mission Quote → full-bleed dark, serif italic flush-left
- Info Cards → 3 white cards in a row
- Values → 2-col grid, item 5 left-half
- Credibility band → dark, 4 KPIs in a row, supplementary facts below
- Footer → unchanged from homepage

All transitions feel calm; nothing pops or jolts.

- [ ] **Step 2: Tablet pass at 768px**

Resize to 768px. Check:
- Story still 2-col? (it should — breakpoint is `<768px`, so 768px exactly is desktop)
- Info cards: 3-up still or stacked?
- Values: 2-col still?
- Credibility KPIs: still 4-up?

- [ ] **Step 3: Mobile pass at 390px**

Resize to 390px. Check:
- Story stacks (label on top, body below)
- Info cards stack (single column)
- Values stack (single column, all 5)
- Credibility KPIs become 2×2 grid
- No horizontal scroll on any block
- Vision Banner + Mission Quote backdrops still cover, text still legible

- [ ] **Step 4: Reduced-motion pass**

In DevTools → Rendering tab, toggle `Emulate CSS prefers-reduced-motion: reduce`. Reload `about.html`. All sections should be visible immediately with no transform animation.

- [ ] **Step 5: Link integrity**

From `index.html`:
- Click navbar **About** → loads `about.html` ✓
- Click footer **About** → loads `about.html` ✓
- Click homepage teaser **Read our story →** → loads `about.html` ✓

From `about.html`:
- Click navbar **About** (already on /about) → reloads `about.html` ✓
- Click footer **About** → reloads `about.html` ✓
- Click brand logo or footer brand link → returns to `index.html` ✓

- [ ] **Step 6: HTML sanity**

Open `about.html` source in browser, run `Ctrl+U` (View Source). Confirm:
- Single `<h1>` (the page Header title)
- All `<section>` elements have either `aria-labelledby` or a heading inside
- All decorative `<img>` have `alt=""` and `aria-hidden="true"`
- No leftover placeholder comments like `PASTE INDEX.HTML LINES…`

- [ ] **Step 7: Commit any QA fixes**

If you found and fixed any bugs in steps 1–6, commit them now:

```bash
git add -p
git commit -m "About page: QA fixes from final responsive pass"
```

If no bugs: skip the commit; the work is done.

---

## Done

The `/about.html` page is live, the homepage `#about` teaser links into it, and both navbar + footer About links point at the new file. No automated tests because none exist in this project; manual browser verification at 3 widths + reduced-motion is the verification contract.
