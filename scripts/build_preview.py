#!/usr/bin/env python3
"""Convert Jekyll PawsUnited site to static HTML preview."""
import yaml, shutil
from pathlib import Path

ROOT = Path("E:/Pawsunited")
OUT = ROOT / "_preview"

with open(ROOT / "_config.yml") as f:
    site = yaml.safe_load(f) or {}
with open(ROOT / "_data/locales.yml") as f:
    locales = yaml.safe_load(f) or {}
with open(ROOT / "_data/servers.yml") as f:
    servers_data = yaml.safe_load(f) or {}
with open(ROOT / "_data/team-members.yml") as f:
    team_members = yaml.safe_load(f) or {}
with open(ROOT / "_data/streamers.yml") as f:
    streamers = yaml.safe_load(f) or {}
discord_url = site.get("discord_invite", "#")

PICONS = {
    "twitch": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z"/></svg>',
    "youtube": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
    "tiktok": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>',
    "kick": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M3.394 2.333h17.212l-3.395 4.17v7.505l-5.455 6.244V4.636H7.06L3.394 2.333Z"/></svg>',
}

def esc(s):
    s = str(s)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s

def nav_html(locale, H):
    nav_map = {"de": {"servers": "Server", "team": "Team", "creators": "Creator"}, "en": {"servers": "Servers", "team": "Team", "creators": "Creators"}}
    n = nav_map.get(locale, nav_map["de"])
    return '''<nav class="navbar" id="navbar" role="navigation">
  <div class="nav-inner">
    <a href="#home" class="nav-logo">
      <span class="nav-logo-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span>
      <span class="nav-logo-text">PAWS UNITED</span>
    </a>
    <ul class="nav-links" id="navLinks">
      <li><a href="#servers" class="nav-link">''' + n["servers"] + '''</a></li>
      <li><a href="#team" class="nav-link">''' + n["team"] + '''</a></li>
      <li><a href="#creators" class="nav-link">''' + n["creators"] + '''</a></li>
      <li class="nav-mobile-only"><a href="''' + discord_url + '''" class="btn btn--primary btn--full" target="_blank" rel="noopener noreferrer">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>
        ''' + esc(H["discord_button"]) + '''</a></li>
    </ul>
    <a href="''' + discord_url + '''" class="btn btn--discord-nav" target="_blank" rel="noopener noreferrer">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>
      <span>''' + esc(H["discord_button"]) + '''</span>
    </a>
    <button class="hamburger" id="hamburger" aria-label="Menü">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>'''

def server_strip_html(locale):
    return '''<div class="server-strip" id="serverStatusStrip">
  <div class="server-strip__inner">
    <span class="server-strip__stat">
      <span class="server-strip__dot"></span>
      <span class="label">Server:</span>
      <span class="value">play.pawsunited.info</span>
    </span>
    <span class="server-strip__stat"><span class="label">Java 1.20.4</span></span>
    <span class="server-strip__stat">
      <span class="label">\U0001f465</span>
      <span class="value" id="discordOnline">43</span>
      <span class="label">online</span>
    </span>
    <span class="server-strip__stat">
      <span class="label">\U0001f464</span>
      <span class="value" id="discordMembers">305</span>
      <span class="label">''' + ("members" if locale == "en" else "Mitglieder") + '''</span>
    </span>
  </div>
</div>'''

def filer_bar_html():
    return '''<div class="filter-bar" id="filterBar">
    <button class="filter-btn active" data-filter="all">Alle</button>
    <button class="filter-btn" data-filter="tiktok">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
      TikTok
    </button>
    <button class="filter-btn" data-filter="twitch">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z"/></svg>
      Twitch
    </button>
    <button class="filter-btn" data-filter="youtube">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
      YouTube
    </button>
  </div>'''

