"""
Generate static JSON API endpoints for the RDMS Rwanda site.

Single source of truth: the homepage HTML (FAQ entries, leadership
cards, services, projects) plus the canonical institutional facts
encoded below. Run this script before each deploy; it writes
deterministic JSON files into api/v1/ that AI agents can fetch.

Usage:
    python build_api.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
INDEX_HTML = ROOT / "index.html"
API_DIR = ROOT / "api" / "v1"
SITE_URL = "https://rdms-rwanda.vercel.app"

# --- Canonical institutional facts (single source of truth) ---------

ORGANIZATION = {
    "@id": f"{SITE_URL}/api/v1/organization.json",
    "name": "Dento-Medical Society Rwanda",
    "abbreviation": "RDMS",
    "type": "Non-Profit Limited by Guarantee",
    "founded": "2024-07-01",
    "registration": {
        "authority": "Rwanda Development Board (RDB)",
        "code": "143885158",
        "country": "RW"
    },
    "address": {
        "street": "Ngoma",
        "locality": "Huye",
        "region": "Amajyepfo (Southern Province)",
        "country": "Rwanda",
        "country_code": "RW"
    },
    "contact": {
        "phone": "+250791853120",
        "phone_display": "+250 791 853 120",
        "email": [
            "rdmspresident13@gmail.com",
            "igisubizojimmy@gmail.com"
        ],
        "languages": ["en", "rw", "fr"]
    },
    "social": {
        "twitter": "https://x.com/RDMS_rw",
        "twitter_handle": "@RDMS_rw",
        "instagram": "https://www.instagram.com/rdms_rw/",
        "linkedin": "https://www.linkedin.com/in/rdms-dento-medical-society-rwanda-24035029b",
        "tiktok": "https://www.tiktok.com/@rdmsrw"
    },
    "website": SITE_URL,
    "logo": f"{SITE_URL}/assets/img/rdms-logo.png",
    "mission": (
        "To unite dental surgeons, dental therapists, and public-"
        "health professionals in advancing oral-systemic health "
        "through collaborative education, research, outreach, and "
        "policy advocacy."
    ),
    "vision": (
        "To become a multidisciplinary center of excellence for the "
        "integration of oral health and general health in Rwanda, "
        "ensuring a healthier nation through unified care and "
        "innovation."
    ),
    "description": (
        "A non-profit professional society uniting dental surgeons, "
        "dental therapists, medical doctors, and public-health "
        "professionals to advance oral and public health across "
        "Rwanda."
    ),
    "area_served": "Rwanda",
    "topics": [
        "oral health",
        "dental medicine",
        "public health",
        "preventive dentistry",
        "oral-systemic health",
        "dental research",
        "ectodermal dysplasia",
        "school dental screenings",
        "community mobile clinics"
    ]
}

LEADERSHIP = [
    {
        "id": "igisubizo-jimmy-confiance",
        "name": "Igisubizo Jimmy Confiance",
        "role": "CEO & President",
        "is_founder": True,
        "discipline": "Dental Surgeon",
        "bio": (
            "Dental professional and public health advocate "
            "committed to transforming oral healthcare access "
            "across Rwanda. Founder and driving force behind RDMS "
            "since its establishment in 2024."
        ),
        "photo": f"{SITE_URL}/assets/img/team-igisubizo-jimmy.jpg"
    },
    {
        "id": "natukunda-sharon",
        "name": "Natukunda Sharon",
        "role": "General Secretary",
        "is_founder": False,
        "discipline": "Medicine",
        "photo": f"{SITE_URL}/assets/img/team-natukunda-sharon.jpg"
    },
    {
        "id": "dushimitanga-luc",
        "name": "Dushimitanga Luc",
        "role": "VP of Finance",
        "is_founder": False,
        "discipline": "Medicine",
        "photo": f"{SITE_URL}/assets/img/team-dushimitanga-luc.jpg"
    },
    {
        "id": "kubwimana-steven",
        "name": "Kubwimana Steven",
        "role": "VP of External Affairs",
        "is_founder": False,
        "discipline": "Dental Surgeon",
        "photo": f"{SITE_URL}/assets/img/team-kubwimana-steven.jpg"
    },
    {
        "id": "mbagoroziki-samuel",
        "name": "Mbagoroziki Samuel",
        "role": "VP of Internal Affairs",
        "is_founder": False,
        "discipline": "Dental Surgeon",
        "photo": f"{SITE_URL}/assets/img/team-mbagoroziki-samuel.jpg"
    }
]

SERVICES = [
    {
        "id": "school-screenings",
        "number": "01",
        "category": "Field Service",
        "name": "School-Based Dental Screenings",
        "description": (
            "Systematic dental screenings at primary and secondary "
            "schools across Rwanda. Teams arrive with portable "
            "equipment, assess students, identify untreated caries "
            "and developmental issues, and connect families with "
            "local follow-up care."
        ),
        "evidence": [
            "Active in primary and secondary schools in Huye District",
            "Portable equipment, free to community",
            "Follow-up referrals to local dental services"
        ]
    },
    {
        "id": "preventive-care",
        "number": "02",
        "category": "Education",
        "name": "Preventive Care Programs",
        "description": (
            "Daily oral health messaging, fluoride application "
            "sessions, hygiene kit distribution, and community "
            "workshops on brushing, diet, and dental habits."
        ),
        "evidence": []
    },
    {
        "id": "research",
        "number": "03",
        "category": "Research",
        "name": "Oral Health Research & Data Collection",
        "description": (
            "Cross-sectional studies on disease prevalence, care "
            "access, and health behaviours across Rwanda. RDMS "
            "partners with academic institutions, hospitals, and "
            "international research bodies."
        ),
        "evidence": []
    },
    {
        "id": "mobile-clinics",
        "number": "04",
        "category": "Outreach",
        "name": "Community Mobile Clinics",
        "description": (
            "Mobile dental units deployed into underserved rural "
            "and peri-urban communities. Free examinations, "
            "extractions, fluoride treatment, and oral hygiene "
            "supplies."
        ),
        "evidence": [
            "Active across rural districts",
            "Free dental examinations and extractions",
            "Oral hygiene supplies distributed on-site"
        ]
    },
    {
        "id": "research-academy",
        "number": "05",
        "category": "Knowledge",
        "name": "RDMS Research Academy",
        "description": (
            "Curated research lessons and continuing professional "
            "development for dental and health professionals."
        ),
        "evidence": []
    },
    {
        "id": "chronicles",
        "number": "06",
        "category": "Publication",
        "name": "Dental Medicine Chronicles",
        "description": (
            "Clinical case studies, public health updates, and "
            "policy commentary from Rwandan dental and medical "
            "professionals."
        ),
        "evidence": []
    }
]

PROJECTS = {
    "active": [
        {
            "id": "oral-systemic-baseline-2025-2026",
            "category": "Research",
            "name": "Oral-Systemic Health Baseline Study, Rwanda",
            "description": (
                "A cross-sectional research study documenting the "
                "prevalence of dental conditions and their systemic "
                "health correlations in Rwandan adults."
            ),
            "date": "2025-2026",
            "date_iso": "2025"
        },
        {
            "id": "daily-messaging-2026",
            "category": "Preventive Care",
            "name": "Daily Oral Health Messaging Campaign",
            "description": (
                "Automated daily preventive care messages "
                "distributed to community members via SMS and "
                "social media platforms."
            ),
            "date": "Ongoing 2026",
            "date_iso": "2026"
        },
        {
            "id": "huye-screening-q1-2026",
            "category": "Screenings",
            "name": "Huye District School Dental Screening Drive",
            "description": (
                "Systematic oral health screenings across 7 primary "
                "schools in Huye District, identifying untreated "
                "caries and periodontal conditions."
            ),
            "date": "Q1 2026",
            "date_iso": "2026-Q1"
        }
    ],
    "completed": [
        {
            "id": "world-ed-day-2026",
            "category": "Awareness",
            "name": "World Ectodermal Dysplasia Day 2026",
            "description": (
                "Community awareness event raising support for "
                "individuals and families affected by Ectodermal "
                "Dysplasia in Rwanda and beyond."
            ),
            "date": "20 Feb 2026",
            "date_iso": "2026-02-20"
        }
    ],
    "planned": [
        {
            "id": "mobile-clinic-q1-2026",
            "category": "Outreach",
            "name": "Mobile Dental Clinic, Rural Outreach Q1",
            "description": (
                "Mobile dental unit providing free extractions, "
                "fluoride treatment, and oral hygiene kits to "
                "communities in underserved areas."
            ),
            "date": "March 2026",
            "date_iso": "2026-03"
        },
        {
            "id": "interdisciplinary-workshop-q2-2026",
            "category": "Training",
            "name": "Interdisciplinary Health Workshop Series",
            "description": (
                "Training workshops for dental and medical "
                "professionals on integrating oral and systemic "
                "health in patient care."
            ),
            "date": "Q2 2026",
            "date_iso": "2026-Q2"
        }
    ]
}

# --- FAQ extraction from index.html ---------------------------------

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    text = re.sub(r"[-\s]+", "-", text)
    return text


def extract_faq() -> tuple[list, list]:
    """Parse the FAQ section out of index.html. Returns (categories, items)."""
    if not INDEX_HTML.exists():
        sys.exit(f"index.html not found at {INDEX_HTML}")
    soup = BeautifulSoup(INDEX_HTML.read_text(encoding="utf-8"), "html.parser")
    sections = soup.select("section.faq__category")
    categories = []
    items = []
    item_id = 0
    for sec in sections:
        cat_id = sec.get("id", "").replace("faq-", "")
        heading_el = sec.select_one(".faq__category-heading")
        if not heading_el:
            continue
        cat_name = heading_el.get_text(strip=True)
        cat_items = []
        for entry in sec.select(".faq__item"):
            q_el = entry.select_one(".faq__question")
            a_el = entry.select_one(".faq__answer")
            if not q_el or not a_el:
                continue
            item_id += 1
            entry_data = {
                "id": item_id,
                "category_id": cat_id,
                "category": cat_name,
                "question": q_el.get_text(strip=True),
                # plain text answer (links flattened to URLs in parens)
                "answer": _flatten_links(a_el),
                "answer_html": a_el.decode_contents().strip()
            }
            items.append(entry_data)
            cat_items.append(item_id)
        categories.append({
            "id": cat_id,
            "name": cat_name,
            "count": len(cat_items),
            "item_ids": cat_items
        })
    return categories, items


def _flatten_links(node) -> str:
    """Convert <a href="...">text</a> → 'text (url)' for plain-text answer."""
    parts = []
    for child in node.children:
        if getattr(child, "name", None) == "a":
            text = child.get_text(strip=True)
            href = child.get("href", "")
            if href and href != text:
                parts.append(f"{text} ({href})")
            else:
                parts.append(text)
        elif getattr(child, "name", None) == "br":
            parts.append(" ")
        else:
            parts.append(getattr(child, "get_text", lambda: str(child))() if hasattr(child, "get_text") else str(child))
    return re.sub(r"\s+", " ", "".join(parts)).strip()


# --- Endpoint document construction ---------------------------------

def make_meta() -> dict:
    return {
        "generated": date.today().isoformat(),
        "license": "Public — facts about a registered Rwandan non-profit",
        "source": SITE_URL,
        "schema_version": "v1"
    }


def build_index_doc(faq_categories) -> dict:
    return {
        "name": "RDMS Rwanda Public API",
        "description": (
            "Read-only JSON endpoints with institutional facts about "
            "the Dento-Medical Society Rwanda. AI-friendly: no auth, "
            "permissive CORS, deterministic schema, generated from the "
            "homepage content at deploy time."
        ),
        "version": "v1",
        "documentation": f"{SITE_URL}/api/v1/openapi.json",
        "endpoints": [
            {"name": "Organization", "url": f"{SITE_URL}/api/v1/organization.json"},
            {"name": "Leadership", "url": f"{SITE_URL}/api/v1/leadership.json"},
            {"name": "Services", "url": f"{SITE_URL}/api/v1/services.json"},
            {"name": "Projects", "url": f"{SITE_URL}/api/v1/projects.json"},
            {"name": "FAQ — full list", "url": f"{SITE_URL}/api/v1/faq.json"},
            {"name": "FAQ — categories", "url": f"{SITE_URL}/api/v1/faq/categories.json"},
        ],
        "_meta": make_meta()
    }


def build_openapi(faq_count: int) -> dict:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "RDMS Rwanda Public API",
            "version": "1.0.0",
            "description": (
                "Read-only JSON endpoints with institutional facts "
                "about RDMS (Dento-Medical Society Rwanda). Static "
                "files; no auth required; permissive CORS."
            ),
            "contact": {
                "name": "RDMS Rwanda",
                "email": "rdmspresident13@gmail.com",
                "url": SITE_URL
            },
            "license": {
                "name": "Public — facts about a registered non-profit"
            }
        },
        "servers": [{"url": f"{SITE_URL}/api/v1", "description": "Production"}],
        "paths": {
            "/index.json": {
                "get": {
                    "summary": "API root index",
                    "description": "List of endpoints and metadata.",
                    "responses": {"200": {"description": "Index document"}}
                }
            },
            "/organization.json": {
                "get": {
                    "summary": "Organization facts",
                    "description": "Institutional registration, contact, address, mission, vision, social.",
                    "responses": {"200": {"description": "Organization document"}}
                }
            },
            "/leadership.json": {
                "get": {
                    "summary": "Leadership roster",
                    "description": "Five named leaders with role, discipline, founder flag.",
                    "responses": {"200": {"description": "List of leaders"}}
                }
            },
            "/services.json": {
                "get": {
                    "summary": "Six core services",
                    "description": "Programs offered: screenings, preventive care, research, mobile clinics, Academy, Chronicles.",
                    "responses": {"200": {"description": "List of services"}}
                }
            },
            "/projects.json": {
                "get": {
                    "summary": "Activity log",
                    "description": "Active, completed, and planned project entries grouped by status.",
                    "responses": {"200": {"description": "Projects grouped by status"}}
                }
            },
            "/faq.json": {
                "get": {
                    "summary": f"All {faq_count} FAQ entries",
                    "description": "Question, answer (plain text + html), category metadata.",
                    "responses": {"200": {"description": "List of FAQ items"}}
                }
            },
            "/faq/categories.json": {
                "get": {
                    "summary": "FAQ categories",
                    "description": "Nine category groups with item counts.",
                    "responses": {"200": {"description": "List of categories"}}
                }
            }
        }
    }


# --- Writer ---------------------------------------------------------

def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"  wrote {path.relative_to(ROOT)} ({path.stat().st_size:,} bytes)")


# --- Main -----------------------------------------------------------

def main() -> int:
    print(f"Building API into {API_DIR.relative_to(ROOT)}/ ...")
    categories, items = extract_faq()
    print(f"  parsed {len(categories)} FAQ categories, {len(items)} FAQ items")

    write_json(
        API_DIR / "organization.json",
        {**ORGANIZATION, "_meta": make_meta()}
    )
    write_json(
        API_DIR / "leadership.json",
        {"leaders": LEADERSHIP, "_meta": make_meta()}
    )
    write_json(
        API_DIR / "services.json",
        {"services": SERVICES, "_meta": make_meta()}
    )
    write_json(
        API_DIR / "projects.json",
        {**PROJECTS, "_meta": make_meta()}
    )
    write_json(
        API_DIR / "faq.json",
        {"items": items, "count": len(items), "_meta": make_meta()}
    )
    write_json(
        API_DIR / "faq" / "categories.json",
        {"categories": categories, "_meta": make_meta()}
    )
    write_json(
        API_DIR / "index.json",
        build_index_doc(categories)
    )
    write_json(
        API_DIR / "openapi.json",
        build_openapi(len(items))
    )

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
