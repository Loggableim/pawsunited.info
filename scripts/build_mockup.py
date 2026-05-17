#!/usr/bin/env python3
"""Build NEON RETRO mockup v4 – neue Section-Reihenfolge + Server-Karussell."""
import shutil
from pathlib import Path

ROOT = Path("E:/Pawsunited")
OUT = ROOT / "_preview" / "mockups"
OUT.mkdir(parents=True, exist_ok=True)

SERVERS = [
    ("🧱 Minecraft", "Java + Bedrock crossplay. Custom plugins, land claims, weekly build events.", "play.pawsunited.info:25565"),
    ("🦖 ARK: Survival", "Boosted rates, active admins. Tame dinosaurs, build tribes, raid in style.", "ark.pawsunited.info"),
    ("🚗 GTA V RP", "Custom roleplay server with unique storylines and player-driven economy.", "gta.pawsunited.info"),
    ("⚡ C&C Red Alert", "Classic RTS action. Custom maps, Tesla coils, epic 4v4 showdowns.", "cnc.pawsunited.info"),
    ("🎮 Valheim", "Viking survival with the pack. Build, explore, slay bosses together.", "valheim.pawsunited.info"),
    ("🔫 CS2 Community", "Deathmatch, retake, surf — community-run Counter-Strike 2 server.", "cs2.pawsunited.info"),
]

STREAMERS = [
    ("FeuerFuchs", "@derfeuerfuchs", "assets/images/avatars/derfeuerfuchs.jpeg", "https://www.tiktok.com/@derfeuerfuchs"),
    ("Bouizs Spiros", "@boz12427", "assets/images/avatars/boz12427.jpeg", "https://www.tiktok.com/@boz12427"),
    ("Pup Cid", "@pupcid", "assets/images/avatars/pupcid.jpeg", "https://www.tiktok.com/@pupcid"),
    ("wrexythefurry", "@wrexyfurry", "assets/images/avatars/wrexythefurry.jpeg", "https://www.tiktok.com/@wrexyfurry"),
    ("tombluedragon", "@tombluedragon", "assets/images/avatars/tombluedragon.jpeg", "https://www.tiktok.com/@tombluedragon"),
    ("sabari94", "@sabari94_official", "assets/img/characters/sabari.png", "https://www.tiktok.com/@sabari94_official"),
    ("noctobun", "@noctobun", "assets/img/characters/nocto.png", "https://www.tiktok.com/@noctobun"),
    ("Virox Bloodfang", "@viroxbloodfang", "assets/img/characters/viroxbloodfang.png", "https://www.tiktok.com/@viroxbloodfang"),
    ("Chef Mahlzeit", "@chefmahlzeit", "assets/img/characters/chefmahlzeit.png", "https://www.tiktok.com/@chefmahlzeit"),
    ("Xais &amp; Mojita", "@xais_mojita", "assets/img/characters/xaismojita.png", "https://www.tiktok.com/@xais_mojita"),
    ("Keksi", "@keksesindtoll", "assets/img/streamers/keksi5.png", "https://www.tiktok.com/@keksesindtoll"),
    ("Fluxflauschpaw", "@fluxflauschpaw", "assets/img/streamers/fluxflauschpaw.png", "https://www.tiktok.com/@fluxflauschpaw"),
    ("Atamiel Fuchs", "@atamiel_fuchs", "assets/img/streamers/atamiel.png", "https://www.tiktok.com/@atamiel_fuchs"),
]

FEATURES = [
    ("🎮", "5 Dedicated Servers", "ARK, Minecraft, GTA V, C&C + more — all community-hosted, always online."),
    ("📺", "13+ Streamers", "Daily content on TikTok, Twitch and YouTube. Cross-promotion included."),
    ("🛡️", "Curated Space", "Active moderation, zero toxicity. Furry & LGBTQ+ friendly."),
    ("🎪", "Weekly Events", "Build battles, game nights, collab streams — never a dull moment."),
    ("🎤", "24/7 Voice", "Active Discord voice channels. Always someone to play or chat with."),
    ("🚀", "Growth Network", "Shared audiences, creator spotlights and community-driven promotion."),
]

