# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project shape

This is a **static HTML / CSS / vanilla JS marketing site** for RDMS — Dento-Medical Society Rwanda. There is no build step, no bundler, no test runner, no React, no TypeScript, no Tailwind, no shadcn, no npm dependency tree for the site itself. Every page is shipped exactly as authored. Treat any request to "drop in a React component" or "add a TypeScript file" as a stack mismatch — flag it and propose a vanilla port.

The codebase began as a clone of the Tech-ish Webflow template (originally `tech-ish.org`, a Kenyan tech blog) and is being rebranded section-by-section into RDMS. Webflow's runtime, classnames, and IX hooks are still scattered through the markup. **Read the layering note below before editing any CSS.**

## Documentation hierarchy (read these before designing)

- `PRODUCT.md` — audience, brand voice, anti-aesthetics ("must NOT look like white-savior NGO / generic healthcare / tech-startup template / Africa-stock-photo / templated AI-generated"). Treat its anti-references as hard constraints.
- `DESIGN.md` + `DESIGN.json` — visual system: cream + green + dark-navy palette, typography, component tokens. Use the named tokens (e.g. `cream-paper #f6f3ec`, `cooperative-green #58cc6f`, `band-dark #0a0a0a`) rather than inventing new ones.
- `docs/superpowers/specs/` and `docs/superpowers/plans/` — design specs and implementation plans for completed work (the cream-palette /about page is the worked example).
- `.agents/skills/impeccable/` — Impeccable design skill installed. Invoke via `/impeccable <command> [target]` for shape, craft, critique, audit, polish, bolder, quieter, distill, and friends. Setup gates require PRODUCT.md (present) and DESIGN.md (present). Register = `brand` (declared in PRODUCT.md). The skill has its own `reference/` library; load only the command reference you need.

## File map (the parts that need explaining)

```
index.html                 Homepage — Hero → About (7 inlined blocks) → Leadership →
                           Three Pillars (3-col scroll) → Services → Projects →
                           Research Academy → Contact → Footer.
about.html                 Cream-palette /about page. Orphan: nothing in the
                           navigation links to it anymore. Kept on disk as a
                           deeper-cut design reference.
local-overrides.css        ALL custom RDMS styling for the homepage. ~3,400 lines,
                           organized by section with /* === SECTION NAME === */
                           banners. Loaded AFTER assets/css/webflow.css so its
                           rules win cascade conflicts.
assets/css/webflow.css     Vendor: Webflow's exported stylesheet. DO NOT EDIT.
                           Override in local-overrides.css instead.
assets/css/about.css       Cream-palette page styles for about.html only. Not
                           loaded on index.html.
script.js                  Vanilla JS for the homepage: GSAP/ScrollTrigger animations,
                           the Get-In-Touch overlay, contact-form mailto submit,
                           Projects filter tabs, scroll-collapse navbar, mobile
                           menu, reveal-on-scroll. Multiple IIFEs, one per concern.
assets/js/about.js         IntersectionObserver scroll-reveal for about.html.
assets/img/                Site assets. Optimized variants (bg-*.jpg, team-*.jpeg,
                           column-scroll-*.jpg, about-*.png, rdms-logo.png) are
                           what the HTML references. The full-resolution sources
                           (RDMS (n).png, named portraits, WhatsApp Image*, the
                           logo/ folder, rwanda-flag.png) are tracked but only
                           used for re-derivation.
optimize_images.py         Compresses anything >30 KB in assets/img/ in-place.
extract_css.py             One-shot tool used during the original Webflow clone.
                           Not part of normal workflow.
download_assets.py         One-shot tool. Same.
generate_report.py         Generates a clone report. Not used.
verify.py                  Quick smoke test: hits http://localhost:8080/ and
                           checks key asset paths render.
```

## Running and verifying locally

There is no `npm start`. Serve any static way you like; the project's `verify.py` expects port 8080:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/` in a browser. `python verify.py` against a running server confirms key asset paths resolve.

For asset compression after adding images:

```bash
python optimize_images.py
```

## Architectural conventions to respect

**1. Webflow layering is sacred.** `webflow.css` is loaded first; `local-overrides.css` is loaded second; per-page overrides win. Don't edit `webflow.css` — it's vendor. The Webflow runtime (`assets/js/webflow.*.js`, jQuery, GSAP, ScrollTrigger) handles the IX2/IX3 animation system; many DOM elements have `data-w-id` attributes that Webflow uses internally. Leave those attributes alone even if they look noisy.

