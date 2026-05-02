---
name: RDMS Rwanda
description: Marketing site for the Dento-Medical Society Rwanda, a non-profit oral and public health society in Huye.
colors:
  cream-paper: "#f6f3ec"
  cream-tint: "#ece6d6"
  surface-card-light: "#ffffff"
  border-paper: "#e3ddd1"
  ink-primary: "#0a0a0a"
  ink-body: "#2a2a2a"
  ink-secondary: "#4a4a4a"
  ink-muted: "#7a7a7a"
  field-green-deep: "#1f6b3a"
  cooperative-green: "#58cc6f"
  mint-on-dark: "#a9e0b6"
  band-dark: "#0a0a0a"
  surface-card-dark-navy: "#0d2438"
  surface-card-dark-deep: "#0a1620"
  accent-gold: "#f5d28a"
  accent-cyan: "#7fd3e4"
typography:
  display:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(2rem, 4vw, 3rem)"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: "'Google Sans', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "normal"
  label:
    fontFamily: "'Google Sans', sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.08em"
  ui:
    fontFamily: "'Google Sans Flex', 'Montserrat', sans-serif"
    fontSize: "0.95rem"
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: "0.01em"
rounded:
  sm: "6px"
  md: "12px"
  lg: "20px"
  pill: "100px"
components:
  button-primary-light:
    backgroundColor: "{colors.surface-card-light}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "0.875rem 1.75rem"
    typography: "{typography.body}"
  button-primary-light-hover:
    backgroundColor: "#ededed"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
  button-ghost-on-dark:
    backgroundColor: "rgba(255,255,255,0.08)"
    textColor: "{colors.surface-card-light}"
    rounded: "{rounded.sm}"
    padding: "0.875rem 1.75rem"
  badge-pill-on-dark:
    backgroundColor: "rgba(88,204,111,0.15)"
    textColor: "{colors.cooperative-green}"
    rounded: "{rounded.pill}"
    padding: "0.375rem 1rem"
    typography: "{typography.label}"
  info-card-light:
    backgroundColor: "{colors.surface-card-light}"
    textColor: "{colors.ink-body}"
    rounded: "{rounded.md}"
    padding: "1.75rem"
  vision-banner:
    backgroundColor: "{colors.field-green-deep}"
    textColor: "{colors.surface-card-light}"
    rounded: "{rounded.lg}"
    padding: "3rem"
---

# Design System: RDMS Rwanda

## 1. Overview

**Creative North Star: working title "The Huye Cooperative."**

The system as it ships today is a layered surface. A Webflow template (cloned originally from `tech-ish.org`, a Kenyan tech blog) provides the structural foundation, with two RDMS-specific overlays painted on top: `local-overrides.css` for the homepage and `assets/css/about.css` for the about page. The result is a working site, but a system in transition: the bones of the template are still visible underneath the rebrand.

The current visual personality reads as warm, light-mode, evidence-led where it works and clinical-template where it does not. The cream paper background (`#f6f3ec`) carries the long-form material; deep-green and dark navy bands punctuate the scroll for the hero, vision, and call-to-action moments. The accent green (`#58cc6f`) is the loudest voice in the palette and appears on most interactive elements. Headlines run in stock browser Georgia, body in Google Sans, with a third UI face (Google Sans Flex / Montserrat) showing up in navigation. Component shape vocabulary is rounded but not consistent: 6px, 12px, 20px, and pill all appear with no fixed scale.

What this system explicitly rejects, per PRODUCT.md: white-savior NGO aesthetic, generic healthcare blue-and-teal, tech-startup template moves (gradient hero text, hero-metric, identical card grids), Africa-stock-photo, and any look that reads as templated or AI-generated. The current implementation has not fully escaped its template origins; that is the central tension this document records.

**Key Characteristics:**

- Two-mode site: long-form on warm cream, marketing punctuation on dark green/navy.
- One dominant accent (`cooperative-green`, `#58cc6f`) carrying both action and decoration.
- Typography is utilitarian: stock Georgia plus Google Sans, no committed display face.
- Spacing and radii are ad-hoc; there is no shared scale across the live CSS.
- A second, dead design system (`styles.css`) sits in the repo unlinked. It must be removed.
- Implementation depth: heavy. Webflow IX, GSAP, ScrollTrigger, UnicornStudio, Leaflet all run on the homepage.

