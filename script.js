/* ================================================================
   Tech/ish — Local clone script.js
   Handles:
     1. Webflow IX2/IX3 failsafe (GSAP-driven entrance animations)
     2. Column-scroll 3-panel image reveal (GSAP ScrollTrigger)
     3. Hero background-video clip-path reveal (GSAP ScrollTrigger)
     4. Get-in-touch overlay open/close
     5. Video autoplay fallback
     6. Event card hover dimming
   ================================================================ */

(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var html = document.documentElement;

    /* ----------------------------------------------------------------
       STEP 1 — Add BOTH ix classes immediately and unconditionally.

       This deactivates every Webflow IX CSS rule (the "not(.w-mod-ix)"
       selectors) so all elements become naturally visible.
       If GSAP never loads, the page is STILL fully readable.
       GSAP will then set its own opacity:0 start states via gsap.set().
    ---------------------------------------------------------------- */
    html.classList.add('w-mod-ix3');
    html.classList.add('w-mod-ix');


    /* ----------------------------------------------------------------
       STEP 2 — GSAP animations (entrance + scroll effects)
    ---------------------------------------------------------------- */
    if (typeof gsap !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);

      var navbar        = document.querySelector('[data-w-id="5da7e745-947d-7935-3d60-e1a815c44aed"]');
      var heroContainer = document.querySelector('[data-w-id="e2924a72-ee95-a190-5f45-b013228b7d00"]');

      /* Set initial hidden states via GSAP (CSS IX rules are already off) */
      if (navbar)        gsap.set(navbar,        { opacity: 0 });
      if (heroContainer) gsap.set(heroContainer,  { opacity: 0, scale: 0.75 });

      /* Navbar — fade in */
      if (navbar) {
        gsap.to(navbar, {
          opacity:  1,
          duration: 0.6,
          ease:     'power2.out',
          delay:    0.2
        });
      }

      /* Hero container — scale 0.75 → 1, opacity 0 → 1 */
      if (heroContainer) {
        gsap.to(heroContainer, {
          opacity:  1,
          scale:    1,
          duration: 1.1,
          ease:     'power3.out',
          delay:    0.4
        });
      }


      /* HERO BACKGROUND VIDEO clip-path reveal — REMOVED. The reveal
         was clipping the video to a tiny pill in the middle and
         leaving the rest of the hero looking opaque-black. The video
         now shows full from page load. */


      /* ----------------------------------------------------------------
         FOOTER CIRCLE — subtle pulse on scroll into view
      ---------------------------------------------------------------- */
      var circleDots = document.querySelector('.circle-dots.large');
      if (circleDots) {
        gsap.fromTo(circleDots,
          { scale: 1.1, opacity: 0.4 },
          {
            scale:    1,
            opacity:  1,
            duration: 1.2,
            ease:     'power2.out',
            scrollTrigger: {
              trigger:       '.footer-div',
              start:         'top 80%',
              toggleActions: 'play none none reverse'
            }
          }
        );
      }

      /* ----------------------------------------------------------------
         TEXT CALL-OUT — heading fade-up on scroll
      ---------------------------------------------------------------- */
      var calloutHeading = document.querySelector('.heading-6');
      if (calloutHeading) {
        gsap.fromTo(calloutHeading,
          { opacity: 0, y: 40 },
          {
            opacity:  1,
            y:        0,
            duration: 0.9,
            ease:     'power2.out',
            scrollTrigger: {
              trigger:       calloutHeading,
              start:         'top 80%',
              toggleActions: 'play none none reverse'
            }
          }
        );
      }

    }
    /* If GSAP is absent, w-mod-ix was already added above → page fully visible. */


    /* ----------------------------------------------------------------
       GET IN TOUCH OVERLAY
    ---------------------------------------------------------------- */
    var overlay = document.querySelector('.get-in-touch-overlay');
    var closeEl = document.querySelector('.close');
    var openers = [
      document.getElementById('getInTouchNavBtn'),
      document.getElementById('getInTouchMobileLink'),
      document.getElementById('sponsorGetInTouchBtn'),
      document.getElementById('servicesCtaBtn'),
      document.getElementById('chroniclesSubscribeBtn'),
      document.getElementById('contactWriteBtn'),
      document.getElementById('navWriteBtn'),
      document.getElementById('heroPartnerBtn')
    ];

    function openOverlay(e) {
      if (e) e.preventDefault();
      if (!overlay) return;
      overlay.style.display   = 'flex';
      overlay.style.opacity   = '0';
      overlay.style.transform = 'translate3d(60px, 0, 0)';
      overlay.style.transition = '';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          overlay.style.transition = 'opacity 0.45s cubic-bezier(0.16,1,0.3,1), transform 0.45s cubic-bezier(0.16,1,0.3,1)';
          overlay.style.opacity    = '1';
          overlay.style.transform  = 'translate3d(0, 0, 0)';
        });
      });
    }

    function closeOverlay() {
      if (!overlay) return;
      overlay.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      overlay.style.opacity    = '0';
      overlay.style.transform  = 'translate3d(60px, 0, 0)';
      setTimeout(function () {
        overlay.style.display    = 'none';
        overlay.style.transition = '';
      }, 320);
    }

    openers.forEach(function (el) {
      if (el) el.addEventListener('click', openOverlay);
    });
    if (closeEl) closeEl.addEventListener('click', closeOverlay);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeOverlay();
    });


    /* ----------------------------------------------------------------
       HERO VIDEO AUTOPLAY
       Chrome checks the JS .muted property (not just the HTML attr).
       Webflow's w-background-video handler can reset .muted to false,
       blocking autoplay. We force muted=true, then call play().
       A rAF deferral gives Webflow's init one tick to finish first.
    ---------------------------------------------------------------- */
    var heroVideos = [
      document.getElementById('hero-video'),            /* background-video-2 (hidden fallback) */
      document.querySelector('.hero-bg-video'),         /* clip-path hero background            */
      document.querySelector('.sponsor-bg-video'),      /* sponsor-tech section background      */
      document.querySelector('.academy__bg-video'),     /* academy section background           */
      document.querySelector('.contact__bg-video'),     /* contact section background           */
      document.querySelector('.hero__photo-video')      /* hero right-side photo video          */
    ];

    function forcePlay(vid) {
      if (!vid) return;
      vid.muted  = true;
      vid.loop   = true;
      vid.volume = 0;
      var pp = vid.play();
      if (pp !== undefined) {
        pp.catch(function () {
          /* Blocked — retry on ANY first user interaction */
          var unlockEvents = ['click', 'touchstart', 'keydown', 'scroll', 'wheel'];
          function unlock() {
            vid.muted = true;
            vid.play();
            unlockEvents.forEach(function (ev) {
              document.removeEventListener(ev, unlock, true);
            });
          }
          unlockEvents.forEach(function (ev) {
            document.addEventListener(ev, unlock, { once: true, capture: true });
          });
        });
      }
    }

    /* Defer one frame so Webflow's init finishes before we play */
    requestAnimationFrame(function () {
      heroVideos.forEach(forcePlay);
    });



    /* ----------------------------------------------------------------
       CARD HOVER — dim siblings on hover
    ---------------------------------------------------------------- */
    var cards = document.querySelectorAll('.card-4.sibling_link-item');
    cards.forEach(function (card) {
      card.addEventListener('mouseenter', function () {
        cards.forEach(function (s) {
          if (s !== card) {
            s.style.opacity    = '0.55';
            s.style.transform  = 'scale(0.97)';
            s.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
          }
        });
      });
      card.addEventListener('mouseleave', function () {
        cards.forEach(function (s) {
          s.style.opacity   = '';
          s.style.transform = '';
        });
      });
    });

    /* ----------------------------------------------------------------
       COLUMN SCROLL — sequential Y-stagger triptych reveal.
       Webflow IX data-w-id was removed from the wrapper so IX never
       touches these items; GSAP has exclusive control.
       requestAnimationFrame lets Webflow IX apply its 100vw inline
       style to the inner before we read layout / set transforms.
    ---------------------------------------------------------------- */
  }); // end ready()

  /* ----------------------------------------------------------------
     COLUMN SCROLL — sequential Y-stagger triptych reveal.
     Runs at window load (after all resources + Webflow IX init).
     data-w-id removed from wrapper in HTML → IX never touches items.
     inner width forced to 100vw via CSS → items tile as equal thirds.
  ---------------------------------------------------------------- */
  (function initColScroll() {
    function run() {
      if (typeof gsap === 'undefined' || window.innerWidth < 992) return;

      var wrapper     = document.querySelector('.column-scroll-wrapper');
      var stickyInner = document.querySelector('.column-scroll-sticky-inner');
      if (!wrapper || !stickyInner) return;

      var is1 = stickyInner.querySelector('.column-scroll-item.is-1');
      var is2 = stickyInner.querySelector('.column-scroll-item.is-2');
      var is3 = stickyInner.querySelector('.column-scroll-item.is-3');
      if (!is1 && !is2 && !is3) return;

      /* Park all items fully below the panel (overflow:hidden hides them). */
      [is1, is2, is3].forEach(function (el) {
        if (el) gsap.set(el, { y: '110%' });
      });

      var sectionScroll = wrapper.offsetHeight - window.innerHeight;

      /* ── Phase 1: Y-stagger — images rise from below, finishing in
         the first 40 % of section scroll so all three are fully
         revealed before the fan-compress in Phase 2 begins. ─────────── */
      var tl = gsap.timeline({
        scrollTrigger: {
          trigger: wrapper,
          start:   'top top',
          end:     'top+=' + Math.round(sectionScroll * 0.40) + ' top',
          scrub:   0.5
        }
      });

      if (is1) tl.to(is1, { y: 0, ease: 'none', duration: 0.40 }, 0.00);
      if (is2) tl.to(is2, { y: 0, ease: 'none', duration: 0.45 }, 0.20);
      if (is3) tl.to(is3, { y: 0, ease: 'none', duration: 0.50 }, 0.40);

      /* ── Phase 2: Per-item fanned overlap (45 % → 65 % of scroll).
         Items shift right by different amounts so they end up
         fanned/stacked on the right ~50 % of the viewport, leaving
         the left ~50 % clear for the text panel.
           is-1 (natural left)   → +50vw  : back of stack, leftmost peek
           is-2 (natural middle) → +27vw  : middle of stack
           is-3 (natural right)  → +3vw   : front of stack, mostly visible
         Deferred one rAF so ScrollTrigger's refresh() (fired by the Y
         timeline above) completes before we add the second ST. ─────── */
      var _wrapper = wrapper;
      requestAnimationFrame(function () {
        var phase2 = gsap.timeline({
          scrollTrigger: {
            trigger: _wrapper,
            start:   'top+=' + Math.round(sectionScroll * 0.45) + ' top',
            end:     'top+=' + Math.round(sectionScroll * 0.65) + ' top',
            scrub:   0.5
          }
        });

        if (is1) phase2.to(is1, { x: '50vw', ease: 'none' }, 0);
        if (is2) phase2.to(is2, { x: '27vw', ease: 'none' }, 0);
        if (is3) phase2.to(is3, { x: '3vw',  ease: 'none' }, 0);
      });
    }

    if (document.readyState === 'complete') {
      run();
    } else {
      window.addEventListener('load', run, { once: true });
    }
  }());

})();

