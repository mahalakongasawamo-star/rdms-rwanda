"""
Generate a design + strategy summary PDF for the RDMS Rwanda website.
Reads brand from PRODUCT.md / DESIGN.md and writes a multi-page PDF
covering: what the site is for, goals, design system, color rationale,
and look-and-feel decisions.
"""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Image,
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os

ROOT = Path(__file__).parent
OUTPUT = ROOT / "RDMS-Rwanda-Design-Summary.pdf"
LOGO = ROOT / "assets" / "img" / "rdms-logo.png"

# Brand colors (from DESIGN.md)
CREAM_PAPER       = HexColor("#f6f3ec")
CREAM_TINT        = HexColor("#ece6d6")
INK_PRIMARY       = HexColor("#0a0a0a")
INK_BODY          = HexColor("#2a2a2a")
INK_SECONDARY     = HexColor("#4a4a4a")
INK_MUTED         = HexColor("#7a7a7a")
FIELD_GREEN_DEEP  = HexColor("#1f6b3a")
COOPERATIVE_GREEN = HexColor("#58cc6f")
MINT_ON_DARK      = HexColor("#a9e0b6")
BAND_DARK         = HexColor("#0a0a0a")
RWANDA_BLUE       = HexColor("#00a1de")
RWANDA_YELLOW     = HexColor("#fad201")
RWANDA_GREEN      = HexColor("#20603d")

# --- Styles ---------------------------------------------------------

styles = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1", parent=styles["Title"],
    fontName="Times-Roman", fontSize=28, leading=32,
    textColor=INK_PRIMARY, spaceAfter=8, alignment=TA_LEFT,
)
H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName="Times-Roman", fontSize=18, leading=22,
    textColor=INK_PRIMARY, spaceBefore=18, spaceAfter=8, alignment=TA_LEFT,
)
H3 = ParagraphStyle(
    "H3", parent=styles["Heading3"],
    fontName="Helvetica-Bold", fontSize=11, leading=14,
    textColor=FIELD_GREEN_DEEP, spaceBefore=12, spaceAfter=4, alignment=TA_LEFT,
)
EYEBROW = ParagraphStyle(
    "Eyebrow", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9, leading=12,
    textColor=FIELD_GREEN_DEEP, spaceAfter=4, alignment=TA_LEFT,
)
BODY = ParagraphStyle(
    "Body", parent=styles["BodyText"],
    fontName="Helvetica", fontSize=10.5, leading=15.5,
    textColor=INK_BODY, spaceAfter=8, alignment=TA_LEFT,
)
LEAD = ParagraphStyle(
    "Lead", parent=BODY,
    fontName="Times-Italic", fontSize=12, leading=18,
    textColor=INK_BODY, spaceAfter=12,
)
META = ParagraphStyle(
    "Meta", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8.5, leading=11,
    textColor=INK_SECONDARY, alignment=TA_LEFT,
)
COVER_TITLE = ParagraphStyle(
    "CoverTitle", parent=H1,
    fontSize=36, leading=42, spaceAfter=14,
)
COVER_SUB = ParagraphStyle(
    "CoverSub", parent=BODY,
    fontName="Times-Italic", fontSize=14, leading=20,
    textColor=INK_SECONDARY, spaceAfter=24,
)
SWATCH_LABEL = ParagraphStyle(
    "Swatch", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8.5, leading=11,
    textColor=INK_BODY, alignment=TA_LEFT,
)


# --- Page decorations ----------------------------------------------

