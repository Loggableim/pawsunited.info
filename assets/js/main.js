// PAWS UNITED - Main JavaScript v4
// Sticky Nav, Mobile Menu, Streamer Filter, Live Discord Data + Streamer Status

(function() {
  'use strict';

  /* ==============================
     STICKY NAV
     ============================== */
  const navbar = document.getElementById('navbar');
  let ticking = false;

  function handleNavScroll() {
    navbar.classList.toggle('scrolled', (window.scrollY || window.pageYOffset) > 60);
  }

  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        handleNavScroll();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  handleNavScroll();

  /* ==============================
     MOBILE HAMBURGER
     ============================== */
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function() {
      this.classList.toggle('active');
      navLinks.classList.toggle('open');
      document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
    });

    navLinks.querySelectorAll('.nav-link').forEach(function(link) {
      link.addEventListener('click', function() {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ==============================
     LIVE DISCORD STATUS — Public API
     ============================== */
  const onlineEl = document.getElementById('discordOnline');
  const membersEl = document.getElementById('discordMembers');
  const statusDot = document.querySelector('.server-strip__dot');

  function animateNumber(el, from, to) {
    if (from === to) return;
    var range = to - from;
    var step = Math.max(1, Math.ceil(Math.abs(range) / 20));
    var dir = range > 0 ? 1 : -1;
    var current = from;
    var timer = setInterval(function() {
      current += step * dir;
      if ((dir > 0 && current >= to) || (dir < 0 && current <= to)) {
        current = to;
        clearInterval(timer);
      }
      el.textContent = current;
    }, 40);
  }

  function fetchDiscordStatus() {
    fetch('https://discord.com/api/v10/invites/pawsunited?with_counts=true', {
      cache: 'no-store'
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var online = data.approximate_presence_count;
      var members = data.approximate_member_count;
      if (online !== undefined && onlineEl) {
        animateNumber(onlineEl, parseInt(onlineEl.textContent) || 0, online);
      }
      if (members !== undefined && membersEl) {
        animateNumber(membersEl, parseInt(membersEl.textContent) || 0, members);
      }
      if (statusDot) {
        statusDot.style.background = (online > 0) ? '#3ba55c' : '#ed4245';
      }
    })
    .catch(function() { /* silent */ });
  }

  if (document.getElementById('serverStatusStrip')) {
    fetchDiscordStatus();
    setInterval(fetchDiscordStatus, 45000);
  }

  /* ==============================
     LIVE STREAMER STATUS — GitHub Action JSON
     ============================== */
  function fetchLiveStatus() {
    fetch('assets/data/live-status.json?t=' + Date.now(), {
      cache: 'no-store'
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var liveList = data.live || [];
      var onlineList = data.online_voice || [];

      // Build lookup: streamer_name -> status
      var statusMap = {};
      liveList.forEach(function(s) {
        if (s.streamer) statusMap[s.streamer] = 'live';
      });
      onlineList.forEach(function(s) {
        if (s.streamer && !statusMap[s.streamer]) statusMap[s.streamer] = 'online';
      });

      // Update streamer cards in the grid
      var cards = document.querySelectorAll('#creatorsGrid .creator-card');
      cards.forEach(function(card) {
        var nameEl = card.querySelector('.creator-card__name');
        if (!nameEl) return;
        var cardName = nameEl.textContent.trim();

        // Remove existing badges
        var oldBadge = card.querySelector('.live-badge');
        if (oldBadge) oldBadge.remove();

        var status = statusMap[cardName];
        if (status === 'live') {
          var badge = document.createElement('span');
          badge.className = 'live-badge live-badge--live';
          badge.textContent = '🔴 LIVE';
          card.querySelector('.creator-card__avatar').after(badge);
        } else if (status === 'online') {
          var badge = document.createElement('span');
          badge.className = 'live-badge live-badge--online';
          badge.textContent = '🟢 Online';
          card.querySelector('.creator-card__avatar').after(badge);
        }
      });

      // Update live counter in nav or strip
      var liveCountEl = document.getElementById('liveCount');
      if (liveCountEl) {
        liveCountEl.textContent = data.live_count || 0;
      }

      // Pulse status dot if anyone is live
      if (data.live_count > 0 && statusDot) {
        statusDot.style.background = '#ff4444';
        statusDot.style.animation = 'pulse-live 1.5s infinite';
      }
    })
    .catch(function() { /* silent - file may not exist yet */ });
  }

  // Fetch on load + every 60 seconds (GitHub Action runs every 5 min)
  fetchLiveStatus();
  setInterval(fetchLiveStatus, 60000);

  /* ==============================
     STREAMER FILTER
     ============================== */
  const filterBar = document.getElementById('filterBar');
  const creatorsGrid = document.getElementById('creatorsGrid');

  if (filterBar && creatorsGrid) {
    var cards = creatorsGrid.querySelectorAll('.creator-card');

    filterBar.addEventListener('click', function(e) {
      var btn = e.target.closest('.filter-btn');
      if (!btn) return;

      filterBar.querySelectorAll('.filter-btn').forEach(function(b) {
        b.classList.remove('active');
      });
      btn.classList.add('active');

      var filter = btn.getAttribute('data-filter');

      cards.forEach(function(card) {
        if (filter === 'all') {
          card.classList.remove('filter-hidden');
        } else {
          var platform = card.getAttribute('data-platform') || '';
          card.classList.toggle('filter-hidden', platform !== filter);
        }
      });
    });
  }

  /* ==============================
     SMOOTH SCROLL
     ============================== */
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ==============================
     COUNTER ANIMATION (stats)
     ============================== */
  document.querySelectorAll('[data-count-to]').forEach(function(el) {
    var target = parseInt(el.getAttribute('data-count-to'));
    var duration = parseInt(el.getAttribute('data-count-duration')) || 1500;
    var current = 0;
    var step = Math.max(1, Math.ceil(target / 40));
    var observer = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting) {
        var timer = setInterval(function() {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(timer);
          }
          el.textContent = current;
        }, Math.max(16, duration / 40));
        observer.unobserve(el);
      }
    }, { threshold: 0.5 });
    observer.observe(el);
  });

  console.log('🐾 PAWS UNITED — Where Paws Unite, Legends Rise');
  console.log('📡 play.pawsunited.info · Discord: discord.gg/pawsunited');

})();
