// ── Particles ──
const canvas = document.getElementById('particlesCanvas');
const ctx = canvas.getContext('2d');
let W, H;
function resize() { W = canvas.width = canvas.offsetWidth; H = canvas.height = canvas.offsetHeight; }
window.addEventListener('resize', resize); resize();
const COLORS = ['#FF2D95', '#00F0FF', '#A855F7', '#39FF14'];
const particles = [];
for (let i = 0; i < 80; i++) {
  particles.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - 0.5) * 0.6, vy: (Math.random() - 0.5) * 0.6, r: 1 + Math.random() * 2, color: COLORS[Math.floor(Math.random() * COLORS.length)], alpha: 0.2 + Math.random() * 0.8 });
}
function drawParticles() {
  ctx.clearRect(0, 0, W, H);
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
    if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = p.color; ctx.globalAlpha = p.alpha; ctx.fill(); ctx.globalAlpha = 1;
  });
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 120) {
        ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = particles[i].color; ctx.globalAlpha = (1 - dist / 120) * 0.15;
        ctx.lineWidth = 0.5; ctx.stroke(); ctx.globalAlpha = 1;
      }
    }
  }
  requestAnimationFrame(drawParticles);
}
drawParticles();

// ── Marquee ──
const mt = document.getElementById('marqueeTrack');
if (mt) mt.innerHTML += mt.innerHTML;

// ── Live counts ──
const oc = document.getElementById('onlineCount');
const lc = document.getElementById('liveCount');
if (oc) setInterval(() => { oc.textContent = 42 + Math.floor(Math.random() * 14); }, 18000);
if (lc) { let i = 0; const arr = ['0','0','1','0','0','0','2','0','1']; setInterval(() => { lc.textContent = arr[i % arr.length]; i++; }, 28000); }

// ── SERVER CAROUSEL ──
(function() {
  const track = document.getElementById('carouselTrack');
  const nav = document.getElementById('carouselNav');
  if (!track || !nav) return;
  const slides = track.querySelectorAll('.server-carousel__slide');
  const totalSlides = slides.length;
  let current = 0;
  let autoInterval;
  let paused = false;

  // Build dots
  for (let i = 0; i < totalSlides; i++) {
    const dot = document.createElement('button');
    dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
    dot.dataset.index = i;
    dot.addEventListener('click', function() { goTo(parseInt(this.dataset.index)); });
    nav.appendChild(dot);
  }

  // Resize handler: how many visible?
  function getVisibleSlides() {
    const w = window.innerWidth;
    if (w <= 450) return 1;
    if (w <= 700) return 2;
    return 3; // show 3 cards at a time
  }

  function goTo(index) {
    const visible = getVisibleSlides();
    const maxStart = Math.max(0, totalSlides - visible);
    current = Math.min(index, maxStart);
    const slideW = track.querySelector('.server-carousel__slide').offsetWidth + 16; // 1rem gap
    track.scrollTo({ left: current * slideW, behavior: 'smooth' });
    // Update dots
    nav.querySelectorAll('.carousel-dot').forEach((d, i) => {
      d.classList.toggle('active', i === current);
    });
  }

  function nextSlide() {
    if (paused) return;
    const visible = getVisibleSlides();
    const maxStart = Math.max(0, totalSlides - visible);
    if (current >= maxStart) { current = 0; }
    else { current++; }
    goTo(current);
  }

  function startAuto() {
    stopAuto();
    autoInterval = setInterval(nextSlide, 3000);
  }
  function stopAuto() {
    if (autoInterval) { clearInterval(autoInterval); autoInterval = null; }
  }

  // Pause on hover
  const carousel = document.getElementById('serverCarousel');
  carousel.addEventListener('mouseenter', function() { paused = true; stopAuto(); });
  carousel.addEventListener('mouseleave', function() { paused = false; startAuto(); });

  // Touch support
  let touchStartX = 0;
  carousel.addEventListener('touchstart', function(e) { touchStartX = e.changedTouches[0].screenX; }, { passive: true });
  carousel.addEventListener('touchend', function(e) {
    const diff = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) nextSlide();
      else { 
        const visible = getVisibleSlides();
        const maxStart = Math.max(0, totalSlides - visible);
        if (current <= 0) current = maxStart;
        else current--;
        goTo(current);
      }
    }
  }, { passive: true });

  // Recalc on resize
  let resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      const visible = getVisibleSlides();
      const maxStart = Math.max(0, totalSlides - visible);
      if (current > maxStart) { current = maxStart; }
      goTo(current);
    }, 200);
  });

  // Arrow buttons (◀ ▶)
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');
  if (prevBtn) {
    prevBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      const visible = getVisibleSlides();
      const maxStart = Math.max(0, totalSlides - visible);
      if (current <= 0) current = maxStart;
      else current--;
      goTo(current);
      stopAuto(); paused = true;
      setTimeout(function() { paused = false; startAuto(); }, 5000);
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      nextSlide();
      stopAuto(); paused = true;
      setTimeout(function() { paused = false; startAuto(); }, 5000);
    });
  }

  startAuto();
  // Ensure dots match initially
  setTimeout(() => goTo(0), 100);
})();

// ── Smooth scroll ──
document.querySelectorAll('a[href^="#"]').forEach(a => { a.addEventListener('click', e => { const t = document.querySelector(a.getAttribute('href')); if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); } }); });

// ── MOBILE HAMBURGER ──
(function() {
  const btn = document.getElementById('hamburgerBtn');
  const menu = document.getElementById('mobileMenu');
  if (!btn || !menu) return;

  function openMenu() {
    menu.classList.add('open');
    btn.textContent = '✕';
    btn.setAttribute('aria-label', 'Menü schließen');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    menu.classList.remove('open');
    btn.textContent = '☰';
    btn.setAttribute('aria-label', 'Menü öffnen');
    document.body.style.overflow = '';
  }

  btn.addEventListener('click', function() {
    if (menu.classList.contains('open')) closeMenu();
    else openMenu();
  });

  // Close on Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && menu.classList.contains('open')) closeMenu();
  });

  // Close on click outside menu (on the backdrop)
  menu.addEventListener('click', function(e) {
    if (e.target === menu) closeMenu();
  });

  // Close on link click
  menu.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', function() {
      closeMenu();
    });
  });
})();
