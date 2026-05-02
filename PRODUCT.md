# Product

## Register

brand

## Users

**Primary: institutional donors and program funders.** International NGO program officers, Rwandan diaspora donors, foundations, ministry partners, and corporate CSR leads. They arrive evaluating whether RDMS is a credible, fundable partner for a specific program, most often a mobile-clinic deployment, school screening campaign, or research initiative. Context: they are doing diligence, comparing RDMS against other African health NGOs, often on a phone, often in a hurry.

**Secondary users:** dental and medical students and professionals in Rwanda considering RDMS membership; government and academic partners exploring collaboration; community organizations and schools seeking information about RDMS programs in their district.

## Product Purpose

A marketing and credibility site for the Dento-Medical Society Rwanda (RDMS), a non-profit oral and public health society founded 1 July 2024 in Huye, Southern Province, Rwanda. RDB Code 143885158.

The site exists to convert qualified visitors into funders, members, and partners by communicating who RDMS is, what it does, where it operates, and the evidence behind its work. Five core programs anchor the offer: school-based dental screenings, preventive care programs, oral health research and data collection, the Dental Medicine Chronicles publication, the RDMS Research Academy, and community mobile clinics.

Success: a donor finishes the homepage ready to fund a specific program deployment, most often a mobile-clinic. Secondary success: a Rwandan dental or medical professional applies for membership. Tertiary: a partner institution makes contact.

## Brand Personality

Three words: **proudly-Rwandan, warm, community-led.** Supporting note: **modern-African.**

The voice is that of a Rwandan-rooted, Africa-confident health professional speaking directly to peers and partners. Not a Western NGO talking about Rwanda. Not a clinical institution lecturing communities. Confident in its origin, generous in its tone, evidence-led in its substance.

Emotional register: dignified without being stiff, warm without being soft, modern without chasing tech-trend signals. The site should feel like the work of people who live and practice in Huye, not the work of a Geneva consultancy or a Webflow template farm.

## Anti-references

This site must not look like:

1. **White-savior-NGO aesthetic.** No sad-children photography, no "your $5 saves a life" appeals, no hand-on-shoulder stock imagery, no copy that frames Rwandans as recipients of pity rather than agents of their own health system. Donors should be invited into a partnership, not a rescue.

2. **Generic healthcare.** No white-and-teal palette, no blue-on-white SaaS-clinic feel, no stethoscope-or-tooth-icon decoration. The first-order training-data reflex for "oral health website" is exactly what to avoid.

3. **Tech-startup template.** No big-number-small-label hero metrics, no gradient hero text, no "platform" copy, no identical card grids with icon-plus-heading-plus-text. The current codebase began as a clone of `tech-ish.org`, a tech-blog template, and that DNA must be designed out rather than preserved.

4. **Africa-stock-photo.** No baobab-trees-at-sunset, no generic-Africa imagery without specificity to Rwanda, Huye, Ngoma district, or RDMS programs. If a photo could be from any country in the region, it does not belong on this site.

5. **Templated or AI-generated look.** No glassmorphism-because-it-feels-modern, no floating-card hero clichés, no symmetrical hero-grid-CTA-grid-footer rhythm that any Webflow agency could ship in a day. The site should feel hand-crafted for RDMS specifically: its place, its people, its work.

## Design Principles

1. **Specificity over generality.** Every photo, stat, name, and label should be unmistakably RDMS in Huye, not interchangeable with any other health NGO. Real names (Igisubizo Jimmy Confiance, Natukunda Sharon, the rest of the team), real places (Ngoma district, Southern Province), real numbers (RDB Code 143885158, founded 1 July 2024, +250 791 853 120).

2. **Evidence as visual material.** Research findings, screening data, program reach, and partner names are the design content, not decoration laid over abstract shapes. Treat numbers and field photographs as primary craft surfaces. A donor reads "screened 4,200 schoolchildren in 12 districts" before they read any tagline.

3. **Donor-grade trust signals throughout.** Legal registration, governance structure, leadership, financial discipline, and named partners should be visible without being shoved at the reader. A program officer should see legitimacy within the first scroll, not buried on the About page.

4. **Mobile-first, low-bandwidth-respectful.** Most Rwandan visitors and many regional partners arrive on mobile, often on metered 3G or 4G. Image weight, web-font payload, and JS-execution cost must work under those constraints. Performance is an accessibility decision, not a polish step.

5. **Modern-African, not template-modern.** Typography, color, photography, and motion should reach for contemporary Rwandan and pan-African design references rather than generic SaaS or NGO templates. When in doubt, favor the choice that could only have been made for this specific organization.

## Accessibility & Inclusion

- **WCAG 2.1 AA** is the minimum bar: color contrast, keyboard navigation, visible focus states, semantic landmarks, alt text on every photo, captions on any video.
- **Reduced motion.** The site relies on Webflow IX, GSAP, ScrollTrigger, and UnicornStudio. All decorative motion must honor `prefers-reduced-motion: reduce`.
- **Low-bandwidth performance.** Treat low-bandwidth performance as an accessibility requirement, not a polish step. Image dimensions, codec choice (WebP / AVIF), font subsetting, and lazy-loading all matter on 3G or 4G.
- **Languages.** English ships first. Kinyarwanda and French are planned. Build copy and components so they are translatable: no hard-coded strings inside JS, room for longer French strings in buttons and navigation, allowance for slightly longer Kinyarwanda compounds in headings. Right-to-left is not required.