TEAM = [
    ("S", "Scorpion", "Moderator"), ("K", "Kitsus Gehirn", "Moderator"),
    ("B", "Bouizs Spiros", "Moderator, Tech"), ("M", "Mordessa", "Moderator"),
    ("K", "Kawumm", "Moderator"), ("S", "SilberFuchs", "Moderator"),
]

# Build all server cards HTML for rotation
server_cards_html = ""
for icon_name, desc, ip in SERVERS:
    server_cards_html += f'''<div class="server-card"><span class="tag">Online</span><h3>{icon_name}</h3><p>{desc}</p><div class="ip">▸ {ip}</div></div>\n'''

html = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PAWS UNITED · NEON RETRO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Bebas+Neue&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}

  :root {{
    --bg: #08080E;
    --bg2: #0D0D16;
    --bg3: #12121E;
    --border: rgba(255,255,255,0.06);
    --neon-pink: #FF2D95;
    --neon-cyan: #00F0FF;
    --neon-purple: #A855F7;
    --neon-green: #39FF14;
    --text: #EEEEF0;
    --text2: #8888A0;
    --text3: #5C5C72;
    --glow-pink: 0 0 20px rgba(255,45,149,0.3), 0 0 60px rgba(255,45,149,0.1);
    --glow-cyan: 0 0 20px rgba(0,240,255,0.3), 0 0 60px rgba(0,240,255,0.1);
    --glow-purple: 0 0 20px rgba(168,85,247,0.25), 0 0 50px rgba(168,85,247,0.08);
    --font-display: 'Bebas Neue', 'Impact', sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }}

  html {{ scroll-behavior: smooth; }}

  body {{
    font-family: var(--font-body);
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
  }}

  body::after {{
    content: ''; position: fixed; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px);
    pointer-events: none; z-index: 9999;
  }}
  body::before {{
    content: ''; position: fixed; inset: 0; opacity: 0.02;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 9998;
  }}

  ::selection {{ background: var(--neon-pink); color: #000; }}
  h1, h2, h3, .display {{ font-family: var(--font-display); letter-spacing: 2px; }}
  h1 {{ font-size: clamp(4rem, 12vw, 8rem); line-height: 0.92; }}
  h2 {{ font-size: clamp(2.5rem, 5vw, 4rem); line-height: 1; }}

  .glitch {{
    position: relative;
    animation: glitch-skew 4s infinite linear alternate-reverse;
  }}
  .glitch::before, .glitch::after {{
    content: attr(data-text); position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
  }}
  .glitch::before {{ color: var(--neon-cyan); animation: glitch1 2.5s infinite linear alternate-reverse; clip-path: inset(20% 0 60% 0); }}
  .glitch::after {{ color: var(--neon-pink); animation: glitch2 2.5s infinite linear alternate-reverse; clip-path: inset(60% 0 10% 0); }}
  @keyframes glitch1 {{ 0%{{transform:translate(0)}}20%{{transform:translate(-3px,3px)}}40%{{transform:translate(3px,-2px)}}60%{{transform:translate(-5px,1px)}}80%{{transform:translate(2px,-3px)}}100%{{transform:translate(-1px,2px)}} }}
  @keyframes glitch2 {{ 0%{{transform:translate(0)}}25%{{transform:translate(4px,-3px)}}50%{{transform:translate(-3px,5px)}}75%{{transform:translate(2px,-4px)}}100%{{transform:translate(-4px,1px)}} }}
  @keyframes glitch-skew {{ 0%{{transform:skew(0deg)}}10%{{transform:skew(1deg)}}20%{{transform:skew(0deg)}}30%{{transform:skew(-1deg)}}40%{{transform:skew(0deg)}}50%{{transform:skew(2deg)}}60%{{transform:skew(-0.5deg)}}70%{{transform:skew(0deg)}}80%{{transform:skew(-1.5deg)}} }}

  .gradient-text {{
    background: linear-gradient(135deg, var(--neon-pink), var(--neon-purple), var(--neon-cyan));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }}

  nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 2rem;
    background: rgba(8,8,14,0.7);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
  }}
  .nav-logo {{ display: flex; align-items: center; text-decoration: none; }}
  .nav-logo img {{ height: 52px; width: auto; }}
  .nav-links {{ display: flex; gap: 0.25rem; align-items: center; list-style: none; }}
  .nav-links a {{ padding: 0.5rem 1rem; color: var(--text2); text-decoration: none; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; border-radius: 4px; transition: all 0.2s; }}
  .nav-links a:hover {{ color: var(--text); background: rgba(255,255,255,0.04); }}
  .nav-discord {{ padding: 0.45rem 1.4rem !important; border: 1px solid var(--neon-purple); border-radius: 4px; color: var(--neon-purple) !important; transition: all 0.3s !important; }}
  .nav-discord:hover {{ background: var(--neon-purple) !important; color: #000 !important; box-shadow: var(--glow-purple) !important; }}

  .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; padding: 8rem 2rem 4rem; position: relative; overflow: hidden; }}
  .hero-bg-glow {{ position: absolute; inset: 0; z-index: 0; }}
  .hero-bg-glow::before {{ content: ''; position: absolute; width: 500px; height: 500px; border-radius: 50%; background: radial-gradient(circle, rgba(168,85,247,0.12), transparent 70%); top: -100px; left: -100px; animation: orbA 12s ease-in-out infinite alternate; }}
  .hero-bg-glow::after {{ content: ''; position: absolute; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(255,45,149,0.08), transparent 70%); bottom: -50px; right: -80px; animation: orbB 15s ease-in-out infinite alternate; }}
  @keyframes orbA {{ 0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(100px,60px) scale(1.2)}} }}
  @keyframes orbB {{ 0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(-80px,-40px) scale(1.3)}} }}
  #particlesCanvas {{ position: absolute; inset: 0; z-index: 1; }}
  .hero-content {{ position: relative; z-index: 2; }}
  .hero-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border: 1px solid var(--neon-green); color: var(--neon-green); font-family: var(--font-mono); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1.5rem; }}
  .hero-badge .dot {{ width: 6px; height: 6px; background: var(--neon-green); animation: pulse-dot 1.5s infinite; }}
  @keyframes pulse-dot {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}
  .hero-sub {{ color: var(--text2); font-size: 1.05rem; max-width: 500px; margin: 1.5rem auto 2rem; line-height: 1.7; }}
  .hero-actions {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }}
  .btn-neon {{ display: inline-flex; align-items: center; gap: 8px; padding: 14px 32px; font-family: var(--font-body); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; text-decoration: none; border: none; cursor: pointer; transition: all 0.3s; }}
  .btn-neon--pink {{ background: var(--neon-pink); color: #000; box-shadow: var(--glow-pink); }}
  .btn-neon--pink:hover {{ transform: scale(1.05); box-shadow: 0 0 30px rgba(255,45,149,0.5); }}
  .btn-neon--cyan {{ background: transparent; color: var(--neon-cyan); border: 1px solid var(--neon-cyan); }}
  .btn-neon--cyan:hover {{ background: var(--neon-cyan); color: #000; box-shadow: var(--glow-cyan); }}

  .marquee-strip {{ background: var(--bg2); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 0.75rem 0; overflow: hidden; }}
  .marquee-track {{ display: flex; gap: 3rem; animation: marquee 35s linear infinite; width: max-content; }}
  .marquee-track span {{ font-family: var(--font-mono); font-size: 0.78rem; color: var(--text2); white-space: nowrap; }}
  .marquee-track .hl {{ color: var(--neon-cyan); font-weight: 700; }}
  .marquee-track .lv {{ color: var(--neon-pink); }}
  @keyframes marquee {{ 0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}} }}

  section {{ padding: 6rem 2rem; position: relative; }}
  .section-inner {{ max-width: 1200px; margin: 0 auto; }}
  .section-label {{ font-family: var(--font-mono); font-size: 0.7rem; color: var(--neon-purple); text-transform: uppercase; letter-spacing: 3px; margin-bottom: 0.5rem; }}

  /* ── SERVER CAROUSEL ── */
  .server-carousel {{
    position: relative;
    margin-top: 2rem;
  }}
  .server-carousel__track {{
    display: flex;
    gap: 1rem;
    overflow: hidden;
    scroll-behavior: smooth;
  }}
  .server-carousel__slide {{
    flex: 0 0 calc(25% - 0.75rem);
    min-width: 220px;
  }}
  @media (max-width: 700px) {{ .server-carousel__slide {{ flex: 0 0 calc(50% - 0.5rem); }} }}
  @media (max-width: 450px) {{ .server-carousel__slide {{ flex: 0 0 100%; }} }}
  .server-card {{
    background: var(--bg2); border: 1px solid var(--border); padding: 1.75rem;
    position: relative; overflow: hidden; transition: all 0.3s; cursor: pointer;
    height: 100%;
  }}
  .server-card:hover {{ border-color: var(--neon-purple); transform: translateY(-4px); box-shadow: var(--glow-purple); }}
  .server-card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: linear-gradient(180deg, var(--neon-pink), var(--neon-purple)); transform: scaleY(0); transition: transform 0.3s; }}
  .server-card:hover::before {{ transform: scaleY(1); }}
  .server-card .tag {{ display: inline-block; padding: 2px 10px; font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.75rem; border: 1px solid var(--neon-green); color: var(--neon-green); }}
  .server-card h3 {{ font-size: 1.4rem; margin-bottom: 0.25rem; letter-spacing: 1px; }}
  .server-card p {{ color: var(--text2); font-size: 0.82rem; line-height: 1.5; }}
  .server-card .ip {{ font-family: var(--font-mono); font-size: 0.7rem; color: var(--neon-cyan); margin-top: 0.75rem; }}
  .carousel-nav {{
    display: flex; justify-content: center; gap: 0.75rem; margin-top: 1.5rem;
  }}
  .carousel-dot {{
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--text3); border: none; cursor: pointer;
    transition: all 0.3s;
  }}
  .carousel-dot.active {{ background: var(--neon-pink); box-shadow: 0 0 8px rgba(255,45,149,0.5); }}

  /* ── STREAMER GRID ── */
  .streamer-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem; margin-top: 2rem; }}
  @media (max-width: 600px) {{ .streamer-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  .streamer-card {{ padding: 1.25rem 0.75rem; text-align: center; background: var(--bg3); border: 1px solid var(--border); cursor: pointer; transition: all 0.3s; position: relative; overflow: hidden; text-decoration: none; color: inherit; }}
  .streamer-card:hover {{ transform: translateY(-6px); border-color: var(--neon-pink); box-shadow: var(--glow-pink); }}
  .streamer-card::after {{ content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--neon-pink), var(--neon-purple), var(--neon-cyan)); transform: scaleX(0); transition: transform 0.3s; }}
  .streamer-card:hover::after {{ transform: scaleX(1); }}
  .streamer-avatar {{ width: 72px; height: 72px; margin: 0 auto 0.75rem; border-radius: 50%; overflow: hidden; border: 2px solid var(--border); transition: all 0.3s; }}
  .streamer-card:hover .streamer-avatar {{ border-color: var(--neon-pink); box-shadow: 0 0 16px rgba(255,45,149,0.3); }}
  .streamer-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
  .streamer-card .name {{ font-family: var(--font-display); font-size: 1rem; letter-spacing: 1px; margin-bottom: 0.15rem; }}
  .streamer-card .handle {{ font-family: var(--font-mono); font-size: 0.65rem; color: var(--text3); }}
  .streamer-badge {{ display: inline-block; padding: 2px 8px; margin-top: 6px; font-size: 0.55rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; border-radius: 2px; }}
  .streamer-badge--live {{ background: rgba(255,45,149,0.15); color: var(--neon-pink); border: 1px solid rgba(255,45,149,0.3); }}
  .streamer-badge--off {{ background: rgba(255,255,255,0.04); color: var(--text3); }}

  /* ── FEATURES BENTO ── */
  .features-bento {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--border); margin-top: 2rem; border: 1px solid var(--border); }}
  @media (max-width: 700px) {{ .features-bento {{ grid-template-columns: 1fr; }} }}
  .feature-cell {{ background: var(--bg2); padding: 2rem; transition: all 0.3s; }}
  .feature-cell:hover {{ background: var(--bg3); }}
  .feature-cell .icon {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
  .feature-cell h3 {{ font-size: 1.2rem; margin-bottom: 0.3rem; }}
  .feature-cell p {{ color: var(--text2); font-size: 0.82rem; line-height: 1.5; }}

  /* ── TEAM ── */
  .team-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; margin-top: 2rem; }}
  .team-card {{ text-align: center; padding: 1.5rem; background: var(--bg2); border: 1px solid var(--border); transition: all 0.3s; }}
  .team-card:hover {{ border-color: var(--neon-cyan); transform: translateY(-3px); }}
  .team-card .initial {{ width: 48px; height: 48px; margin: 0 auto 0.75rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 1.3rem; border: 2px solid var(--neon-purple); color: var(--neon-purple); }}
  .team-card .tname {{ font-family: var(--font-display); font-size: 1rem; letter-spacing: 1px; }}
  .team-card .trole {{ font-size: 0.7rem; color: var(--text3); }}

  .cta-section {{ text-align: center; padding: 8rem 2rem; position: relative; overflow: hidden; }}
  .cta-section::before {{ content: ''; position: absolute; top: 50%; left: 50%; width: 700px; height: 700px; transform: translate(-50%, -50%); background: radial-gradient(circle, rgba(168,85,247,0.08), transparent 70%); pointer-events: none; }}

  footer {{ border-top: 1px solid var(--border); padding: 3rem 2rem 2rem; position: relative; overflow: hidden; }}
  footer::before {{ content: ''; position: absolute; bottom: -100px; right: -60px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(168,85,247,0.06), transparent 70%); pointer-events: none; }}
  .footer-grid {{ max-width: 1200px; margin: 0 auto 2rem; display: grid; grid-template-columns: 1fr 1fr 1fr 1.5fr; gap: 2rem; text-align: left; align-items: start; }}
  @media (max-width: 800px) {{ .footer-grid {{ grid-template-columns: 1fr 1fr; }} }}
  .footer-grid h4 {{ font-family: var(--font-display); font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 1rem; color: var(--text); }}
  .footer-grid p {{ color: var(--text2); font-size: 0.82rem; line-height: 1.7; }}
  .footer-grid a {{ display: block; color: var(--text2); text-decoration: none; font-size: 0.82rem; margin-bottom: 0.5rem; transition: color 0.2s; }}
  .footer-grid a:hover {{ color: var(--neon-cyan); }}
  .footer-logo-col {{ text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 0.75rem; }}
  .footer-logo-col img {{ height: 110px; width: auto; filter: drop-shadow(0 0 25px rgba(168,85,247,0.2)); transition: filter 0.3s; }}
  .footer-logo-col img:hover {{ filter: drop-shadow(0 0 40px rgba(168,85,247,0.4)); }}
  .footer-bottom {{ max-width: 1200px; margin: 0 auto; padding-top: 1.5rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; font-size: 0.8rem; color: var(--text3); }}
