/* /about page scroll-reveal — IntersectionObserver with reduced-motion. */
(function () {
  'use strict';

  var prefersReduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var targets = document.querySelectorAll(
    '.about-header, .about-vision__inner, .about-story__label, ' +
    '.about-story__body, .about-mission__inner, .about-info__card, ' +
    '.about-values__title, .about-values__item, .about-credibility__inner'
  );

  if (prefersReduced || !('IntersectionObserver' in window)) {
    // No animation: mark everything visible immediately.
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
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

  targets.forEach(function (el) { observer.observe(el); });
})();
