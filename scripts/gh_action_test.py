#!/usr/bin/env python3
"""Debug: test if Discord token works in GitHub Actions."""
import os, asyncio, json, websockets

async def main():
    t = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    print(f"Token len: {len(t)}")
    print(f"First 10: {t[:10]}")
    print(f"Last 5: {t[-5:]}")
    print(f"Has spaces: {' ' in t}")

    async with websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json") as ws:
        hello = json.loads(await ws.recv())
        print(f"Gateway hello OK, interval={hello['d']['heartbeat_interval']}")

        await ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": t,
                "properties": {"$os": "linux", "$browser": "pawsunited", "$device": "pawsunited"},
                "intents": 513,
            }
        }))

        raw = await asyncio.wait_for(ws.recv(), timeout=8)
        data = json.loads(raw)
        op = data.get("op")
        if op == 0:
            print(f"SUCCESS: {data.get('t')}")
        elif op == 9:
            print(f"INVALID SESSION: {data.get('d', '?')}")
        else:
            print(f"Response op={op}: {str(data)[:300]}")

asyncio.run(main())