</style>
</head>
<body>

<nav>
  <a href="#home" class="nav-logo">
    <img src="../../assets/img/logos/pawsunited-alt.png" alt="PAWS UNITED">
  </a>
  <ul class="nav-links">
    <li><a href="#streamers">Creators</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#servers">Server</a></li>
    <li><a href="#team">Team</a></li>
    <li><a href="https://discord.gg/pawsunited" class="nav-discord" target="_blank">[ Join ]</a></li>
  </ul>
</nav>

<section class="hero" id="home">
  <div class="hero-bg-glow"></div>
  <canvas id="particlesCanvas"></canvas>
  <div class="hero-content">
    <div class="hero-badge"><span class="dot"></span> 306 Members · Level 3 Boosted</div>
    <h1 class="glitch" data-text="PAWS UNITED">PAWS UNITED</h1>
    <p class="hero-sub">Furry-friendly gaming community. Dedicated servers, daily streams, zero toxicity.</p>
    <div class="hero-actions">
      <a href="https://discord.gg/pawsunited" class="btn-neon btn-neon--pink" target="_blank">▸ Join Discord</a>
      <a href="#streamers" class="btn-neon btn-neon--cyan">Meet the Pack</a>
    </div>
  </div>
</section>

<div class="marquee-strip">
  <div class="marquee-track" id="marqueeTrack">
    <span>🟢 <span class="hl">play.pawsunited.info</span></span>
    <span>Java 1.20.4 · Survival · Creative</span>
    <span>👥 <span class="hl" id="onlineCount">47</span> online</span>
    <span>👤 <span class="hl">306</span> members</span>
    <span><span class="lv">🔴</span> <span class="lv" id="liveCount">0</span> live now</span>
    <span>🏆 Tier 3 · 18 Boosts</span>
    <span>🎮 6 Game Servers</span>
    <span>🟢 <span class="hl">play.pawsunited.info</span></span>
    <span>Java 1.20.4 · Survival · Creative</span>
    <span>👥 <span class="hl">47</span> online</span>
    <span>👤 <span class="hl">306</span> members</span>
    <span><span class="lv">🔴</span> <span class="lv">0</span> live now</span>
    <span>🏆 Tier 3 · 18 Boosts</span>
    <span>🎮 6 Game Servers</span>
  </div>