**2. The contact overlay opener pattern.** A single Get-In-Touch overlay (`.get-in-touch-overlay`) is opened by *many* buttons across the site. The mechanism is a hard-coded ID list in `script.js`:

```js
var openers = [
  document.getElementById('getInTouchNavBtn'),
  document.getElementById('footerConnectBtn'),
  document.getElementById('sponsorGetInTouchBtn'),
  document.getElementById('servicesCtaBtn'),
  document.getElementById('academyJoinBtn'),
  document.getElementById('chroniclesSubscribeBtn'),
  // …
];
```

To wire a new "Contact" / "Get In Touch" / "Subscribe" button to the overlay, add an `id` to the link and append it to this array. The `if (el)` guard means stale entries (where the element no longer exists) are safe.

**3. Contact form has no backend.** The `<form id="contactForm">` in the Contact section uses `mailto:` via JS. On submit, `script.js` builds a `mailto:` URL with the form fields URL-encoded into the body and opens the visitor's mail client. Recipients are hard-coded (`rdmspresident13@gmail.com`, `igisubizojimmy@gmail.com`). **There is no server endpoint.** If a request asks you to "submit form to backend", flag the gap and propose an external service (Formspree, Netlify Forms, Google Forms) or extend the existing mailto pattern — don't fabricate an API.

**4. Photo backdrop pattern.** Sections that use a photo as a background follow this layout:

```html
<section class="services">
  <img class="services__bg-img reveal-photo" src="…" alt="" aria-hidden="true"/>
  <div class="services__bg-overlay" aria-hidden="true"></div>
  <div class="services__inner">…</div>
</section>
```

CSS uses `position: absolute; inset: 0; z-index: -2` for the image, `z-index: -1` for the overlay, plus `position: relative; isolation: isolate` on the section. The `.reveal-photo` class enables fade-in + slight-zoom on first scroll into viewport (IntersectionObserver in `script.js`). Vision Banner and Mission Quote photos additionally get a slow Ken Burns animation via the `kenBurns` keyframes.

**5. Adding a new photo asset.** Sources and optimized variants both live in `assets/img/`. The HTML always references the optimized variant. Workflow:
1. Drop the source image into `assets/img/`. Use kebab-case filenames (`my-photo.jpg`); avoid spaces and parentheses (Webflow / URL encoding pain).
2. Resize to ≤1400px on the long edge, JPEG quality 82, progressive. Use `optimize_images.py` (compresses anything ≥30 KB) or a one-off Python + Pillow script.
3. Save the optimized variant under a semantic name: `bg-services.jpg` for backdrops, `team-jane-doe.jpeg` for portraits, `column-scroll-1.jpg` for sticky-image scroll panels.
4. Reference the optimized variant in HTML; never reference the source directly.
5. If it's a backdrop, use the `__bg-img` + `__bg-overlay` pattern from convention 4.

**6. The two-mode visual system.**
- **Homepage (`index.html`)**: dark / transparent / glassmorphic. Most sections sit transparent over the fixed hero video, with frosted-glass cards (`background: rgba(15,15,18,0.55) + backdrop-filter: blur(14px) + 1px white-tint border`). Photo bands punctuate.
- **About page (`about.html`)**: cream / light. Editorial typographic system. Different palette and class namespace (`.about-*` vs `.home-about-*`).

Class naming is BEM-ish (`.block__element` / `.block__element--modifier`). Homepage about classes are namespaced `home-about-*` to avoid collision with about.html's `about-*`.

**7. Mobile navigation.** Below 768px, the inline nav is hidden and a hamburger button reveals a slide-from-right overlay (`.mobile-menu`). Both `index.html` and `about.html` have the panel markup. Toggle logic + close-on-Esc/backdrop/link-click is the last IIFE in `script.js`.

**8. Sticky navbar / collapse-on-scroll.** The navbar sits at body root (NOT inside `.hero`) so `position: fixed` is anchored to the viewport regardless of GSAP transforms applied to hero descendants. At ≥992px, scrolling down past 150px collapses the pill to a 56px circle showing a hamburger; scrolling up 80px expands it back. Click the circle to expand manually. Below 992px this collapse logic is disabled — mobile uses the hamburger overlay instead.