/* ================================================================
   COLLAPSE-ON-SCROLL NAVBAR
   Vanilla port of the framer-motion behavior:
   - Scroll DOWN past 150px → collapse (.is-collapsed class)
   - Scroll UP 80px from collapse point → expand
   - Click the collapsed circle → expand
   Disabled below 992px (Webflow's mobile pattern owns small viewports).
   ================================================================ */
(function () {
  'use strict';

  var navbar = document.querySelector('.navbar.w-nav');
  if (!navbar) return;

  var COLLAPSE_THRESHOLD = 150;
  var EXPAND_THRESHOLD = 80;
  var DESKTOP_QUERY = window.matchMedia('(min-width: 992px)');

  var lastScrollY = window.scrollY || 0;
  var collapsedAt = 0;
  var isCollapsed = false;
  var ticking = false;

  function setCollapsed(next) {
    if (next === isCollapsed) return;
    isCollapsed = next;
    navbar.classList.toggle('is-collapsed', next);
  }

  function update() {
    if (!DESKTOP_QUERY.matches) {
      // Below 992px: ensure expanded state and skip scroll handling.
      if (isCollapsed) setCollapsed(false);
      ticking = false;
      return;
    }

    var currentY = window.scrollY || 0;
    var direction = currentY > lastScrollY ? 'down' : 'up';

    if (!isCollapsed && direction === 'down' && currentY > COLLAPSE_THRESHOLD) {
      collapsedAt = currentY;
      setCollapsed(true);
    } else if (isCollapsed && direction === 'up' && (collapsedAt - currentY) > EXPAND_THRESHOLD) {
      setCollapsed(false);
    }

    // Always expand at the very top.
    if (currentY < 30 && isCollapsed) setCollapsed(false);

    lastScrollY = currentY;
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });

  // Click the collapsed circle to expand back manually.
  navbar.addEventListener('click', function (e) {
    if (isCollapsed) {
      e.preventDefault();
      setCollapsed(false);
    }
  });

  // If the viewport crosses the breakpoint, re-evaluate.
  DESKTOP_QUERY.addEventListener
    ? DESKTOP_QUERY.addEventListener('change', update)
    : DESKTOP_QUERY.addListener(update);
})();