</div>

<!-- 1. CREATORS (oben) -->
<section id="streamers" style="background:var(--bg2);">
  <div class="section-inner">
    <div class="section-label">▸ 01 · Live Squad</div>
    <h2>Our <span class="gradient-text">Creators</span></h2>
    <p style="color:var(--text2);margin-top:0.5rem;font-size:0.9rem;">13 streamers — one pack. Click any card to visit their TikTok.</p>
    <div class="streamer-grid">
'''
for name, handle, avatar, url in STREAMERS:
    html += f'''<a href="{url}" target="_blank" class="streamer-card">
  <div class="streamer-avatar"><img src="../../{avatar}" alt="{name}"></div>
  <div class="name">{name}</div>
  <div class="handle">{handle}</div>
  <span class="streamer-badge streamer-badge--off">Offline</span>
</a>
'''

html += '''  </div>
</section>

<!-- 2. FEATURES (The Pack Life) -->
<section id="features">
  <div class="section-inner">
    <div class="section-label">▸ 02 · The Pack Life</div>
    <h2>What Makes Us <span class="gradient-text">Special</span></h2>
    <div class="features-bento">
'''
for icon, title, desc in FEATURES:
    html += f'''<div class="feature-cell"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>
'''
html += '''  </div>
</section>

<!-- 3. SERVERS (rotierend) -->
<section id="servers" style="background:var(--bg2);">
  <div class="section-inner">
    <div class="section-label">▸ 03 · Game Servers</div>
    <h2>Choose Your <span class="gradient-text">Arena</span></h2>
    <div class="server-carousel" id="serverCarousel">
      <div class="server-carousel__track" id="carouselTrack">