def first_page(canvas, doc):
    """Cover page: tricolor stripe + logo + title."""
    width, height = LETTER
    canvas.saveState()
    # Cream paper backdrop
    canvas.setFillColor(CREAM_PAPER)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    # Tricolor letterhead at the very top
    bar_h = 6
    canvas.setFillColor(RWANDA_BLUE)
    canvas.rect(0, height - bar_h, width, bar_h, fill=1, stroke=0)
    canvas.setFillColor(RWANDA_YELLOW)
    canvas.rect(0, height - bar_h * 2, width, bar_h, fill=1, stroke=0)
    canvas.setFillColor(RWANDA_GREEN)
    canvas.rect(0, height - bar_h * 3, width, bar_h, fill=1, stroke=0)
    # Footer line
    canvas.setStrokeColor(FIELD_GREEN_DEEP)
    canvas.setLineWidth(0.6)
    canvas.line(0.75 * inch, 0.75 * inch, width - 0.75 * inch, 0.75 * inch)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(INK_SECONDARY)
    canvas.drawString(0.75 * inch, 0.55 * inch,
                      "RDMS Rwanda  ·  Design & Strategy Summary  ·  May 2026")
    canvas.restoreState()


def later_page(canvas, doc):
    """Subsequent pages: cream backdrop + thin top stripe + footer rule."""
    width, height = LETTER
    canvas.saveState()
    canvas.setFillColor(CREAM_PAPER)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    # Slim tricolor at top
    bar_h = 3
    canvas.setFillColor(RWANDA_BLUE)
    canvas.rect(0, height - bar_h, width, bar_h, fill=1, stroke=0)
    canvas.setFillColor(RWANDA_YELLOW)
    canvas.rect(0, height - bar_h * 2, width, bar_h, fill=1, stroke=0)
    canvas.setFillColor(RWANDA_GREEN)
    canvas.rect(0, height - bar_h * 3, width, bar_h, fill=1, stroke=0)
    # Footer
    canvas.setStrokeColor(FIELD_GREEN_DEEP)
    canvas.setLineWidth(0.4)
    canvas.line(0.75 * inch, 0.65 * inch, width - 0.75 * inch, 0.65 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK_SECONDARY)
    canvas.drawString(0.75 * inch, 0.45 * inch,
                      "RDMS Rwanda  ·  Design & Strategy Summary")
    canvas.drawRightString(width - 0.75 * inch, 0.45 * inch,
                           "Page %d" % canvas.getPageNumber())
    canvas.restoreState()


# --- Color swatch table --------------------------------------------

def color_swatches():
    rows = [
        ("Cream paper",        CREAM_PAPER,       "#F6F3EC", "Long-form body surfaces (About, Services, Projects, Contact paper)"),
        ("Cream tint",         CREAM_TINT,        "#ECE6D6", "Academy paper card; chatbot footer"),
        ("Field-green-deep",   FIELD_GREEN_DEEP,  "#1F6B3A", "Institutional accent; donor-grade trust signal"),
        ("Cooperative-green",  COOPERATIVE_GREEN, "#58CC6F", "Action accent; CTAs; active-state pill-tint"),
        ("Mint-on-dark",       MINT_ON_DARK,      "#A9E0B6", "Soft accent on dark surfaces"),
        ("Ink primary",        INK_PRIMARY,       "#0A0A0A", "Headlines on cream"),
        ("Ink body",           INK_BODY,          "#2A2A2A", "Long-form body text"),
        ("Ink secondary",      INK_SECONDARY,     "#4A4A4A", "Supporting copy, labels"),
        ("Rwanda blue",        RWANDA_BLUE,       "#00A1DE", "Tricolor letterhead stripe"),
        ("Rwanda yellow",      RWANDA_YELLOW,     "#FAD201", "Tricolor letterhead stripe"),
        ("Rwanda green",       RWANDA_GREEN,      "#20603D", "Tricolor letterhead stripe"),
    ]
    data = [["", "Token", "Hex", "Used on"]]
    for name, color, hex_str, usage in rows:
        # Swatch cell — empty, colored via TableStyle
        data.append(["", name, hex_str, usage])
    t = Table(data, colWidths=[0.55 * inch, 1.6 * inch, 0.85 * inch, 3.5 * inch])
    style = [
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), INK_PRIMARY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK_PRIMARY),
        ("FONT", (1, 1), (-1, -1), "Helvetica", 9.5),
        ("TEXTCOLOR", (1, 1), (-1, -1), INK_BODY),
        ("FONT", (2, 1), (2, -1), "Courier", 9),
        ("TEXTCOLOR", (2, 1), (2, -1), INK_SECONDARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, HexColor("#e3ddd1")),
    ]
    # Fill swatch cells with each color
    for i, (_, color, _, _) in enumerate(rows, start=1):
        style.append(("BACKGROUND", (0, i), (0, i), color))
    t.setStyle(TableStyle(style))
    return t