/* PROJECTS FILTER TABS — removed.
   The Projects section was redesigned as a press-release-log activity
   log grouped by status (Active Now / Recently Completed / Coming
   Next). Status is visible via grouping; no filter UI. The original
   30-line click-to-filter IIFE was deleted as part of that craft. */

/* (was: CONTACT FORM mailto handler — removed in Letter from Huye craft.
   The inline 6-field form is gone; the Write to RDMS button on the
   Contact section opens the get-in-touch overlay via the openers
   array above, same as every other "Send Message" button on the page.) */

/* ================================================================
   REVEAL-ON-SCROLL — fade-in + slight zoom on .reveal-photo elements
   when they enter the viewport. Paired with CSS in local-overrides.css.
   prefers-reduced-motion: skip observer, mark all visible immediately.
   ================================================================ */
(function () {
  'use strict';

  var targets = document.querySelectorAll('.reveal-photo');
  if (!targets.length) return;

  var prefersReduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReduced || !('IntersectionObserver' in window)) {
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
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  targets.forEach(function (el) { observer.observe(el); });
})();

/* ================================================================
   MOBILE MENU OVERLAY
   Open via the hamburger button (.navbar-mobile-toggle), close via
   the X button, the backdrop, the Esc key, or any link click.
   ================================================================ */
