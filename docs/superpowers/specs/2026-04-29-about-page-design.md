# /about page + homepage teaser — design spec

**Date:** 2026-04-29
**Project:** RDMS Rwanda site (`d:/Claude/Rwanda`)
**Scope:** New dedicated `/about.html` page, plus a refresh of the homepage `#about` block to act as a teaser linking into it.

---

## 1. Decisions made (from brainstorming)

| # | Decision | Choice |
|---|---|---|
| Q1 | Where the long-form content lives | **C** — new `/about.html` page **and** refreshed homepage teaser linking to it |
| Q2 | Overall palette for `/about` | **B** — all-light / cream, with two photographic dark-overlay bands as visual interludes |
| Q3 | Vision Banner vs Header redundancy | **B** — Vision Banner is rewritten with vision-forward copy; no longer restates the org description |
| Q4 | Imagery strategy | **C** — strategic / hybrid: two photo moments only (Vision Banner + Mission Quote backdrops); story and cards stay typographic. Better photography is coming, so picture-shaped containers must be ready to swap art later |
| Q5 | Page-top photo placement | **B** — typographic header opens the page; Vision Banner (block 2) carries the first photo moment |
| Q6 | Value 6 + registration metadata | **C** — drop Value 6 from the values grid; consolidate RDB code, founding date, location, phone, member count, services into a single "Credibility band" at the page bottom. Values become 5 |
| Q7 | Full-page wireframe v2 | Approved as-shown, with one correction: **all text flush-left** (project-wide rule, saved to memory) |

---

## 2. Block sequence (top to bottom)

1. **Header** — eyebrow + title + subtitle (typographic, cream)
2. **Vision Banner** — eyebrow + headline + tightened paragraph (full-bleed photo + dark overlay, white text)
3. **Story** — heading + 3 paragraphs (cream, two-column layout)
4. **Mission Quote** — label + serif italic pull-quote (full-bleed photo + dark overlay, white text)
5. **Info Cards** — Where We Operate / Who We Bring Together / Our Reach (3-up grid on cream)
6. **Values** — eyebrow + title + 5 numbered manifesto entries (2-col, cream)
7. **Credibility band** — RDMS at a Glance: founded, RDB code, HQ, members, phone, location, services (dark closer band)

---

## 3. Visual system

### Palette

| Token | Value | Use |
|---|---|---|
| `--cream-bg` | `#f6f3ec` | Page background, Header, Story, Info Cards section, Values section |
| `--cream-tint` | `#ece6d6` | Optional tinted band (kept available; unused in v2) |
| `--card-bg` | `#ffffff` | Info card surfaces |
| `--card-border` | `#e3ddd1` | Card + divider borders |
| `--text-primary` | `#0a0a0a` | Headings on cream |
| `--text-body` | `#2a2a2a` | Story paragraphs |
| `--text-secondary` | `#4a4a4a` | Card descriptions, value descriptions |
| `--text-muted` | `#7a7a7a` | Story label sub-meta |
| `--green-on-light` | `#1f6b3a` | Eyebrows + value numerals on cream |
| `--green-on-dark` | `#a9e0b6` | Eyebrows on dark photo bands |
| `--green-accent` | `#58cc6f` | Credibility band eyebrow (matches existing site accent) |
| `--vision-overlay` | `linear-gradient(135deg,#1c3a2c,#3d6b52)` | Vision Banner photo overlay (placeholder until photo arrives) |
| `--mission-overlay` | `linear-gradient(135deg,#3d3a32,#1f1d18)` | Mission Quote photo overlay (placeholder until photo arrives) |
| `--dark-band` | `#0a0a0a` | Credibility band background |

### Typography

Existing site already loads Google Sans, Google Sans Flex, Montserrat, Allison. The /about page uses:

- **Eyebrows** — Google Sans, 11px, uppercase, letter-spacing .18em, `--green-on-light` (or `--green-on-dark`)
- **Headings (Header title, Vision headline, Values title)** — Google Sans, fluid `clamp(28px, 4vw, 38px)`, weight 500, letter-spacing -.01em, line-height 1.05
- **Story body** — Google Sans, 16px, line-height 1.65, `--text-body`, max-width 640px
- **Mission Quote** — Georgia (serif fallback), italic, fluid `clamp(20px, 2.4vw, 26px)`, line-height 1.4, max-width 820px
- **Value numerals (01–05)** — Georgia (serif fallback), 32px, weight 300, `--green-on-light`
- **Card title** — Google Sans, 15px, weight 600
- **Card body** — Google Sans, 13px, line-height 1.55, `--text-secondary`

### Alignment rule

