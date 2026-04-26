import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    r = urllib.request.urlopen('http://localhost:8080/', timeout=5)
    html = r.read().decode('utf-8')
    print(f'Local server OK — page size: {len(html)} bytes\n')
except Exception as e:
    print(f'Server error: {e}')
    sys.exit(1)

checks = [
    ('Webflow CSS (local)',        'assets/css/webflow.css'),
    ('Logo white (local)',         'assets/img/logo-white.png'),
    ('Logo dark (local)',          'assets/img/logo-dark.png'),
    ('Hero background video',      'assets/video/hero-bg.mp4'),
    ('Video poster image',         'assets/img/video-poster.jpg'),
    ('Mobile green image',         'assets/img/green.jpg'),
    ('UnicornStudio project',      'data-us-project="jlPiacgTTLEVKCfErDZe"'),
    ('GSAP (local)',               'assets/js/gsap.min.js'),
    ('ScrollTrigger (local)',      'assets/js/ScrollTrigger.min.js'),
    ('jQuery (local)',             'assets/js/jquery.min.js'),
    ('Webflow chunk1 (local)',     'assets/js/webflow.chunk1.js'),
    ('Webflow chunk2 (local)',     'assets/js/webflow.chunk2.js'),
    ('Webflow main (local)',       'assets/js/webflow.main.js'),
    ('Get in touch overlay',       'get-in-touch-overlay'),
    ('Overlay close button',       'class="close"'),
    ('Overlay form',               'id="email-form"'),
    ('Hero section',               'class="hero"'),
    ('Background video container', 'background-video-container'),
    ('Navbar',                     'class="navbar w-nav"'),
    ('Webflow IX data attrs',      'data-w-id="5da7e745'),
    ('Hero container',             'class="w-layout-blockcontainer hero-container'),
    ('Heading-12 desktop',         'class="heading-12">You belong'),
    ('Desktop headline area',      'headline-area-desktop'),
    ('Mobile headline area',       'headline-area-small'),
    ('Asheville event card',       'Blind Tiger'),
    ('NY event card',              'Black Box'),
    ('Event Eventbrite links',     'eventbrite.com'),
    ('Sponsor middle card',        'Sponsor Tech/ish in Your City'),
    ('About section desktop',      'about-container desktop'),
    ('About section mobile',       'about-container mobile'),
    ('Column scroll wrapper',      'column-scroll-wrapper'),
    ('Sponsor section anchor',     'id="Sponsor-tech"'),
    ('Column image char2',         'assets/img/char2.png'),
    ('Column image avl',           'assets/img/avl.png'),
    ('Column image new-york',      'assets/img/new-york.png'),
    ('Sponsor content title',      'Sponsor Tech/ish in your city'),
    ('Sponsor Why text',           'local, engaged'),
    ('Venue Sponsor text',         'Venue Sponsor'),
    ('Promotional Sponsor text',   'Promotional Sponsor'),
    ('Text call-out section',      'text-call-out homepage'),
    ('Pull up a chair quote',      'Pull up a chair'),
    ('image-6 gradient bg',        'image-6 dev homepage'),
    ('Footer div',                 'class="footer-div"'),
    ('Circle abstract',            'circle-abstract'),
    ('Ellipse image',              'assets/img/ellipse.svg'),
    ('Lets Connect',               "Let's Connect"),
    ('Connect with a human btn',   'Connect with a human'),
    ('Footer dark logo',           'assets/img/logo-dark.png'),
    ('Footer nav about link',      'href="/about"'),
    ('Footer nav events link',     'href="/events"'),
    ('Footer LinkedIn link',       'linkedin.com/company/tech-ish'),
    ('Custom script.js',           'src="script.js"'),
    ('GSAP clip-path animation',   'clipPath: "inset(0%'),
    ('Webfont Montserrat',         'Montserrat'),
    ('Webfont Google Sans',        'Google Sans'),
    ('Arrow white (local)',        'assets/img/arrow-white.png'),
    ('Arrow dark (local)',         'assets/img/arrow-dark.png'),
    ('IX initial states style',    'data-w-id="e2924a72'),
    ('IX3 visibility rule',        'w-mod-ix3'),
    ('Leaflet CSS (local)',        'assets/css/leaflet.css'),
    ('Webflow wf-domain attr',     'data-wf-domain="www.tech-ish.org"'),
    ('Favicon (local)',            'assets/img/favicon.png'),
]

passed = 0
failed = 0
for label, needle in checks:
    found = needle in html
    status = 'PASS' if found else 'FAIL'
    if found:
        passed += 1
    else:
        failed += 1
    print(f'  [{status}] {label}')

print(f'\n{passed}/{len(checks)} checks passed', end='')
if failed == 0:
    print(' — All good!')
else:
    print(f' — {failed} failed')
