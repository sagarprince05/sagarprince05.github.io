/* ==========================================================================
   Portfolio — script.js
   Small, dependency-free enhancements:
     1. Light / dark theme toggle (persisted)
     2. Cursor spotlight (desktop only)
     3. Active nav link that follows scroll position
     4. Scroll-reveal for sections
     5. Copy-email button + footer year
   Everything degrades gracefully if JS is disabled.
   ========================================================================== */

(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Theme toggle ---------- */
  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* private mode etc. */ }
    });
  }

  /* ---------- 2. Cursor spotlight ---------- */
  var spotlight = document.querySelector('.spotlight');
  var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (spotlight && canHover && !reduceMotion) {
    var raf = null;
    var lastX = 0;
    var lastY = 0;
    window.addEventListener('mousemove', function (e) {
      lastX = e.clientX;
      lastY = e.clientY;
      if (raf) return;
      raf = window.requestAnimationFrame(function () {
        spotlight.style.setProperty('--x', lastX + 'px');
        spotlight.style.setProperty('--y', lastY + 'px');
        raf = null;
      });
    }, { passive: true });
  }

  /* ---------- 3. Active nav on scroll ---------- */
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
      // Pick the section with the largest visible area; fall back to the first in DOM order
      var best = null;
      var bestRatio = 0;
      sections.forEach(function (s) {
        if (visible[s.id] > bestRatio) { best = s.id; bestRatio = visible[s.id]; }
      });
      if (best) setActive(best);
    }, { rootMargin: '-20% 0px -60% 0px', threshold: [0, 0.1, 0.25, 0.5, 0.75, 1] });

    sections.forEach(function (s) { navObserver.observe(s); });

    // Mark the last section active when the page is scrolled to the bottom
    window.addEventListener('scroll', function () {
      var atBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 2;
      if (atBottom) setActive(sections[sections.length - 1].id);
    }, { passive: true });
  }

  /* ---------- 4. Scroll reveal ---------- */
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
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    Array.prototype.forEach.call(reveals, function (el) { revealObserver.observe(el); });
  }

  /* ---------- 5. Copy email + footer year ---------- */
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
})();
