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


      /* ----------------------------------------------------------------
         HERO BACKGROUND VIDEO — clip-path scroll reveal
         Expands from a pill shape to full viewport as you scroll.
      ---------------------------------------------------------------- */
      gsap.to('.background-video', {
        clipPath: 'inset(0% 0% 0% 0% round 0px)',
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start:   'top top',
          end:     'bottom top',
          scrub:   true,
          onEnter: function () {
            var el = document.querySelector('.background-video');
            if (el) el.classList.add('no-clip');
          },
          onLeaveBack: function () {
            var el = document.querySelector('.background-video');
            if (el) el.classList.remove('no-clip');
          }
        }
      });


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
      document.getElementById('footerConnectBtn'),
      document.getElementById('sponsorGetInTouchBtn')
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
      document.getElementById('hero-video'),        /* background-video-2 (hidden fallback) */
      document.querySelector('.hero-bg-video'),     /* clip-path hero background            */
      document.querySelector('.sponsor-bg-video'),  /* sponsor-tech section background      */
      document.querySelector('.circle-bg-video')    /* footer circle background             */
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
