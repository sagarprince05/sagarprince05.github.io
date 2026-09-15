/* ==========================================================================
   Portfolio — script.js
   Small, dependency-free enhancements:
     1. Mobile nav toggle + header shadow on scroll
     2. Active nav link that follows scroll position
     3. Scroll-reveal for sections
     4. Copy-email button + footer year
     5. Screenshot lightbox (case-study pages)
   Everything degrades gracefully if JS is disabled.
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Header: mobile menu + scrolled state ---------- */
  var header = document.querySelector('.site-header');
  var navToggle = document.querySelector('.nav-toggle');
  if (header && navToggle) {
    navToggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    // Close the panel after choosing a destination
    Array.prototype.forEach.call(header.querySelectorAll('.nav-panel a'), function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('nav-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- 2. Active nav on scroll ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-link'));
  var sections = navLinks
    .map(function (link) { return document.querySelector(link.getAttribute('href')); })
    .filter(Boolean);

  function setActive(id) {
    navLinks.forEach(function (link) {
      var isActive = link.getAttribute('href') === '#' + id;
      link.classList.toggle('is-active', isActive);
      if (isActive) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  if ('IntersectionObserver' in window && sections.length) {
    var visible = {};
    var navObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        visible[entry.target.id] = entry.isIntersecting ? entry.intersectionRatio : 0;
      });
      var best = null, bestRatio = 0;
      sections.forEach(function (s) {
        if (visible[s.id] > bestRatio) { best = s.id; bestRatio = visible[s.id]; }
      });
      if (best) setActive(best);
      else if (window.scrollY < 200) setActive('');
    }, { rootMargin: '-30% 0px -55% 0px', threshold: [0, 0.1, 0.25, 0.5, 0.75, 1] });
    sections.forEach(function (s) { navObserver.observe(s); });
  }

  /* ---------- 3. Scroll reveal ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-visible'); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.02 });
    Array.prototype.forEach.call(reveals, function (el) { revealObserver.observe(el); });
  }

  /* ---------- 4. Copy email + footer year ---------- */
  var copyBtn = document.querySelector('.copy-email');
  if (copyBtn) {
    var label = copyBtn.querySelector('.copy-label');
    var original = label ? label.textContent : '';
    copyBtn.addEventListener('click', function () {
      var email = copyBtn.getAttribute('data-email') || '';
      var done = function () {
        copyBtn.classList.add('is-copied');
        if (label) label.textContent = 'Copied!';
        window.setTimeout(function () {
          copyBtn.classList.remove('is-copied');
          if (label) label.textContent = original;
        }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(email).then(done).catch(function () {
          window.prompt('Copy this email address:', email);
        });
      } else {
        window.prompt('Copy this email address:', email);
      }
    });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- 5. Screenshot lightbox (case-study pages) ---------- */
  var lightbox = document.querySelector('.lightbox');
  if (lightbox && typeof lightbox.showModal === 'function') {
    var lbImg = lightbox.querySelector('img');
    var lbClose = lightbox.querySelector('.lightbox-close');
    var lastTrigger = null;

    Array.prototype.forEach.call(document.querySelectorAll('a.shot'), function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        var thumb = link.querySelector('img');
        lbImg.src = link.getAttribute('href');
        lbImg.alt = thumb ? thumb.alt : '';
        lastTrigger = link;
        lightbox.showModal();
      });
    });

    if (lbClose) lbClose.addEventListener('click', function () { lightbox.close(); });
    lightbox.addEventListener('click', function (e) { if (e.target === lightbox) lightbox.close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && lightbox.open) lightbox.close(); });
    lightbox.addEventListener('close', function () {
      lbImg.removeAttribute('src');
      if (lastTrigger) lastTrigger.focus();
    });
  }
})();
