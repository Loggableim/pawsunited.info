# PAWS UNITED

Ein Zuhause für Gamer, Furrys, Streamer & Creator — Furry-freundliche Gaming Community mit eigenen Servern.

![PAWS UNITED](pawsunitedlogo.png)

## Über uns

PAWS UNITED ist eine Gaming-Community mit Fokus auf Furry-Kultur, Creator-Unterstützung und gemeinsames Spielen. Wir betreiben eigene Game Server und bieten eine lebendige, offene Community auf Discord.

## Features

- **🎮 Game Server** — ARK, Minecraft (Bedrock & Java), C&C Red Alert, GTA V
- **🎥 Creator Support** — Streamer & Content Creator aus verschiedenen Plattformen
- **🛠️ Team gesucht** — Moderatoren, GameMaster und Admins
- **🐾 Furry-freundlich** — Offene und inklusive Community
- **🌈 Events & Collabs** — Regelmäßige Community-Events und Streams

## Entwicklung

Diese Seite ist mit [Jekyll](https://jekyllrb.com/) gebaut und kompatibel mit [GitHub Pages](https://pages.github.com/).

### Lokale Entwicklung

```bash
# Dependencies installieren
gem install bundler jekyll

# Development Server starten
jekyll serve
```

Besuche `http://localhost:4000` um die Seite anzuzeigen.

### Dateistruktur

```
├── _config.yml           # Jekyll Konfiguration
├── _data/
│   ├── servers.yml       # Game Server Daten
│   ├── streamers.yml     # Creator Daten
│   └── team-roles.yml    # Team-Rollen
├── _includes/            # Wiederverwendbare Komponenten
│   ├── hero.html
│   ├── servers.html
│   ├── server-card.html
│   ├── team.html
│   ├── creators.html
│   ├── creator-card.html
│   ├── why-join.html
│   ├── cta.html
│   └── footer.html
├── _layouts/
│   └── default.html      # Haupt-Layout
├── assets/
│   └── css/
│       └── main.css      # Design System
└── index.html            # Landing Page
```

### Creator hinzufügen

Bearbeite `_data/streamers.yml` um Creator hinzuzufügen oder zu ändern:

```yaml
- name: "CreatorName"
  handle: "@socialhandle"
  primary_platform: "tiktok"  # twitch, youtube, tiktok, oder kick
  secondary_platforms:
    - "youtube"
    - "twitch"
  tagline: "Kurze Beschreibung"
```

### Game Server hinzufügen

Bearbeite `_data/servers.yml`:

```yaml
- name: "Server Name"
  game: "Game Title"
  panel_url: "https://panel.pawsunited.info/c/..."
  description: "Server Beschreibung"
  status: "online"  # online, offline, maintenance
  vibe: "Community-Vibe"
```

## Design System

Die Seite folgt dem PAWS UNITED Brand & Design System:

- **Primärfarben (Regenbogen)**: 
  - Paws Red `#E94B35`
  - Paws Orange `#F39C12`
  - Paws Yellow `#F1C40F`
  - Paws Green `#2ECC71`
  - Paws Blue `#3498DB`
  - Paws Purple `#9B59B6`
- **UI-Farben**: Dark Base `#0E0F14`, Surface Dark `#161823`
- **Typografie**: Poppins (Headlines), Inter (Body)

## Lizenz

Siehe [LICENSE](LICENSE) für Details.
