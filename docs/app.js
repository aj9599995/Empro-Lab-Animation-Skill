// Landing page script. No dependencies. Self-contained so GitHub Pages can serve /docs alone.

const root = document.documentElement;
const reduceQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

/* ---------- Reduced motion switch (starts from the OS setting) ---------- */

const reduceToggle = document.getElementById('reduce');

function setReduce(on) {
  root.dataset.motion = on ? 'reduce' : 'full';
  reduceToggle.checked = on;
  readTokens();
}

setReduce(reduceQuery.matches);
reduceToggle.addEventListener('change', () => setReduce(reduceToggle.checked));
reduceQuery.addEventListener('change', (event) => setReduce(event.matches));

/* ---------- Personality switch (changes the tokens) ---------- */

const personality = document.getElementById('personality');

personality.addEventListener('change', () => {
  root.dataset.personality = personality.value;
  readTokens();
});

/* ---------- Token readout ---------- */

function readTokens() {
  const css = getComputedStyle(root);
  document.getElementById('readout-duration').textContent = css.getPropertyValue('--motion-duration-base').trim();
  document.getElementById('readout-ease').textContent = css.getPropertyValue('--motion-ease-enter').trim();
  document.getElementById('readout-distance').textContent = css.getPropertyValue('--motion-distance-md').trim();
}

readTokens();

/* ---------- Token box (press to move) ---------- */

const tokenBox = document.getElementById('token-box');

tokenBox.addEventListener('click', () => {
  const pressed = tokenBox.getAttribute('aria-pressed') !== 'true';
  tokenBox.setAttribute('aria-pressed', String(pressed));
});

/* ---------- Replay the hero entrance ---------- */

document.getElementById('replay').addEventListener('click', () => {
  const items = document.querySelectorAll('.motion-enter');
  items.forEach((el) => el.classList.remove('motion-enter'));
  void document.body.offsetWidth; // force one reflow so the class change restarts the animation
  items.forEach((el) => el.classList.add('motion-enter'));
});

/* ---------- Collapse (accordion) ---------- */

const collapseToggle = document.getElementById('collapse-toggle');
const collapse = document.getElementById('collapse-demo');

collapseToggle.addEventListener('click', () => {
  const open = collapse.dataset.open !== 'true';
  collapse.dataset.open = String(open);
  collapseToggle.setAttribute('aria-expanded', String(open));
  collapseToggle.textContent = open ? 'Hide details' : 'Show details';
});

/* ---------- Scroll progress (rAF-throttled) ---------- */

const progress = document.getElementById('progress');
let ticking = false;

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = max > 0 ? window.scrollY / max : 0;
  progress.style.transform = `scaleX(${ratio})`;
  ticking = false;
}

window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(updateProgress);
    ticking = true;
  }
}, { passive: true });

updateProgress();

/* ---------- Scroll reveal (same logic as templates/reveal.js) ---------- */

function initReveal(selector = '[data-reveal]') {
  const items = Array.from(document.querySelectorAll(selector));
  if (items.length === 0) return;

  if (reduceQuery.matches || !('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-revealed'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });

  items.forEach((el) => observer.observe(el));
}

initReveal();
