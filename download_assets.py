"""
Tech/ish asset downloader — downloads all images, CSS, and JS for local serving.
Run: python download_assets.py
"""
import urllib.request
import os
import sys
import time

BASE_CDN = "https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/"
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(f"{ASSETS_DIR}/css", exist_ok=True)
os.makedirs(f"{ASSETS_DIR}/js", exist_ok=True)
os.makedirs(f"{ASSETS_DIR}/img", exist_ok=True)
os.makedirs(f"{ASSETS_DIR}/video", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.tech-ish.org/"
}

def download(url, local_path, label=""):
    if os.path.exists(local_path):
        print(f"  [skip] {label or local_path} (already exists)")
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(local_path, "wb") as f:
            f.write(data)
        size = len(data) / 1024
        print(f"  [ok]   {label or local_path} ({size:.1f} KB)")
        return True
    except Exception as e:
        print(f"  [fail] {label or local_path}: {e}")
        return False

print("=== Downloading images ===")
images = [
    ("698f668936b34a48e71544e8_Logo-white.png",      "img/logo-white.png"),
    ("69962ad8fcfbcc4a46521405_Logo-dark.png",       "img/logo-dark.png"),
    ("6990bf5e35957c5425cbf6d3_Arrow%201-white.png", "img/arrow-white.png"),
    ("6990b9fc6dc902dbeb43b29f_Arrow%201.png",       "img/arrow-dark.png"),
    ("69935f679a6f30136442fade_green.jpg",           "img/green.jpg"),
    ("69a85c24c82425565a4e3ddc_char2.png",           "img/char2.png"),
    ("69a85c032aa74833329f054e_avl.png",             "img/avl.png"),
    ("69a85c7a1054a15085158eb4_new%20york-new.png",  "img/new-york.png"),
    ("698f803b5bbcba62c781f672_Ellipse-1.svg",       "img/ellipse.svg"),
    ("699c7b6503215c6f85d6e0b5_x.png",               "img/close-x.png"),
    ("699c9a5563011311ccd4d2d2_linkedin.png",         "img/linkedin.png"),
    ("69a8d711470d43b69aa52854_Favicon-small-green.png", "img/favicon.png"),
    ("69a84ed00b4332680d92cc43_Favicon-large.webp",  "img/favicon-large.webp"),
    ("69ac644f6498982a054e269f_Image%20Graph.png",   "img/og-image.png"),
    ("69a84c75703ced3e4928b5bd_flow_gradient_remix%20copy%202_poster.0000000.jpg", "img/video-poster.jpg"),
    ("699899deed22444313237ac9_flow_gradient_remix%20copy.jpeg", "img/bg-gradient.jpeg"),
    ("69ac651225b440f5ee8d7719_gradient.jpeg",        "img/gradient.jpeg"),
    ("69920580a385e4d6c08fdb74_asheville-events.png", "img/asheville-events.png"),
    ("699c9a5563011311ccd4d2d2_linkedin.png",          "img/linkedin.png"),
    # Green image srcset variants
    ("69935f679a6f30136442fade_green-p-500.jpg",      "img/green-p-500.jpg"),
    ("69935f679a6f30136442fade_green-p-800.jpg",      "img/green-p-800.jpg"),
    ("69935f679a6f30136442fade_green-p-1080.jpg",     "img/green-p-1080.jpg"),
]

for cdn_path, local in images:
    download(BASE_CDN + cdn_path, f"{ASSETS_DIR}/{local}", local)
    time.sleep(0.1)

print("\n=== Downloading CSS ===")
css_files = [
    (
        "https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/css/tech-ish.webflow.shared.7c88d1d15.css",
        "css/webflow.css"
    ),
]
for url, local in css_files:
    download(url, f"{ASSETS_DIR}/{local}", local)
    time.sleep(0.2)

print("\n=== Downloading JS ===")
js_files = [
    (
        "https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=6984c1d3abec40cf208336a4",
        "js/jquery.min.js"
    ),
    (
        "https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/js/webflow.schunk.36b8fb49256177c8.js",
        "js/webflow.chunk1.js"
    ),
    (
        "https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/js/webflow.schunk.1d6e3072cb432cf9.js",
        "js/webflow.chunk2.js"
    ),
    (
        "https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/js/webflow.ebb45c2a.4a47afd4b5fad44c.js",
        "js/webflow.main.js"
    ),
    (
        "https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js",
        "js/webfont.js"
    ),
    (
        "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js",
        "js/gsap.min.js"
    ),
    (
        "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js",
        "js/ScrollTrigger.min.js"
    ),
    (
        "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js",
        "js/leaflet.js"
    ),
    (
        "https://unpkg.com/leaflet.markercluster/dist/leaflet.markercluster.js",
        "js/leaflet.markercluster.js"
    ),
]
for url, local in js_files:
    download(url, f"{ASSETS_DIR}/{local}", local)
    time.sleep(0.2)

print("\n=== Downloading Leaflet CSS ===")
leaflet_css = [
    ("https://unpkg.com/leaflet@1.7.1/dist/leaflet.css", "css/leaflet.css"),
    ("https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.css", "css/MarkerCluster.css"),
    ("https://unpkg.com/leaflet.markercluster/dist/MarkerCluster.Default.css", "css/MarkerCluster.Default.css"),
]
for url, local in leaflet_css:
    download(url, f"{ASSETS_DIR}/{local}", local)
    time.sleep(0.1)

print("\n=== Downloading video (this may take a while) ===")
video_url = "https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/69a84c75703ced3e4928b5bd_flow_gradient_remix%20copy%202_mp4.mp4"
download(video_url, f"{ASSETS_DIR}/video/hero-bg.mp4", "video/hero-bg.mp4")

print("\n=== All done! ===")