(function () {
  'use strict';

  var toggle   = document.querySelector('.navbar-mobile-toggle');
  var menu     = document.getElementById('mobileMenu');
  var backdrop = document.querySelector('.mobile-menu__backdrop');
  if (!toggle || !menu) return;

  var closeBtn = menu.querySelector('.mobile-menu__close');
  var links    = menu.querySelectorAll('.mobile-menu__link');

  function openMenu() {
    menu.classList.add('is-open');
    if (backdrop) backdrop.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    menu.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    menu.classList.remove('is-open');
    if (backdrop) backdrop.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  toggle.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (backdrop) backdrop.addEventListener('click', closeMenu);

  links.forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) {
      closeMenu();
    }
  });
})();

/* ================================================================
   NAVBAR ACTIVE-SECTION + ADAPTIVE THEME
   Two IntersectionObservers, one for each concern, both reading
   data-nav-theme attributes set on each section.

   - Observer A: tracks which section is currently dominant in the
     viewport (highest intersectionRatio); sets data-active="true"
     on the matching nav link (matched by href).
   - Observer B: tracks each section's data-nav-theme; the dominant
     section's theme is mirrored onto .navbar via [data-nav-theme].

   Skipped when prefers-reduced-motion is set (theme still swaps,
   but observation runs without animation jitter — actual transition
   timing is handled by CSS, which respects the media query).
   ================================================================ */