**All text on the page is flush-left** (`text-align: left`). Project-wide rule, no exceptions on /about. Numerals/icons inside grid cells may be naturally placed.

### Containers + spacing

- Page max-width: `1200px` centered, page horizontal padding `clamp(20px, 4vw, 36px)`
- Section vertical padding: `clamp(48px, 7vw, 80px)` top/bottom for content sections; Vision and Mission bands use `clamp(56px, 8vw, 96px)`
- Inter-section dividers: 1px `--card-border` (between cream sections only — photo bands and dark band have their own visual separation)

---

## 4. Block-by-block spec

### 4.1 Header

- Single block on cream
- Eyebrow: `Who We Are`
- Title: `Rwanda's Dento-Medical Society` — large, max-width 780px
- Subtitle: existing copy — max-width 680px

### 4.2 Vision Banner

- Full-bleed (page edge to page edge), padding `clamp(56px, 8vw, 96px)` × `clamp(20px, 4vw, 36px)`
- Background: `<img>` placeholder (use `assets/img/hero-bg-rwanda-vivid.jpg` until better photo arrives) + `--vision-overlay` gradient at 70% opacity over the image, plus a `rgba(0,0,0,0.32)` overlay to keep white text legible
- Image is `picture-shaped` — `object-fit: cover; height: 100%`, designed to be swapped without code changes. Future swap = replace `src` only.
- Eyebrow: `Our Vision` (`--green-on-dark`)
- Headline: `Advancing Oral & Public Health Through Innovation and Partnership`
- Body: **rewritten** so it does not repeat the header. Draft:

  > *"We envision a Rwanda where oral health is recognized as foundational to general well-being — where every community, regardless of geography or income, has access to preventive care, modern clinical practice, and the research and education that drive both forward. Our work bridges dentistry and medicine, students and professionals, urban centres and rural districts, to make that vision a reality."*

  User reviews this draft during spec review and may rewrite.

### 4.3 Story

- Two-column layout at `≥768px`: left column 240px (sticky-style label), right column flex (max-width 640px)
- At `<768px`: stack to single column, label on top
- Left column:
  - Eyebrow `Our Story` + sub-meta `Founded 2024 · Ngoma, Huye · Southern Province`
- Right column: 3 paragraphs from user copy verbatim, with 18px gap between them
- 1px bottom divider `--card-border`

### 4.4 Mission Quote

- Full-bleed, padding `clamp(56px, 8vw, 96px)`
- Background: same picture-shaped slot as Vision Banner. Default placeholder: `assets/img/doctor4.jpeg`. Hot-swappable via `src` attribute when better art arrives.
- Overlay: `--mission-overlay` gradient at 70% over image + `rgba(0,0,0,0.40)` darker overlay (heavier than Vision Banner — pull-quote needs maximum contrast)
- Eyebrow: `Our Mission` (`--green-on-dark`)
- Quote: serif italic, **flush-left**, max-width 820px, opening + closing curly quotes around the existing copy verbatim

### 4.5 Info Cards

- 3-up grid at `≥768px`, single column at `<768px`
- Each card: white surface, 1px `--card-border`, 14px border-radius, 22px padding, subtle shadow `0 1px 2px rgba(0,0,0,.04)`
- Card layout (top to bottom): emoji 22px → title 15px/600 → description 13px/400
- Emojis use the user's copy verbatim (📍 🤝 🌍). Note: emoji rendering varies by OS — accept this for now; SVG icon swap is a future enhancement, not in scope for this spec.

### 4.6 Values

- Two-column manifesto-style numbered list, `≥768px`. Single column at `<768px`.
- 36px row gap, 48px column gap
- Each entry: 32px serif numeral (`01`–`05`) in `--green-on-light` + content block (title 16px/600 + description 13px/secondary)
- Entries 1–4 fill rows 1 and 2; entry 5 spans column 1 of row 3 (left half, asymmetric on purpose — feels intentional rather than awkward)
- Eyebrow `What Guides Us` + Title `Our Core Values` precede the grid

### 4.7 Credibility band

- Dark band `--dark-band`, white text, padding `clamp(40px, 6vw, 56px)` × `clamp(20px, 4vw, 36px)`
- Eyebrow `RDMS at a Glance` (`--green-accent`)
- 4-up KPI grid (single row at `≥768px`, 2×2 at `<768px`):

  | Founded | RDB Code | Headquarters | Members |
  |---|---|---|---|
  | 1 July 2024 | 143885158 | Ngoma, Huye | 30+ |

- Below KPIs, 1px `rgba(255,255,255,.12)` divider, then a flex row of supplementary facts, gap 32px:
  - `📞 +250 791 853 120`
  - `📍 Southern Province, Rwanda`
  - `5+ Core Services`

