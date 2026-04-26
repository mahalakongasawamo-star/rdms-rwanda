import urllib.request, re, sys

sys.stdout.reconfigure(encoding='utf-8')

r = urllib.request.urlopen('https://cdn.prod.website-files.com/6984c1d3abec40cf208336a4/css/tech-ish.webflow.shared.7c88d1d15.css')
css = r.read().decode('utf-8')

# Find :root CSS variables
root_match = re.search(r':root\s*\{([^}]+)\}', css)
if root_match:
    print('=== ROOT VARIABLES ===')
    print(root_match.group())
    print()

# Find specific classes
targets = [
    'card-4', 'hero', 'heading-12', 'heading-6', 'bug',
    'circle-abstract', 'circle-dots', 'image-6', 'text-call-out',
    'heading-7', 'get-in-touch-overlay', 'line-breaker',
    'column-scroll-wrapper', 'column-scroll-sticky-inner',
    'column-scroll-image', 'cards', 'you-belong', 'in-ai',
    'headline-area-desktop', 'headline-area-small',
    'background-video-2', 'background-video-container',
    'mobile-image', 'heading-8', 'sign-up-link-block',
    'footer', 'image-4', 'circle-color'
]

for cls in targets:
    pattern = r'\.' + re.escape(cls) + r'(?:[^{]*)?\{([^}]+)\}'
    matches = re.findall(pattern, css)
    if matches:
        print(f'=== .{cls} ===')
        for m in matches[:3]:
            print(m.strip()[:500])
        print()

# Also print the last 20000 chars of CSS for media queries
print('\n=== LAST SECTION (media queries) ===')
print(css[-25000:-15000])