(function () {
  'use strict';

  var navbar = document.querySelector('.navbar.w-nav');
  if (!navbar || !('IntersectionObserver' in window)) return;

  var sections = document.querySelectorAll('[data-nav-theme]');
  if (!sections.length) return;

  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.navbar.w-nav .nav-link[href^="#"]')
  );

  /* Track every section's current visibility ratio so we can pick the
     dominant one synchronously on each observer callback. Avoids the
     "first matched section wins" bug that single-target observers hit. */
  var ratios = new WeakMap();
  sections.forEach(function (s) { ratios.set(s, 0); });

  function pickDominant() {
    var best = null;
    var bestRatio = 0;
    sections.forEach(function (s) {
      var r = ratios.get(s) || 0;
      if (r > bestRatio) {
        bestRatio = r;
        best = s;
      }
    });
    return best;
  }

  var lastTheme = navbar.getAttribute('data-nav-theme') || 'dark';
  var lastActiveHref = null;

  function applyDominant() {
    var dominant = pickDominant();
    if (!dominant) return;

    /* Theme adaptation. */
    var theme = dominant.getAttribute('data-nav-theme') || 'dark';
    if (theme !== lastTheme) {
      navbar.setAttribute('data-nav-theme', theme);
      lastTheme = theme;
    }

    /* Active-link state. Match section.id to nav link href. */
    var sectionId = dominant.id;
    var targetHref = sectionId ? '#' + sectionId : null;
    if (targetHref !== lastActiveHref) {
      navLinks.forEach(function (link) {
        if (link.getAttribute('href') === targetHref) {
          link.setAttribute('data-active', 'true');
        } else {
          link.removeAttribute('data-active');
        }
      });
      lastActiveHref = targetHref;
    }
  }

  var rafScheduled = false;
  function scheduleApply() {
    if (rafScheduled) return;
    rafScheduled = true;
    requestAnimationFrame(function () {
      rafScheduled = false;
      applyDominant();
    });
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        ratios.set(entry.target, entry.intersectionRatio);
      });
      scheduleApply();
    },
    {
      /* Account for the floating navbar height at the top.
         Threshold steps so the dominant section flips smoothly. */
      rootMargin: '-72px 0px -40% 0px',
      threshold: [0, 0.1, 0.25, 0.5, 0.75, 1]
    }
  );

  sections.forEach(function (s) { observer.observe(s); });
})();

/* ============================================================
   CREDO CAROUSEL — prev/next arrow buttons
   Vanilla port of the Embla canScrollPrev / canScrollNext API.
   Buttons enable/disable based on the rail's scrollLeft; clicking
   advances by one card-width + gap. Section: .about-credo
   ============================================================ */
(function () {
  var section = document.querySelector('.about-credo');
  if (!section) return;
  var rail = section.querySelector('.about-credo__rail');
  var prev = section.querySelector('.about-credo__btn[data-dir="prev"]');
  var next = section.querySelector('.about-credo__btn[data-dir="next"]');
  if (!rail || !prev || !next) return;

  function update() {
    var max = rail.scrollWidth - rail.clientWidth;
    prev.disabled = rail.scrollLeft <= 1;
    next.disabled = rail.scrollLeft >= max - 1;
  }

  function step(dir) {
    var card = rail.querySelector('.about-credo__item');
    var gap = parseFloat(getComputedStyle(rail.querySelector('.about-credo__track')).columnGap) || 16;
    var stride = card ? card.getBoundingClientRect().width + gap : rail.clientWidth * 0.7;
    rail.scrollBy({ left: dir * stride, behavior: 'smooth' });
  }

  prev.addEventListener('click', function () { step(-1); });
  next.addEventListener('click', function () { step(1); });
  rail.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  /* Disable arrows entirely if all cards already fit (no overflow). */
  update();
})();

/* ============================================================
   CHATBOT LAUNCHER — tuck when footer is in view
   The fixed bottom-right launcher overlaps the footer's signature
   line (partner logos, copyright, Made-in-Rwanda coin). When the
   footer enters the viewport we slide the launcher off-screen so
   the closing line reads cleanly; it returns once the user
   scrolls back up.
   ============================================================ */
(function () {
  var launcher = document.querySelector('.chatbot-launcher');
  var footer = document.querySelector('.site-footer');
  if (!launcher || !footer || !('IntersectionObserver' in window)) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        launcher.classList.add('is-tucked');
      } else {
        launcher.classList.remove('is-tucked');
      }
    });
  }, { rootMargin: '0px 0px -40px 0px', threshold: 0 });

  observer.observe(footer);
})();