## 2. Colors: The Cream-and-Cooperative Palette

A two-zone palette. Cream paper for the long, evidence-heavy parts of the page. Dark green and navy bands for moments of identity and action. One bright green accent threaded through both.

### Primary

- **Cooperative Green** (`#58cc6f`): the loudest voice in the palette. Used on links, eyebrow labels, hover states, the small dot animations, and most accent text on dark backgrounds. It is genuinely bright and saturated; it carries the modern-African energy when it lands well, and it tips into "language-app" territory when it lands on too many surfaces at once.

### Secondary

- **Field Green Deep** (`#1f6b3a`): the dignified counterpart to the cooperative green. Used on cream backgrounds for inline links and small accents, and as the base of the vision banner gradient. This is the color that should carry the institutional trust signal.
- **Mint on Dark** (`#a9e0b6`): the soft green used for accents on dark navy and dark green sections, where the saturated cooperative green would vibrate against the dark surface.

### Tertiary (rare, single-purpose)

- **Accent Gold** (`#f5d28a`): used once for a callout, not part of the regular vocabulary.
- **Accent Cyan** (`#7fd3e4`): used once, same.

### Neutral

- **Cream Paper** (`#f6f3ec`): the dominant page background for body content, about-page sections, and most cards' surrounds.
- **Cream Tint** (`#ece6d6`): a slightly darker cream used for tonal layering on cream when separation is needed without a hard border.
- **Border Paper** (`#e3ddd1`): the 1px hairline border on most cream-mode cards.
- **Surface Card Light** (`#ffffff`): white cards sitting on cream. Note: this is a pure-white surface, which contradicts the shared design law against `#fff`; flagged in Don'ts.
- **Ink Primary** (`#0a0a0a`): near-black headlines on cream.
- **Ink Body** (`#2a2a2a`): long-form body text.
- **Ink Secondary** (`#4a4a4a`): supporting copy and labels.
- **Ink Muted** (`#7a7a7a`): low-emphasis labels, small print.
- **Band Dark** (`#0a0a0a`): the dark band background used on dark sections.
- **Surface Card Dark Navy** (`#0d2438`): navy card surface used on a few dark CTAs.
- **Surface Card Dark Deep** (`#0a1620`): the deepest dark surface, used on one footer-adjacent CTA band.

### Named Rules

**The Two-Zone Rule.** The site lives in two modes: cream-paper for long-form content (about, story, values, leadership) and dark-band for hero, vision, mission, and CTA moments. A section commits to one mode or the other; mid-section transitions between cream and dark only happen at hard section breaks.

**The One Green Discipline.** When the cooperative green and the field-green deep both appear on the same surface, they read as "two greens" rather than as a deliberate scale. Pick one per section based on background luminance: cooperative green on dark surfaces, field-green-deep on cream.

## 3. Typography

**Display Font:** Georgia, with `'Times New Roman', serif` fallback. This is browser-stock and is currently the default for headlines on both homepage and about page (`local-overrides.css`, `assets/css/about.css`).

**Body Font:** Google Sans, with `sans-serif` fallback.

**UI Font:** Google Sans Flex with `'Montserrat', sans-serif` fallback. Used in the navigation and a few badge labels.

**Character.** A pragmatic, default-leaning pairing. Georgia carries the editorial weight without making a strong stylistic claim; Google Sans is the friendly Material-adjacent counterpart. The pairing reads competent and modern but does not yet have a typographic POV — and a non-profit working at this level of seriousness has room to claim one.

### Hierarchy