'''
for icon_name, desc, ip in SERVERS:
    html += f'''<div class="server-carousel__slide"><div class="server-card"><span class="tag">Online</span><h3>{icon_name}</h3><p>{desc}</p><div class="ip">▸ {ip}</div></div></div>
'''
html += '''  </div>
    <div class="carousel-nav" id="carouselNav"></div>
  </div>
</section>

<!-- 4. TEAM (unten) -->
<section id="team">
  <div class="section-inner">
    <div class="section-label">▸ 04 · The Pack</div>
    <h2>Meet the <span class="gradient-text">Team</span></h2>
    <div class="team-grid">
'''
for init, name, role in TEAM:
    html += f'<div class="team-card"><div class="initial">{init}</div><div class="tname">{name}</div><div class="trole">{role}</div></div>\n'

html += '''  </div>
</section>

<section class="cta-section">
  <div class="section-inner">
    <div class="section-label">▸ 05 · Join</div>
    <h2 style="margin-bottom:0.75rem;">Ready to <span class="gradient-text">Rise?</span></h2>
    <p style="color:var(--text2);max-width:480px;margin:0 auto 2rem;font-size:0.95rem;">Where paws unite, legends rise. 306 members are waiting for you.</p>
    <a href="https://discord.gg/pawsunited" class="btn-neon btn-neon--pink" target="_blank">▸ Join the Pack — Free</a>
  </div>