# --- Story (the document content) -----------------------------------

def build_story():
    s = []

    # ---------- Cover ----------
    s.append(Spacer(1, 1.6 * inch))
    if LOGO.exists():
        try:
            img = Image(str(LOGO), width=1.0 * inch, height=1.0 * inch)
            img.hAlign = "LEFT"
            s.append(img)
            s.append(Spacer(1, 0.3 * inch))
        except Exception:
            pass
    s.append(Paragraph("RDMS Rwanda", EYEBROW))
    s.append(Paragraph("Design &amp; Strategy Summary", COVER_TITLE))
    s.append(Paragraph(
        "Why this website exists, who it serves, and the design "
        "decisions behind every section, color, and typographic choice.",
        COVER_SUB
    ))
    s.append(Paragraph(
        "Dento-Medical Society Rwanda (RDMS) &middot; Ngoma, Huye, "
        "Southern Province &middot; RDB Code 143885158 &middot; "
        "Registered 1 July 2024",
        META
    ))
    s.append(PageBreak())

    # ---------- Section 1: What this site is for ----------
    s.append(Paragraph("Section 01", EYEBROW))
    s.append(Paragraph("What this website is for", H1))
    s.append(Paragraph(
        "A marketing and credibility site for RDMS, a non-profit oral "
        "and public-health society in Huye, Rwanda. The site exists to "
        "convert qualified visitors into funders, members, and "
        "partners by communicating who RDMS is, what it does, where "
        "it operates, and the evidence behind its work.",
        LEAD
    ))

    s.append(Paragraph("Primary audience", H3))
    s.append(Paragraph(
        "<b>Institutional donors and program funders.</b> International "
        "NGO program officers, Rwandan diaspora donors, foundations, "
        "ministry partners, and corporate CSR leads. They arrive "
        "evaluating whether RDMS is a credible, fundable partner for a "
        "specific program: most often a mobile-clinic deployment, school "
        "screening campaign, or research initiative. Context: they are "
        "doing diligence, comparing RDMS against other African health "
        "NGOs, often on a phone, often in a hurry.",
        BODY
    ))

    s.append(Paragraph("Secondary audiences", H3))
    s.append(Paragraph(
        "Dental and medical students and professionals in Rwanda "
        "considering RDMS membership. Government and academic partners "
        "exploring collaboration. Community organizations and schools "
        "seeking information about RDMS programs in their district.",
        BODY
    ))

    s.append(Paragraph("Success criteria", H3))
    s.append(Paragraph(
        "<b>Primary:</b> a donor finishes the homepage ready to fund a "
        "specific program deployment, most often a mobile-clinic.",
        BODY
    ))
    s.append(Paragraph(
        "<b>Secondary:</b> a Rwandan dental or medical professional "
        "applies for membership.",
        BODY
    ))
    s.append(Paragraph(
        "<b>Tertiary:</b> a partner institution makes contact about "
        "collaboration, research, or policy work.",
        BODY
    ))

    s.append(Paragraph("Five core programs anchor the offer", H3))
    s.append(Paragraph(
        "School-Based Dental Screenings &middot; Preventive Care "
        "Programs &middot; Oral Health Research &amp; Data Collection "
        "&middot; Dental Medicine Chronicles publication &middot; RDMS "
        "Research Academy &middot; Community Mobile Clinics.",
        BODY
    ))

    s.append(PageBreak())

    # ---------- Section 2: Strategic goals ----------
    s.append(Paragraph("Section 02", EYEBROW))
    s.append(Paragraph("Strategic goals", H1))
    s.append(Paragraph(
        "Five design principles, lifted directly from the project's "
        "PRODUCT.md, govern every decision on the site:",
        LEAD
    ))

    goals = [
        (
            "1. Specificity over generality",
            "Every photo, stat, name, and label is unmistakably RDMS in "
            "Huye, not interchangeable with any other health NGO. Real "
            "names (Igisubizo Jimmy Confiance, Natukunda Sharon, the "
            "rest of the team), real places (Ngoma district, Southern "
            "Province), real numbers (RDB Code 143885158, founded "
            "1 July 2024, +250 791 853 120)."
        ),
        (
            "2. Evidence as visual material",
            "Research findings, screening data, program reach, and "
            "partner names are the design content, not decoration laid "
            "over abstract shapes. Numbers and field photographs are "
            "primary craft surfaces. A donor reads &ldquo;screened "
            "4,200 schoolchildren in 12 districts&rdquo; before they "
            "read any tagline."
        ),
        (
            "3. Donor-grade trust signals throughout",
            "Legal registration, governance structure, leadership, "
            "financial discipline, and named partners are visible "
            "without being shoved at the reader. A program officer "
            "should see legitimacy within the first scroll, not buried "
            "on the About page."
        ),
        (
            "4. Mobile-first, low-bandwidth-respectful",
            "Most Rwandan visitors and many regional partners arrive "
            "on mobile, often on metered 3G or 4G. Image weight, "
            "web-font payload, and JS-execution cost work under those "
            "constraints. Performance is treated as an accessibility "
            "decision, not a polish step."
        ),
        (
            "5. Modern-African, not template-modern",
            "Typography, color, photography, and motion reach for "
            "contemporary Rwandan and pan-African design references "
            "rather than generic SaaS or NGO templates. When in doubt, "
            "the choice that could only have been made for this "
            "specific organization wins."
        ),
    ]
    for title, body in goals:
        s.append(Paragraph(title, H3))
        s.append(Paragraph(body, BODY))

    s.append(PageBreak())

    # ---------- Section 3: Anti-references ----------
    s.append(Paragraph("Section 03", EYEBROW))
    s.append(Paragraph("What this website must NOT look like", H1))
    s.append(Paragraph(
        "Five anti-references guide the design as strongly as the "
        "design principles. Each is a category-reflex pattern the "
        "site actively designs against.",
        LEAD
    ))

    antis = [
        (
            "1. White-savior NGO aesthetic",
            "No sad-children photography, no &ldquo;your $5 saves a "
            "life&rdquo; appeals, no hand-on-shoulder stock imagery, "
            "no copy that frames Rwandans as recipients of pity rather "
            "than agents of their own health system. Donors are invited "
            "into a partnership, not a rescue."
        ),
        (
            "2. Generic healthcare",
            "No white-and-teal palette, no blue-on-white SaaS-clinic "
            "feel, no stethoscope-or-tooth-icon decoration. The "
            "first-order training-data reflex for &ldquo;oral health "
            "website&rdquo; is exactly what to avoid."
        ),
        (
            "3. Tech-startup template",
            "No big-number-small-label hero metrics, no gradient hero "
            "text, no &ldquo;platform&rdquo; copy, no identical card "
            "grids with icon-plus-heading-plus-text. The codebase "
            "began as a clone of a tech-blog template; that DNA was "
            "designed out, not preserved."
        ),
        (
            "4. Africa-stock-photo",
            "No baobab-trees-at-sunset, no generic-Africa imagery "
            "without specificity to Rwanda, Huye, Ngoma district, or "
            "RDMS programs. If a photo could be from any country in "
            "the region, it does not belong on this site."
        ),
        (
            "5. Templated or AI-generated look",
            "No glassmorphism-because-it-feels-modern, no "
            "floating-card hero clich&eacute;s, no symmetrical "
            "hero-grid-CTA-grid-footer rhythm that any agency could "
            "ship in a day. The site is hand-crafted for RDMS "
            "specifically: its place, its people, its work."
        ),
    ]
    for title, body in antis:
        s.append(Paragraph(title, H3))
        s.append(Paragraph(body, BODY))

    s.append(PageBreak())

    # ---------- Section 4: Color system ----------
    s.append(Paragraph("Section 04", EYEBROW))
    s.append(Paragraph("Color system", H1))
    s.append(Paragraph(
        "A two-zone palette: cream paper for the long, evidence-heavy "
        "parts of the page, dark green and tricolor moments for "
        "identity and action. One bright green accent threads through "
        "both zones, with a deeper field-green-deep reserved for "
        "institutional trust signals.",
        LEAD
    ))

    s.append(Paragraph("Tokens in use", H3))
    s.append(color_swatches())
    s.append(Spacer(1, 0.18 * inch))

    s.append(Paragraph("Color rationale: why these choices", H2))

    s.append(Paragraph("Cream paper, not white", H3))
    s.append(Paragraph(
        "Pure <font face='Courier'>#FFFFFF</font> is the SaaS-clinic "
        "reflex (anti-reference 2). Cream paper "
        "(<font face='Courier'>#F6F3EC</font>) reads as institutional "
        "stationery, like a foundation report, museum letterhead, or "
        "academic monograph. It signals dignified long-form material, "
        "not consumer product. The cream-tint variant "
        "(<font face='Courier'>#ECE6D6</font>) on the Research Academy "
        "section adds tonal weight without leaving the warm zone, "
        "differentiating it from the Contact paper without changing "
        "register.",
        BODY
    ))

    s.append(Paragraph("Two greens, one discipline", H3))
    s.append(Paragraph(
        "<b>Cooperative green</b> (<font face='Courier'>#58CC6F</font>) "
        "carries action and energy: CTAs, the &ldquo;Write to "
        "RDMS&rdquo; button, the active-state pill on the navbar, the "
        "Drenched Chronicles announcement band. <b>Field-green-deep</b> "
        "(<font face='Courier'>#1F6B3A</font>) carries dignity: inline "
        "links on cream, the institutional accent on Contact, the "
        "founder's signature, the FAQ category headings. The discipline "
        "is one green per surface based on background luminance: "
        "cooperative-green on dark, field-green-deep on cream. They "
        "never compete on the same band.",
        BODY
    ))

    s.append(Paragraph("Why green specifically (and not blue or teal)", H3))
    s.append(Paragraph(
        "<b>Blue/teal is the first-order reflex for healthcare websites.</b> "
        "PRODUCT.md anti-reference 2 explicitly forbids it: "
        "&ldquo;no white-and-teal palette, no blue-on-white SaaS-clinic "
        "feel.&rdquo; Green resists that reflex. It also picks up the "
        "Rwandan flag's lower stripe, anchoring the palette to a real "
        "national identity rather than a generic medical "
        "category-color.",
        BODY
    ))

    s.append(Paragraph("Rwanda flag tricolor as decorative spine", H3))
    s.append(Paragraph(
        "Sky-blue (<font face='Courier'>#00A1DE</font>) &middot; "
        "sun-yellow (<font face='Courier'>#FAD201</font>) &middot; "
        "field-green (<font face='Courier'>#20603D</font>) appear "
        "exclusively as <i>letterhead stripes</i>: thin horizontal bars "
        "at the top of the Letter from Huye, Research Academy, FAQ, "
        "and chatbot panel; a small stacked mark next to "
        "&ldquo;Made in Rwanda&rdquo; in the footer. They are never "
        "used as primary surface colors. The discipline is national "
        "identity as masthead, not as wallpaper. One literal flag "
        "image survives, in the footer's bottom-right circle, as the "
        "single piece of Rwandan iconography earned its weight by "
        "being the closing punctuation on the page.",
        BODY
    ))

    s.append(Paragraph("Inks tinted toward the brand hue", H3))
    s.append(Paragraph(
        "Pure <font face='Courier'>#000000</font> is forbidden; every "
        "neutral on the page is tinted slightly toward the brand "
        "green so the text reads as <i>part of the surface</i>, not "
        "imported from a default browser stylesheet. The four ink "
        "values (primary, body, secondary, muted) form a hierarchy: "
        "headlines own the page; body sits one step quieter; metadata "
        "sits two steps quieter; footnote credits sit three steps "
        "quieter. The eye climbs naturally.",
        BODY
    ))

    s.append(PageBreak())

    # ---------- Section 5: Typography & layout ----------
    s.append(Paragraph("Section 05", EYEBROW))
    s.append(Paragraph("Typography &amp; layout", H1))

    s.append(Paragraph("Two faces, two voices", H3))
    s.append(Paragraph(
        "<b>Georgia</b> (display) carries headlines, signatures, "
        "founder voice, and editorial moments. It evokes the "
        "academic-journal and museum-publication register that "
        "anchors institutional trust. <b>Google Sans</b> (body and "
        "UI) carries body copy, labels, eyebrows, and form fields. "
        "Italic Georgia is reserved for accent words inside headlines "
        "(set in field-green-deep) and the founder's signature. "
        "Together, the pairing reads: pragmatic and modern in body, "
        "editorial and dignified in display.",
        BODY
    ))

    s.append(Paragraph("Body measure capped at 60-65ch", H3))
    s.append(Paragraph(
        "Long lines tire the eye. Every long-form section caps at a "
        "readable measure, which on a 1200px container produces "
        "magazine-style two-column reading rhythm without forcing the "
        "reader to track across 100+ characters per line. The Letter "
        "from Huye, the FAQ answers, and the About origin all hold to "
        "this measure.",
        BODY
    ))

    s.append(Paragraph("Spacing rhythm, not uniform padding", H3))
    s.append(Paragraph(
        "Sections vary in vertical padding deliberately. Hero opens "
        "tall (clamp 96-132px). About starts wide for the breath after "
        "the hero. Services and Projects sit moderate. Chronicles "
        "compresses to a tight Drenched-green bar. Letter from Huye "
        "opens generously, like a real paper letter. The footer settles "
        "compactly. Same padding everywhere is monotony; varied "
        "spacing creates the reading rhythm that makes a long page "
        "feel like a single composed thing.",
        BODY
    ))

    s.append(Paragraph("Section-level layout patterns", H3))
    s.append(Paragraph(
        "<b>Editorial spread</b> (Services): asymmetric featured-big "
        "composition. <b>Press log</b> (Projects): dated activity log "
        "grouped by status. <b>Magazine</b> (FAQ): sticky category nav "
        "left, Q&amp;A pairs right. <b>Letter</b> (Contact): "
        "single-column institutional letter on cream paper, signed. "
        "<b>Featured + roll</b> (Academy): one large article above five "
        "dated rows. <b>Three pillars</b>: Kinyarwanda (<i>Mbere / "
        "Kabiri / Gatatu</i>) anchor each pillar. Every section uses a "
        "different affordance: no two sections look like each other, "
        "which prevents the &ldquo;identical card grid&rdquo; "
        "anti-pattern PRODUCT.md flags.",
        BODY
    ))

    s.append(PageBreak())

    # ---------- Section 6: Look & feel ----------
    s.append(Paragraph("Section 06", EYEBROW))
    s.append(Paragraph("Look &amp; feel: the &ldquo;Modern-African&rdquo; brief", H1))
    s.append(Paragraph(
        "The brand personality is three words: "
        "<b>proudly-Rwandan, warm, community-led</b>, with a supporting "
        "note of <b>modern-African</b>. The voice is that of a "
        "Rwandan-rooted, Africa-confident health professional speaking "
        "directly to peers and partners. Not a Western NGO talking "
        "about Rwanda. Not a clinical institution lecturing communities. "
        "Confident in its origin, generous in its tone, evidence-led "
        "in its substance.",
        LEAD
    ))

    s.append(Paragraph("Specific design moves that earn the brief", H3))
    s.append(Paragraph(
        "<b>Kinyarwanda numerals</b> (<i>Mbere / Kabiri / Gatatu</i>) "
        "label the Three Pillars. A single Kinyarwanda anchor on a "
        "donor-facing page is the strongest signal that the work was "
        "written in Rwanda for Rwandan audiences first.",
        BODY
    ))
    s.append(Paragraph(
        "<b>Letter from Huye</b>, signed by Igisubizo Jimmy Confiance "
        "(Founder &amp; CEO), replaces the conventional contact form "
        "as the page's emotional close. Donors meet a real person, "
        "not a generic input field. The form moves to an overlay; the "
        "letter does the persuasion.",
        BODY
    ))
    s.append(Paragraph(
        "<b>Projects as a dated activity log</b> (Active Now / Recently "
        "Completed / Coming Next, with real dates like 20 Feb 2026) "
        "kills the Kanban-card-grid and replaces it with a society "
        "newsletter format that reads like institutional reporting.",
        BODY
    ))
    s.append(Paragraph(
        "<b>Real names, real district, real RDB code</b> threaded "
        "throughout: hero credibility row, Letter signature, footer "
        "footnote, FAQ. Each reinforces &ldquo;this is a registered "
        "Rwandan organization with named accountable leaders, not a "
        "marketing placeholder.&rdquo;",
        BODY
    ))
    s.append(Paragraph(
        "<b>Tricolor letterhead stripes</b> mark the editorial sections "
        "(Letter, Academy, FAQ, chatbot panel) as official Rwandan "
        "stationery. The detail is small, but a visitor recognizes the "
        "national colors as a continuous design language.",
        BODY
    ))
    s.append(Paragraph(
        "<b>Adaptive nav theme</b>: the floating navbar pill switches "
        "from dark glass over the hero to cream glass over the "
        "long-form sections, picking up each section's "
        "<font face='Courier'>data-nav-theme</font> attribute via "
        "IntersectionObserver. A small detail that signals the nav "
        "respects the surface it floats over.",
        BODY
    ))

    s.append(Paragraph("Anti-pattern interventions", H3))
    s.append(Paragraph(
        "The page actively avoids: gradient hero text, glassmorphism "
        "as decoration, identical 3-up icon-card grids, hero-metric "
        "templates, em dashes (banned by the project's shared design "
        "law), <font face='Courier'>#FFFFFF</font>/"
        "<font face='Courier'>#000000</font> literals, side-stripe "
        "borders larger than 1px, modal-as-first-thought patterns.",
        BODY
    ))

    s.append(Paragraph("Performance as accessibility", H3))
    s.append(Paragraph(
        "PRODUCT.md treats low-bandwidth as an accessibility "
        "requirement, not a polish step. Image weight is capped, "
        "lazy-loading is on for all below-fold imagery, the AI "
        "chatbot is a static client-side mockup with no LLM round-trip, "
        "and partner logos are CSS-filtered to a single tonal "
        "treatment so 7 different JPEGs render as one consistent "
        "monochromatic row. The Rwanda flag-colors video that opens "
        "the hero is the only heavy media asset, web-optimized "
        "(faststart) and reused as ambient backdrop on Academy and "
        "Contact.",
        BODY
    ))

    s.append(Paragraph("Accessibility commitments", H3))
    s.append(Paragraph(
        "WCAG 2.1 AA as the minimum bar. Skip-link as the first "
        "focusable element. Single &lt;main&gt; landmark wrapping all "
        "content. Native semantic HTML throughout (article, dl/dt/dd "
        "for FAQ, blockquote for the mission, ol for projects, "
        "figure/figcaption for photos). All decorative motion honors "
        "<font face='Courier'>prefers-reduced-motion: reduce</font>. "
        "Color contrast meets AA on every text/background pair. "
        "Keyboard tab order is logical from skip-link through nav, "
        "main content, and footer. Focus rings are visible and use the "
        "field-green-deep brand accent rather than browser defaults.",
        BODY
    ))

    s.append(PageBreak())

    # ---------- Section 7: At a glance ----------
    s.append(Paragraph("Section 07", EYEBROW))
    s.append(Paragraph("At a glance", H1))

    s.append(Paragraph("The site, in one sentence", H3))
    s.append(Paragraph(
        "A donor-first, evidence-led, proudly-Rwandan website that "
        "converts qualified visitors into funders, members, and "
        "partners by communicating who RDMS is, what it does, where "
        "it operates, and who is accountable, while actively "
        "rejecting every generic-NGO and SaaS-clinic visual reflex.",
        LEAD
    ))

    s.append(Paragraph("Page composition (top to bottom)", H3))
    composition = [
        "Hero: video backdrop + editorial type-led pitch, primary CTA &ldquo;Partner with RDMS&rdquo;",
        "About: origin + mission manifesto + five-principle credo",
        "Leadership: featured CEO + 4 team members",
        "Three Pillars: Mbere / Kabiri / Gatatu (Care / Knowledge / Advocacy)",
        "Services: editorial spread, six numbered services, no card grid",
        "Projects: dated activity log, three status bands (Active / Completed / Coming)",
        "Research Academy: featured lesson + 5 dated roll rows on cream-tint paper",
        "Chronicles: drenched-green announcement band",
        "FAQ: two-column magazine, 9 categories, 38 questions",
        "Contact: Letter from Huye, signed by Founder, ranked contact methods",
        "Footer: trust-and-closure masthead, partner logos, tricolor mark",
    ]
    for line in composition:
        s.append(Paragraph("&middot;&nbsp; " + line, BODY))

    s.append(Paragraph("Distinctive moves the visitor will remember", H3))
    distinctive = [
        "Kinyarwanda numerals on the Three Pillars",
        "Letter from Huye signed by the founder, replacing a conventional contact form",
        "Dated Projects log written like a society newsletter",
        "Tricolor Rwandan flag stripes as letterhead on editorial sections",
        "Adaptive navbar that swaps theme based on the section it floats over",
        "Static Rwanda flag image as the bottom-right footer punctuation",
        "AI chatbot mockup branded to the site, not a generic SaaS bubble",
    ]
    for line in distinctive:
        s.append(Paragraph("&middot;&nbsp; " + line, BODY))

    s.append(Paragraph("What the donor takes away", H3))
    s.append(Paragraph(
        "<i>This is a registered Rwandan organization, run by named "
        "Rwandan dental and medical professionals, with five concrete "
        "programs, real partners, real research output, and a path "
        "to fund a specific deployment. They published their "
        "registration code, their founding date, their address, and "
        "their team. They wrote me a signed letter. They are not "
        "asking for pity; they are inviting partnership.</i>",
        LEAD
    ))

    return s


# --- Build ----------------------------------------------------------

def main():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=LETTER,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.95 * inch,
        bottomMargin=0.85 * inch,
        title="RDMS Rwanda — Design & Strategy Summary",
        author="RDMS Rwanda",
        subject="Website design rationale",
    )
    story = build_story()
    doc.build(story, onFirstPage=first_page, onLaterPages=later_page)
    size = os.path.getsize(OUTPUT)
    print("Wrote {} ({:,} bytes)".format(OUTPUT, size))


if __name__ == "__main__":
    main()