- **Display** (Georgia, 400, `clamp(2rem, 4vw, 3rem)`, line-height 1.15, letter-spacing -0.01em): hero headlines, vision banner title, mission quote.
- **Headline** (Georgia, 400, ~1.5–2rem): section titles ("Who We Are", "Our Story", "Our Core Values").
- **Title** (Google Sans, 600, ~1.125–1.25rem): card titles, leadership names, value titles.
- **Body** (Google Sans, 400, 1rem, line-height 1.65): long-form paragraphs. Body line length is currently uncapped on wide cards; should be held to 65–75ch.
- **Label** (Google Sans, 500, 0.75rem, letter-spacing 0.08em, uppercase): eyebrows ("Who We Are", "What We Do", "Leadership"), badges, small print.
- **UI** (Google Sans Flex, 500, ~0.95rem): navigation links, primary CTAs.

### Named Rules

**The No-Default-Display Rule.** Georgia is a default. Default is not a brand decision. The display face is the highest-leverage typographic move available; it should be a chosen face that signals proudly-Rwandan and modern-African voice (Pangram Pangram, ABC Dinamo, Velvetyne, Klim, or a custom-drawn face for headlines). Until that choice is made, Georgia is a placeholder, not a position.

## 4. Elevation

The system is **mostly flat** with two exceptions. Cards on cream backgrounds use a 1px `border-paper` hairline to separate, not a shadow. Section bands are full-width color blocks with no elevation; the hierarchy is established by background-color contrast, not by depth.

The two exceptions are the homepage hero (which uses an animated `clip-path` reveal of a video plus a UnicornStudio animated background) and a small `box-shadow` on the primary CTA hover state, transferred from the original template. There is no documented shadow vocabulary across components.

### Named Rules

**The Hairline Rule.** On cream backgrounds, separation is a 1px `#e3ddd1` border. Not a shadow. Shadows on cream paper read as photocopy, not paper.

**The Band-Color Rule.** On dark surfaces, separation between sections is full-bleed background color change, not a card or a shadow. The band IS the elevation.

## 5. Components

### Buttons

The site has two button molds with no formal token-level definition; each is repeated by hand across `local-overrides.css`.

- **Primary on Dark (light pill).** White surface (`#ffffff`), near-black text (`#0a0a0a`), 6px radius, 0.875rem × 1.75rem padding. Hover: `#ededed`. Used as the main CTA on dark hero sections. Note: the white surface is currently the common form, not the rare exception, which weakens its impact.
- **Ghost on Dark.** Translucent white background (`rgba(255,255,255,0.08)`), white text and 1px white border, same 6px radius and padding. Used as the secondary CTA on dark hero sections ("Learn About RDMS").

There is no documented light-mode primary button (the light-mode about page uses links and inline anchors only, not buttons). The "Get In Touch" CTA on the partner-with-RDMS section is a dark button on cream that does not match either mold.

### Badges and Pills

- **Eyebrow Pill on Dark.** A small pill containing uppercase label text plus a small pulsing dot. Background `rgba(88, 204, 111, 0.15)`, border `rgba(88, 204, 111, 0.28)`, text in cooperative green, 100px radius, 0.375rem × 1rem padding. Used as the hero badge ("Rwanda's Leading Non-Profit Oral Health Society"). One of the strongest patterns in the system.

### Cards

- **Info Card on Cream.** White surface (`#ffffff`) on cream background, 1px `#e3ddd1` border, 12px radius, 1.75rem padding. Used for the "Where We Operate", "Who We Bring Together", "Our Reach" tiles on the about page. Often opens with an emoji glyph (📍 🤝 🌍) which weakens the institutional voice.
- **Value Tile on Cream.** Same as the info card but smaller padding and a numbered or emoji-led heading. Used in the values grid.
- **Service Card.** Larger info-card variant used for the six core services (school screenings, preventive, research, Chronicles, Academy, mobile clinics).

### Vision and Mission Banners

- **Vision Banner.** Full-width band with a deep-green linear gradient (`linear-gradient(135deg, #1c3a2c, #3d6b52)`), white text, large Georgia display headline, body copy capped at a readable measure. The cleanest custom moment in the system.
- **Mission Banner.** Same shape, warm-dark gradient (`linear-gradient(135deg, #3d3a32, #1f1d18)`), pull-quote treatment.

### Navigation