</section>

<footer>
  <div class="footer-grid">
    <div>
      <h4>Server</h4>
      <p style="margin-bottom:1rem;">play.pawsunited.info</p>
      <a href="#servers">Minecraft</a>
      <a href="#servers">ARK</a>
      <a href="#servers">GTA V</a>
      <a href="#servers">C&amp;C</a>
    </div>
    <div>
      <h4>Community</h4>
      <a href="#streamers">Creators</a>
      <a href="#team">Team</a>
      <a href="https://discord.gg/pawsunited">Discord</a>
    </div>
    <div>
      <h4>Connect</h4>
      <a href="https://discord.gg/pawsunited">Discord</a>
      <a href="https://tiktok.com/@pawsunited">TikTok</a>
    </div>
    <div class="footer-logo-col">
      <img src="../../assets/img/logos/pawsunited-alt.png" alt="PAWS UNITED">
      <span style="font-family:var(--font-mono);font-size:0.65rem;color:var(--text3);">Where Paws Unite, Legends Rise</span>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 PAWS UNITED</span>
    <span>Where Paws Unite, Legends Rise</span>
    <span>play.pawsunited.info</span>
  </div>
</footer>

<script>
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

  startAuto();
  // Ensure dots match initially
  setTimeout(() => goTo(0), 100);
})();

// ── Smooth scroll ──
document.querySelectorAll('a[href^="#"]').forEach(a => { a.addEventListener('click', e => { const t = document.querySelector(a.getAttribute('href')); if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); } }); });
console.log('🐾 NEON RETRO v4 · PAWS UNITED');
</script>
</body>
</html>'''

with open(OUT / "a-neon-retro.html", "w", encoding="utf-8") as f:
    f.write(html)

# Copy assets
logos_dst = ROOT / "_preview" / "assets" / "img" / "logos"
logos_dst.mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "assets" / "img" / "logos" / "pawsunited-alt.png", logos_dst / "pawsunited-alt.png")

for sub in ["assets/images/avatars", "assets/img/characters", "assets/img/streamers"]:
    src = ROOT / sub
    dst = ROOT / "_preview" / sub
    if src.exists() and not dst.exists():
        shutil.copytree(src, dst)

print(f"✅ NEON RETRO v4: {OUT / 'a-neon-retro.html'}")