**9. The `assets/img/logo/` folder** holds the original RDMS logo source plus partner-organization logos (CHUB, FIRAH, Hanga Hubs, etc.) for future partnership sections. Not currently rendered.

**10. Motion conventions.** All decorative motion honors `prefers-reduced-motion: reduce` (transitions/animations disabled or zeroed). Five named patterns:
- **Ken Burns** — slow infinite zoom/pan on Vision Banner + Mission Quote photos. CSS `@keyframes kenBurns`, ~22s ease-in-out, scale 1.02→1.08 with slight drift.
- **Reveal-on-scroll** — `.reveal-photo` class. IntersectionObserver in `script.js` adds `.is-visible` on entry; CSS does opacity 0→1 + scale 0.96→1, 700ms ease-out.
- **Hover-pop on photos** — Leadership team-card photos lift 10px on `:hover` with a green outer glow. Triggered on the `<img>` itself, not the parent card.
- **Collapse-on-scroll navbar** — desktop only (≥992px). Spring-ish `cubic-bezier(0.34, 1.56, 0.64, 1)` on width / position / border-radius.
- **Mobile-menu slide** — slide-from-right overlay, 320ms with the same overshoot easing.

When adding new motion: keep durations 200–700ms, ease-out family, no bounce/elastic, never animate CSS layout properties (use `transform` / `opacity`).

## Project-specific rules (from `~/.claude/projects/d--Claude-Rwanda/memory/`)

- **Flush-left text alignment, ALL viewports.** All titles, headings (h1–h6), eyebrows, body copy, pull-quotes, info-card descriptions, value descriptions, captions, footer credits must be `text-align: left` on **both desktop and mobile**. No centered or justified text in any responsive breakpoint. When a layout collapses to single-column on mobile, audit the mobile rule for `text-align: center` / `align-items: center` / `justify-items: center` and replace with left alignment. When porting third-party components (React / shadcn / Tailwind) that use `text-center` or `items-center` for typography, flip those to left in the vanilla port. Exception only if the user explicitly requests centered alignment for a specific element. Numerical stats grids and KPI tiles may keep left-aligned numbers (no need to center digits inside their cell). Reason: machine-readability for AI scrapers, screen readers, and content-extraction pipelines.

- **Default to clarifying-questions + sparring-partner mode.** For every non-trivial request on this project, behave as if the user appended *"Ask me clarifying questions until you are 95% confident you can complete the task successfully. Be my sparring partner — identify my blind spots, risks & assumptions."* Lead with concise concerns, then 3–5 focused questions (multiple-choice when reasonable). Skip on trivial / risk-free changes (typo fixes, renames, removing comments) and when the user says "just do it" or already supplied the answers.

## Anti-patterns (from PRODUCT.md, summarized)

- White-savior NGO aesthetic (sad-children photography, "your $5 saves a life", hand-on-shoulder stock).
- Generic healthcare blue-and-teal SaaS-clinic look.
- Tech-startup template moves (gradient hero text, hero-metric KPIs, identical 3-up icon-card grids).
- Africa-stock-photo (baobab-trees-at-sunset, generic-Africa imagery without Rwanda specificity).
- Templated / AI-generated look (glassmorphism-because-it-feels-modern, symmetric hero-grid-CTA-grid-footer).

The current site uses glassmorphism heavily on the homepage. PRODUCT.md flags that as a known tension: the design is in transition from template to bespoke. New work should lean toward `PRODUCT.md`'s "modern-African, not template-modern" direction rather than amplifying the existing glass-card vocabulary.

## Branching and the orphan /about

- `main` is the live branch. Two feature branches (`feat/about-page`, `feat/services`) survive on origin as historical breadcrumbs and are kept around per the user's preference.
- `about.html` is no longer linked from any navigation (the homepage has the same content inlined under `#about`). It survives on disk; deleting it is fine if you confirm with the user.

## Working tree hygiene

Some local files are NOT meant to be committed. `git status` will keep showing them as untracked:

- `.agents/` — Impeccable skill local state
- `new 1.txt`, `new 2.txt` — scratch notes
- `skills-lock.json` — Claude Code skill cache

Don't `git add` any of these. The `.gitignore` already covers `.claude/`, `.superpowers/`, `content.txt`, `preview-hero.html`, `__pycache__/`, OS junk, and the unreferenced `kling_*.mp4` source videos. When committing changes, prefer `git add <specific paths>` over `git add .` so untracked scratch files don't sneak in.