- **Desktop.** Logo at left, a row of horizontal text links at right, one CTA. White-on-dark when the page top is in the dark band; switches to dark-on-cream when scrolled into the cream zones. Background uses a translucent backdrop-filter blur on scroll.
- **Mobile.** Hamburger button revealing a slide-from-right overlay menu (per recent commit). The overlay is dark-band-on-dark with white text.

### Maps

- **Leaflet Map** with marker clustering. Used on the about page (or planned) to show Rwanda program locations. A signature opportunity for proudly-Rwandan voice if the basemap and markers are styled away from default.

### Background Animation

- **UnicornStudio.** An animated visual lives behind the hero section, plus a clip-path-revealed video. This is the most ambitious motion moment and the one most at risk of feeling templated; needs an art-direction reason or it should be cut.

## 6. Do's and Don'ts

### Do:

- **Do** keep cream paper (`#f6f3ec`) as the dominant background for long-form material. The cream + dark-band rhythm is the strongest structural decision in the current system.
- **Do** lead with field-green-deep (`#1f6b3a`) for institutional trust signals on cream; reserve cooperative-green (`#58cc6f`) for moments that genuinely need brightness.
- **Do** use the eyebrow-pill-with-pulsing-dot pattern. It is the most distinctive component the system has.
- **Do** cap body line length at 65–75ch on cards and long-form sections.
- **Do** treat real RDMS data (RDB Code, founded date, district names, member count) as primary visual material per PRODUCT.md design principle 2.
- **Do** honor `prefers-reduced-motion: reduce` for the UnicornStudio background, the clip-path video reveal, and all GSAP / ScrollTrigger animations.
- **Do** subset and self-host any future webfont; the current Google Fonts dependency is a render-blocking cost on 3G/4G.

### Don't:

- **Don't** ship Georgia as the display face long-term. Per PRODUCT.md anti-reference 5 ("templated or AI-generated look"), browser-stock serif on a non-profit healthcare site is a tell.
- **Don't** keep `styles.css` in the repo. It is unlinked, contains the abandoned `Fraunces` + `DM Sans` + sage-green tech-blog system from the `tech-ish.org` clone, and is exactly the "tech-startup template" anti-reference. Delete it.
- **Don't** use `#ffffff` and `#000000` literally. Tint every neutral toward the brand hue (chroma 0.005 to 0.01 in OKLCH terms). The current `#ffffff` cards on cream and `#0a0a0a` dark band can both shift slightly green to feel intentional.
- **Don't** use emoji glyphs (📍 🤝 🌍 🇷🇼) as section-card iconography. Per PRODUCT.md anti-reference 5, this reads templated. Replace with custom marks, photography, or nothing.
- **Don't** repeat the icon-plus-heading-plus-paragraph card pattern across multiple sections (currently used for values, info cards, and services). Per PRODUCT.md anti-reference 3 ("tech-startup template") and the shared "identical card grids" ban, vary the affordance per section.
- **Don't** use gradient text (`background-clip: text` on a gradient). It does not appear yet; ban now.
- **Don't** use `border-left` greater than 1px as a colored stripe on cards or callouts. It does not appear yet; ban now.
- **Don't** lean on glassmorphism or backdrop-filter blurs as decoration. The nav already uses one for scroll state, which is the only legitimate use; add no more.
- **Don't** add side-by-side card grids of identical info cards for new sections. If a section has six services, six is not always six identical tiles; one or two of them deserve photographic or evidence-driven treatment.
- **Don't** use stock Africa imagery (baobab trees, generic "African child" photos). Use field photography from RDMS programs in Huye, Ngoma, the Southern Province, or equivalent specificity. If no specific photo exists, use no photo.
- **Don't** ship hero-metric "big number, small label, supporting stats, gradient accent" patterns. The "Founded 2024 · 5+ Core Services · 30+ Members" line is on the line; if it grows into a cliché-shaped grid, it has crossed it.
- **Don't** rely on Webflow IX for primary motion. It is a 200KB+ runtime that costs heavily on 3G; if a motion is essential, build it with native CSS or a small targeted GSAP timeline.
