#!/usr/bin/env python3
"""
PAWS UNITED - Live Status Collector v2
Connects to Discord Gateway via raw WebSocket, collects voice states,
maps streamers to voice channels, and writes live-status.json.
Runs in GitHub Actions on a 5-minute cron schedule.
Zero external dependencies (uses websockets which is pre-installed).
"""
import asyncio, json, os, sys, time
import websockets

GUILD_ID = 1367623607055810620
OUTPUT_FILE = "assets/data/live-status.json"

# Map voice channel IDs to streamer info
CHANNEL_TO_STREAMER = {
    1400089213395009536: {"name": "Pup Cid", "handle": "@pupcid"},
    1400428572992213002: {"name": "FeuerFuchs", "handle": "@derfeuerfuchs"},
    1436773710756577430: {"name": "Bouizs Spiros", "handle": "@boz12427"},
    1460655580476604477: {"name": "tombluedragon", "handle": "@tombluedragon"},
    1462840115528339587: {"name": "wrexythefurry", "handle": "@wrexyfurry"},
    1467671209163358278: {"name": "sabari94", "handle": "@sabari94_official"},
    1485577060268376136: {"name": "noctobun", "handle": "@noctobun"},
    1497635980830576760: {"name": "noctobun", "handle": "@noctobun"},
    1483188063185403975: {"name": "Keksi", "handle": "@keksesindtoll"},
    1483188117367427104: {"name": "Keksi", "handle": "@keksesindtoll"},
    1497637366347862316: {"name": "Xais & Mojita", "handle": "@xais_mojita"},
    1497659581646766080: {"name": "Chef Mahlzeit", "handle": "@chefmahlzeit"},
    1498094672961212426: {"name": "Virox Bloodfang", "handle": "@viroxbloodfang"},
    1499110083509096510: {"name": "Fluxflauschpaw", "handle": "@fluxflauschpaw"},
    1505261216057004224: {"name": "Atamiel Fuchs", "handle": "@atamiel_fuchs"},
}

# Also map by category parent ID (fallback)
CATEGORY_TO_STREAMER = {
    1400088234725343334: {"name": "Pup Cid", "handle": "@pupcid"},
    1400428474811809802: {"name": "FeuerFuchs", "handle": "@derfeuerfuchs"},
    1436773439166746795: {"name": "Bouizs Spiros", "handle": "@boz12427"},
    1460654545544675470: {"name": "tombluedragon", "handle": "@tombluedragon"},
    1462839773608673436: {"name": "wrexythefurry", "handle": "@wrexyfurry"},
    1467584116005408769: {"name": "sabari94", "handle": "@sabari94_official"},
    1485576938478239805: {"name": "noctobun", "handle": "@noctobun"},
    1483187660217651271: {"name": "Keksi", "handle": "@keksesindtoll"},
    1497636124729020597: {"name": "Xais & Mojita", "handle": "@xais_mojita"},
    1497659381934854305: {"name": "Chef Mahlzeit", "handle": "@chefmahlzeit"},
    1498094410678931536: {"name": "Virox Bloodfang", "handle": "@viroxbloodfang"},
    1499109900037656737: {"name": "Fluxflauschpaw", "handle": "@fluxflauschpaw"},
    1505258745645502504: {"name": "Atamiel Fuchs", "handle": "@atamiel_fuchs"},
}

def find_streamer(vc_id, category_id):
    """Look up streamer by channel ID, then by category."""
    s = CHANNEL_TO_STREAMER.get(vc_id)
    if s:
        return s
    return CATEGORY_TO_STREAMER.get(category_id)