- Replaces both Value 6 *and* the standalone "Stats: Founded 2024 · 5+ Core Services · 30+ Active Members" line from the user's copy

---

## 5. Homepage teaser refresh

The existing homepage `#about` block (currently `index.html` lines 265–270 and 273–277, both desktop and mobile variants) shows two paragraphs of unrelated lorem-ish copy about national dental check-up rates. Replace with a short teaser pointing to `/about`.

**New teaser content (both desktop and mobile variants, identical copy):**

- Eyebrow: `About RDMS` (unchanged class `eyebrow light what-is-techish` for visual continuity with the surrounding hero/dark backplate)
- Title: `Uniting dental and medical professionals for healthier communities.`
- Body (one paragraph, ~2 sentences):

  > *"RDMS Rwanda is a nonprofit professional society advancing oral and public health through education, research, and outreach. Founded in 2024 in Ngoma, Huye, we bring dental surgeons, therapists, doctors, and students together under one mission."*

- CTA: `Read our story →` linking to `about.html`. Styled as `.rdms-cta.secondary` to match hero CTA language, but recoloured for the dark backplate (it already sits over the hero video on mobile and over the dark hero gradient on desktop, so existing dark-bg styles apply).

The nav `/about` link (`index.html:192`) currently points to a non-existent path. Update to `about.html` in the same edit pass so the nav works on this static-hosted site.

---

## 6. Animations

- Match the existing site's `Webflow IX3` entrance pattern — subtle fade-in + slight Y translate on scroll-into-view for headings and major blocks.
- The existing site declares many of its IX3 hooks via `data-w-id` attributes that Webflow's runtime reads. For the new `about.html`, we **do not** wire up Webflow IX hooks (avoid coupling new code to that runtime). Instead, use a plain `IntersectionObserver` script that adds an `is-visible` class and let CSS transitions handle the reveal. Targets: section headings, Vision Banner content, Mission Quote, Value entries (staggered with `transition-delay`).
- Target durations: 600ms ease-out, max 80px Y translate.
- Reduced-motion: respect `prefers-reduced-motion: reduce` and disable transforms/transitions.

---

## 7. File plan

| Path | Action |
|---|---|
| `about.html` | **New** — full /about page, references existing `assets/css/webflow.css` (for resets/typography) and a new `assets/css/about.css` (page-specific styles). Reuses navbar + footer markup from `index.html` for visual + nav consistency. |
| `assets/css/about.css` | **New** — all /about block styles. Kept separate from `local-overrides.css` to keep the homepage's CSS surface clean. |
| `index.html` | **Edit** — replace the two `.about-container` blocks (desktop + mobile, lines ~265–277) with the new teaser markup. |
| `local-overrides.css` | **Edit** — add styles for the homepage teaser refresh (new title typography + CTA on the dark backplate). |
| `index.html` (nav link) | **Edit** — change `/about` → `about.html` at line ~192 so the navbar works on the static host. |
| `assets/img/` | **No new assets required** for v1 ship. Two photo placeholders use existing images (`hero-bg-rwanda-vivid.jpg`, `doctor4.jpeg`) and are designed for hot-swap when better photography lands. |

---

## 8. Out of scope (explicit non-goals)

- Custom SVG icons for info cards (emojis are accepted for v1)
- Final art-directed photography (placeholder strategy with hot-swap; user will replace)
- A new RDMS green-on-cream brand-colour token system beyond what's in §3
- Editing the existing 3-column scroll, text-callout, footer, or hero sections of the homepage
- Pop-up forms, contact-form behaviour, or analytics events
- Internationalization / translation; English only
- The Webflow runtime's `IX3` data-w-id hooks; new page uses vanilla `IntersectionObserver`

---

## 9. Risks & open questions

- **Photo placeholder identity:** The Vision Banner uses `hero-bg-rwanda-vivid.jpg` until art arrives. That same image is also the mobile hero fallback (`index.html:179`), so visitors may see it twice. Risk is low (different framing/overlay) but worth noting; user should swap to a different photo on first available pass.
- **Mission Quote backdrop choice:** I'm defaulting to `doctor4.jpeg`. If `doctor4` is going to be replaced too, both placeholder choices are equally easy to swap.
- **Vision Banner copy draft (§4.2):** Drafted but unvalidated by user. User reviews in spec-review step and rewrites if desired.
- **Mobile rhythm:** 7 stacked sections + global nav + footer is a long mobile scroll. Estimated 5–6 phone-screens of vertical content. Acceptable for an /about page; user can revisit if it feels long after seeing it live.
