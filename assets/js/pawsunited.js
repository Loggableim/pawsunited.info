/* ============================================================
   PawsUnited.info — Magic & Interactivity v1.0
   ============================================================ */

document.addEventListener('DOMContentLoaded', function() {

  /* --- Sticky Nav --- */
  const navbar = document.querySelector('.navbar');
  let lastScroll = 0;

  window.addEventListener('scroll', function() {
    const current = window.scrollY;
    if (current > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    lastScroll = current;
  });

  /* --- Mobile Menu Toggle --- */
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');

  if (hamburger) {
    hamburger.addEventListener('click', function() {
      this.classList.toggle('active');
      navLinks.classList.toggle('open');
    });

    // Close on link click
    navLinks.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
      });
    });
  }

  /* --- Scroll Reveal (Intersection Observer) --- */
  const revealElements = document.querySelectorAll('.reveal');

  const revealObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -60px 0px'
  });

  revealElements.forEach(function(el) {
    revealObserver.observe(el);
  });

  /* --- Hero Particle System --- */
  const heroParticles = document.querySelector('.hero-particles');
  if (heroParticles) {
    var colors = ['#FF6B35', '#7B2D8E', '#00C9A7', '#FFD166', '#4ECDC4', '#E84855'];
    for (var i = 0; i < 30; i++) {
      var p = document.createElement('div');
      p.className = 'particle';
      p.style.left = Math.random() * 100 + '%';
      p.style.animationDelay = Math.random() * 8 + 's';
      p.style.animationDuration = (6 + Math.random() * 6) + 's';
      p.style.width = p.style.height = (2 + Math.random() * 4) + 'px';
      p.style.background = colors[Math.floor(Math.random() * colors.length)];
      heroParticles.appendChild(p);
    }
  }

  /* --- Discord Widget Counter Sim --- */
  const counterEl = document.getElementById('discord-online-count');
  if (counterEl) {
    // Animate from 0 to target
    var target = parseInt(counterEl.dataset.target) || 42;
    var current = 0;
    var step = Math.ceil(target / 30);
    var interval = setInterval(function() {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(interval);
      }
      counterEl.textContent = current;
    }, 40);
  }

  /* --- Smooth Scroll for anchor links --- */
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  /* --- Counter Animation (general use) --- */
  document.querySelectorAll('[data-count-to]').forEach(function(el) {
    var target = parseInt(el.dataset.countTo);
    var duration = parseInt(el.dataset.countDuration) || 1500;
    var start = 0;
    var stepTime = Math.max(16, Math.floor(duration / target));
    var observer = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting) {
        var timer = setInterval(function() {
          start += Math.ceil(target / 40);
          if (start >= target) {
            start = target;
            clearInterval(timer);
          }
          el.textContent = start;
        }, stepTime);
        observer.unobserve(el);
      }
    }, { threshold: 0.5 });
    observer.observe(el);
  });

  console.log('🐾 PawsUnited — Where Paws Unite, Legends Rise');
  console.log('📡 play.pawsunited.info');
});