def build_page(locale):
    loc = locales.get(locale, locales["de"])
    srv = servers_data.get(locale, servers_data["de"])
    team = team_members.get(locale, team_members["de"])
    H = loc["hero"]
    F = loc["features"]
    W = loc["why_join"]
    C = loc["cta"]
    FT = loc["footer"]
    SV = loc["servers"]

    L = []

    def a(s):
        L.append(s)

    a("<!DOCTYPE html>")
    a('<html lang="' + locale + '">')
    a("<head>")
    a('<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    a("<title>" + esc(loc["meta"]["default_title"]) + "</title>")
    a('<meta name="description" content="' + esc(loc["meta"]["default_description"]) + '">')
    a('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Ctext y=%2728%27 font-size=%2728%27%3E\U0001f43e%3C/text%3E%3C/svg%3E">')
    a('<link rel="preconnect" href="https://fonts.googleapis.com">')
    a('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    a('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet">')
    a('<link rel="stylesheet" href="../assets/css/main.css">')
    a("<style>.locale-link{color:var(--color-text-secondary);font-size:var(--text-small)}.locale-link:hover{color:var(--color-text-primary)}</style>")
    a("</head>")
    a("<body>")

    # Nav
    a(nav_html(locale, H))

    # Hero
    a('<section class="hero">')
    a('<div class="hero__content">')
    a('<img src="../pawsunitedlogo.png" alt="PAWS UNITED Logo" class="hero__logo animate-fade-in">')
    a('<h1 class="hero__title animate-fade-in animate-delay-1">' + esc(H["title"]) + "</h1>")
    a('<p class="hero__subtitle animate-fade-in animate-delay-2">' + esc(H["subtitle"]) + "</p>")
    a('<div class="hero__actions animate-fade-in animate-delay-3">')
    a('<a href="' + discord_url + '" class="btn btn--primary btn--large" target="_blank" rel="noopener noreferrer">')
    a('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>')
    a(esc(H["discord_button"]))
    a("</a>")
    a('<a href="#servers" class="btn btn--secondary btn--large">' + esc(H["discover_servers_button"]) + "</a>")
    a("</div>")
    a("</div>")
    a("</section>")

    # Server Status Strip
    a(server_strip_html(locale))

    # Servers
    a('<section id="servers" class="section">')
    a('<div class="container">')
    a('<div class="section-header">')
    a('<h2 class="section-header__title">' + esc(SV["title"]) + "</h2>")
    a('<p class="section-header__text">' + esc(SV["text"]) + "</p>")
    a("</div>")
    a('<div class="grid grid--3">')
    for s in srv:
        sc = "server-card__status--" + s["status"]
        a('<article class="card server-card">')
        a('<div class="server-card__header">')
        a('<h3 class="server-card__title">' + esc(s["name"]) + "</h3>")
        a('<span class="server-card__status ' + sc + '">' + esc(s["status"]) + "</span>")
        a("</div>")
        a('<p class="server-card__description">' + esc(s["description"]) + "</p>")
        a('<div class="server-card__vibe">')
        a('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>')
        a("<span>" + esc(s["vibe"]) + "</span>")
        a("</div>")
        a('<a href="' + s["panel_url"] + '" class="btn btn--primary btn--full" target="_blank" rel="noopener noreferrer">')
        a('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>')
        a(esc(SV["play_button"]))
        a("</a>")
        a("</article>")
    a("</div>")
    a("</div>")
    a("</section>")

    # Features
    a('<section class="section section--alt">')
    a('<div class="container">')
    a('<div class="section-header">')
    a('<h2 class="section-header__title">' + esc(F["title"]) + "</h2>")
    a('<p class="section-header__text">' + esc(F["text"]) + "</p>")
    a("</div>")
    a('<div class="grid grid--3">')
    for k in ["curated_membership","cross_platform_growth","creator_collaboration","moderated_discord","events_collabs","visibility_support"]:
        item = F[k]
        a('<article class="card feature-card">')
        a('<div class="feature-card__icon"><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></div>')
        a('<h3 class="feature-card__title">' + esc(item["title"]) + "</h3>")
        a('<p class="feature-card__text">' + esc(item["text"]) + "</p>")
        a("</article>")
    a("</div>")
    a("</div>")
    a("</section>")

    # Team
    a('<section id="team" class="section section--alt">')
    a('<div class="container">')
    a('<div class="section-header">')
    a('<h2 class="section-header__title">' + esc(loc["team"]["title"]) + "</h2>")
    a('<p class="section-header__text">' + esc(loc["team"]["text"]) + "</p>")
    a("</div>")
    a('<div class="grid grid--3">')
    for m in team:
        a('<article class="card creator-card">')
        a('<div class="creator-card__avatar creator-card__avatar--icon" aria-hidden="true">')
        a('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>')
        a("</div>")
        a('<h3 class="creator-card__name">' + esc(m["name"]) + "</h3>")
        a('<p class="creator-card__tagline">' + esc(m["role"]) + "</p>")
        a("</article>")
    a("</div>")
    a("</div>")
    a("</section>")

    # Creators
    a('<section id="creators" class="section">')
    a('<div class="container">')
    a('<div class="section-header">')
    a('<h2 class="section-header__title">' + esc(loc["creators"]["title"]) + "</h2>")
    a('<p class="section-header__text">' + esc(loc["creators"]["text"]) + "</p>")
    a("</div>")
    a(filer_bar_html())
    a('<div class="grid grid--3" id="creatorsGrid">')
    for c in streamers:
        nm = c["name"]
        hdl = c.get("handle", "")
        tag = c.get("tagline", "")
        av = c.get("avatar", "")
        pp = c.get("primary_platform", "")
        sps = c.get("secondary_platforms", [])
        disp = c.get("display", "framed")
        c_url = c.get("url", "")

        if av:
            av_html = '<img src="../' + av + '" alt="' + esc(nm) + '" class="creator-card__avatar-img">'
        else:
            av_html = '<span style="font-size:1.5rem;font-weight:700;color:var(--color-text-primary);">' + esc(nm[:2]) + "</span>"

        plats = ""
        plats += '<span class="creator-card__platform" title="' + esc(pp.capitalize()) + '">' + PICONS.get(pp, "") + "</span>"
        for sp in sps:
            plats += '<span class="creator-card__platform" title="' + esc(sp.capitalize()) + '">' + PICONS.get(sp, "") + "</span>"

        if c_url:
            a('<a href="' + c_url + '" target="_blank" rel="noopener" class="card creator-card creator-card--link" data-platform="' + pp + '">')
        else:
            a('<article class="card creator-card" data-platform="' + pp + '">')

        a('<div class="creator-card__avatar creator-card__avatar--' + disp + '" aria-hidden="true">' + av_html + "</div>")
        a('<h3 class="creator-card__name">' + esc(nm) + "</h3>")
        if hdl:
            a('<p class="creator-card__handle">' + esc(hdl) + "</p>")
        if tag:
            a('<p class="creator-card__tagline">' + esc(tag) + "</p>")
        a('<div class="creator-card__platforms">' + plats + "</div>")

        if c_url:
            a("</a>")
        else:
            a("</article>")
    a("</div>")
    a("</div>")
    a("</section>")

    # Why Join
    a('<section class="section section--gradient">')
    a('<div class="container">')
    a('<div class="section-header">')
    a('<h2 class="section-header__title">' + esc(W["title"]) + "</h2>")
    a('<p class="section-header__text">' + esc(W["text"]) + "</p>")
    a("</div>")
    a('<div class="grid grid--3">')
    for k in ["shared_reach","own_p_servers","daily_streams","support_feedback","events_collabs","relaxed_atmosphere"]:
        item = W["benefits"][k]
        a('<article class="card benefit-card">')
        a('<div class="benefit-card__icon"><svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>')
        a('<h3 class="benefit-card__title">' + esc(item["title"]) + "</h3>")
        a('<p class="benefit-card__text">' + esc(item["text"]) + "</p>")
        a("</article>")
    a("</div>")
    a("</div>")
    a("</section>")

    # CTA
    a('<section class="cta-section">')
    a('<div class="container">')
    a('<h2 class="cta-section__title">' + esc(C["title"]) + "</h2>")
    a('<p class="cta-section__text">' + esc(C["text"]) + "</p>")
    a('<a href="' + discord_url + '" class="btn btn--primary btn--large" target="_blank" rel="noopener noreferrer">')
    a('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>')
    a(esc(C["discord_button"]))
    a("</a>")
    a("</div>")
    a("</section>")

    # Footer
    a('<footer class="footer">')
    a('<div class="container">')
    a('<div class="footer__content">')
    a('<img src="../pawsunitedlogo.png" alt="' + esc(FT["logo_alt"]) + '" class="footer__logo">')
    a('<p class="footer__text">' + esc(FT["text"]) + "</p>")
    a('<div class="footer__social">')
    a('<a href="' + discord_url + '" class="footer__social-link" title="' + esc(FT["discord_link_title"]) + '" target="_blank" rel="noopener noreferrer">')
    a('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>')
    a('<span class="sr-only">Discord</span>')
    a("</a>")
    a("</div>")
    a('<nav class="footer__links">')
    a('<a href="#servers" class="footer__link">' + esc(FT["server_link"]) + "</a>")
    a('<a href="#team" class="footer__link">' + esc(FT["team_link"]) + "</a>")
    a('<a href="#creators" class="footer__link">' + esc(FT["creator_link"]) + "</a>")
    a("</nav>")
    a('<div class="footer__locale-switcher">')
    if locale == "de":
        a('<a href="en/index.html" class="locale-link">English</a>')
    else:
        a('<a href="../index.html" class="locale-link">Deutsch</a>')
    a("</div>")
    a('<p class="footer__copyright">' + esc(FT["copyright"]) + "</p>")
    a("</div>")
    a("</div>")
    a("</footer>")

    a('<script src="../assets/js/main.js" defer></script>')
    a("</body>")
    a("</html>")

    return "\n".join(L)


# Generate
shutil.rmtree(OUT, ignore_errors=True)
(OUT / "en").mkdir(parents=True)

html_de = build_page("de")
with open(OUT / "index.html", "w", encoding="utf-8") as f:
    f.write(html_de)

html_en = build_page("en")
with open(OUT / "en" / "index.html", "w", encoding="utf-8") as f:
    f.write(html_en)

# Copy assets
shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
for fn in ["pawsunitedlogo.png", "pawsuintedsplashscreen.jpg"]:
    src = ROOT / fn
    if src.exists():
        shutil.copy2(src, OUT / fn)

print("DONE: {} ({})".format(OUT / "index.html", len(html_de)))
print("DONE: {} ({})".format(OUT / "en/index.html", len(html_en)))