async def collect_voice_states(token):
    """Connect to Discord Gateway, collect voice states, return them."""
    voice_states = {}
    guild_channels = {}
    collected = asyncio.Event()
    
    async with websockets.connect(
        "wss://gateway.discord.gg/?v=10&encoding=json",
        ping_interval=20,
        ping_timeout=10,
    ) as ws:
        # Wait for Hello (op 10)
        hello_raw = await ws.recv()
        hello = json.loads(hello_raw)
        heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000.0
        
        # Start heartbeat task
        async def heartbeat():
            while True:
                await asyncio.sleep(heartbeat_interval)
                try:
                    await ws.send(json.dumps({"op": 1, "d": None}))
                except:
                    break
        
        hb_task = asyncio.create_task(heartbeat())
        
        # Send Identify (intent 512 = GUILD_VOICE_STATES, intent 1 = GUILDS)
        await ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "linux",
                    "$browser": "pawsunited",
                    "$device": "pawsunited"
                },
                "intents": 513,  # GUILDS (1) + GUILD_VOICE_STATES (512)
            }
        }))
        
        # Listen for events for max 8 seconds
        start = time.time()
        while time.time() - start < 8:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=2)
            except asyncio.TimeoutError:
                continue
            
            data = json.loads(raw)
            op = data.get("op")
            t = data.get("t")
            d = data.get("d", {})
            
            if op == 0 and t == "READY":
                # Connected! Now guild will follow
                pass
            
            elif op == 0 and t == "GUILD_CREATE":
                # Store channel info
                gid = int(d.get("id", 0))
                if gid == GUILD_ID:
                    for ch in d.get("channels", []):
                        guild_channels[int(ch["id"])] = {
                            "name": ch.get("name", "?"),
                            "type": ch.get("type"),
                            "parent_id": ch.get("parent_id"),
                        }
                    # We have guild + channels, now wait for voice states
                    collected.set()
            
            elif op == 0 and t == "VOICE_STATE_UPDATE":
                # A voice state update
                uid = int(d.get("user_id", 0))
                ch_id = d.get("channel_id")
                if ch_id:
                    voice_states[uid] = {
                        "channel_id": int(ch_id),
                        "self_stream": d.get("self_stream", False),
                        "self_video": d.get("self_video", False),
                        "self_mute": d.get("self_mute", False),
                        "self_deaf": d.get("self_deaf", False),
                        "member_name": d.get("member", {}).get("user", {}).get("username", "?"),
                        "nick": d.get("member", {}).get("nick"),
                        "avatar": d.get("member", {}).get("avatar"),
                    }
                else:
                    # Left voice channel
                    voice_states.pop(uid, None)
            
            elif op == 0 and t == "VOICE_STATE_UPDATE":
                # Already handled above - this is duplicate check
                pass
        
        hb_task.cancel()
        return voice_states, guild_channels


def build_status(voice_states, guild_channels):
    """Build the live status JSON."""
    live = []
    online = []
    other = []
    
    for uid, vs in voice_states.items():
        ch_id = vs["channel_id"]
        ch_info = guild_channels.get(ch_id, {})
        category_id = ch_info.get("parent_id")
        if isinstance(category_id, str):
            category_id = int(category_id)
        
        display_name = vs.get("member_name", "?")
        streaming = vs["self_stream"] or vs["self_video"]
        
        entry = {
            "user_id": uid,
            "name": display_name,
            "nick": vs.get("nick"),
            "channel_id": ch_id,
            "channel_name": ch_info.get("name", "?"),
            "streaming": streaming,
        }
        
        streamer = find_streamer(ch_id, category_id)
        if streamer:
            entry["streamer"] = streamer["name"]
            entry["handle"] = streamer["handle"]
            if streaming:
                entry["status"] = "live"
                live.append(entry)
            else:
                entry["status"] = "online"
                online.append(entry)
        else:
            entry["status"] = "in_voice"
            other.append(entry)
    
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "live": live,
        "online_voice": online,
        "other_voice": other,
        "total_voice": len(live) + len(online) + len(other),
        "live_count": len(live),
        "live_streamers": [s["streamer"] for s in live],
        "online_streamers": [s["streamer"] for s in online],
    }


async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN env var not set", flush=True)
        sys.exit(1)
    
    print("Connecting to Discord Gateway...", flush=True)
    voice_states, guild_channels = await collect_voice_states(token)
    print(f"Found {len(voice_states)} users in voice channels", flush=True)
    
    result = build_status(voice_states, guild_channels)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Written: {OUTPUT_FILE}", flush=True)
    print(f"Live streamers: {result['live_count']}", flush=True)
    if result["live_streamers"]:
        for s in result["live_streamers"]:
            print(f"  🔴 {s}", flush=True)
    if result["online_streamers"]:
        for s in result["online_streamers"]:
            print(f"  🟢 {s}", flush=True)
    print("Done!", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
