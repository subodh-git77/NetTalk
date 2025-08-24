import asyncio
import json
import secrets
import string
import websockets
from datetime import datetime
import http.server
import socketserver
import threading
import os

# ----------------------------
# Room Management
# ----------------------------
rooms = {}

def generate_room_id(length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_pin(length: int = 4) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))

async def broadcast(message: str, room_id: str, sender=None):
    """Send message to all clients in a room except sender"""
    if room_id not in rooms:
        return
    dead = []
    for client in list(rooms[room_id]["clients"].keys()):
        if client is sender:
            continue
        try:
            await client.send(message)
        except Exception:
            dead.append(client)
    for d in dead:
        rooms[room_id]["clients"].pop(d, None)

    # auto delete empty room
    if room_id in rooms and not rooms[room_id]["clients"]:
        del rooms[room_id]

# ----------------------------
# WebSocket Handler
# ----------------------------
async def handler(websocket):
    current_room = None
    username = None

    try:
        async for raw in websocket:
            try:
                data = json.loads(raw)
            except:
                await websocket.send(json.dumps({"type": "error", "message": "Invalid JSON"}))
                continue

            action = data.get("action")

            # CREATE ROOM
            if action == "create_room":
                room_id = generate_room_id()
                pin = generate_pin()
                rooms[room_id] = {"pin": pin, "clients": {}, "history": []}
                await websocket.send(json.dumps({
                    "type": "room_created",
                    "room_id": room_id,
                    "pin": pin
                }))

            # LIST ROOMS
            elif action == "list_rooms":
                room_list = [
                    {"room_id": rid, "users": len(info["clients"])}
                    for rid, info in rooms.items()
                ]
                await websocket.send(json.dumps({
                    "type": "room_list",
                    "rooms": room_list
                }))

            # JOIN ROOM
            elif action == "join_room":
                pin_in = str(data.get("pin") or "").strip()
                username = (data.get("username") or "Guest").strip() or "Guest"

                room_id = None
                for rid, info in rooms.items():
                    if info["pin"] == pin_in:
                        room_id = rid
                        break

                if room_id:
                    # Remove from previous room
                    if current_room and websocket in rooms.get(current_room, {}).get("clients", {}):
                        rooms[current_room]["clients"].pop(websocket, None)

                    current_room = room_id
                    rooms[room_id]["clients"][websocket] = username

                    await websocket.send(json.dumps({
                        "type": "joined_room",
                        "room_id": room_id,
                        "message": f"✅ Joined room {room_id}"
                    }))

                    # Send history
                    for msg in rooms[room_id]["history"]:
                        await websocket.send(msg)

                    # Notify others
                    await broadcast(json.dumps({
                        "type": "status",
                        "message": f"{username} joined the room"
                    }), room_id, sender=websocket)

                else:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid PIN: No room found"
                    }))

            # LEAVE ROOM
            elif action == "leave_room":
                if current_room and current_room in rooms:
                    user = rooms[current_room]["clients"].pop(websocket, None)
                    await websocket.send(json.dumps({
                        "type": "left_room",
                        "message": f"👋 You left room {current_room}"
                    }))
                    if user:
                        await broadcast(json.dumps({
                            "type": "status",
                            "message": f"{user} left the room"
                        }), current_room, sender=websocket)
                    if not rooms[current_room]["clients"]:
                        del rooms[current_room]
                current_room = None

            # CHAT
            elif action == "chat":
                if not current_room:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Join a room first"
                    }))
                    continue

                msg_text = (data.get("message") or "").strip()
                if not msg_text:
                    continue

                # Updated timestamp to ISO 8601 format with UTC 'Z'
                timestamp = datetime.utcnow().isoformat() + "Z"
                payload = json.dumps({
                    "type": "chat",
                    "user": username or "Unknown",
                    "message": msg_text,
                    "time": timestamp
                })

                # save history
                hist = rooms[current_room]["history"]
                hist.append(payload)
                if len(hist) > 50:
                    hist.pop(0)

                # broadcast to others
                await broadcast(payload, current_room, sender=websocket)

            # TYPING INDICATORS
            elif action == "typing":
                if current_room:
                    await broadcast(json.dumps({
                        "type": "typing",
                        "user": username
                    }), current_room, sender=websocket)

            elif action == "stop_typing":
                if current_room:
                    await broadcast(json.dumps({
                        "type": "stop_typing",
                        "user": username
                    }), current_room, sender=websocket)

            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Unknown action"
                }))

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if current_room and current_room in rooms:
            user = rooms[current_room]["clients"].pop(websocket, None)
            if user:
                await broadcast(json.dumps({
                    "type": "status",
                    "message": f"{user} left the room"
                }), current_room)
            if not rooms[current_room]["clients"]:
                del rooms[current_room]

# ----------------------------
# Start Servers
# ----------------------------
async def start_websocket():
    async with websockets.serve(handler, "0.0.0.0", 6789):
        print("✅ WebSocket running at ws://0.0.0.0:6789")
        await asyncio.Future()

def start_http():
    PORT = 8000
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"✅ HTTP running at http://0.0.0.0:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=start_http, daemon=True).start()
    asyncio.run(start_websocket())
