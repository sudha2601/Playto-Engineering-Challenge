"""
Standalone Socket.IO server for real-time updates
Run this alongside Django: python manage.py runserver & python socketio_server.py
"""
import socketio
import threading
import time
import asyncio
from http import HTTPStatus
from aiohttp import web

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    cors_allowed_origins='*',
    engineio_logger=False,
    logger=False
)

app = web.Application()
sio.attach(app)

# Store connected clients
connected_clients = {}

# Event queue for pending broadcasts
pending_events = []

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    try:
        user_id = environ.get('HTTP_X_USER_ID', 'anonymous')
        connected_clients[sid] = {'user_id': user_id}
        print(f"✓ Socket connected - User {user_id}: {sid} (Total: {len(connected_clients)})")
        await sio.emit('connect_response', {'status': 'connected'}, to=sid)
    except Exception as e:
        print(f"Connection error: {e}")

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    if sid in connected_clients:
        user_id = connected_clients[sid].get('user_id', 'anonymous')
        del connected_clients[sid]
        print(f"✗ Socket disconnected - User {user_id}: {sid} (Remaining: {len(connected_clients)})")

@sio.event
async def ping(data):
    """Handle ping/heartbeat"""
    return {'status': 'pong'}

async def broadcast_event(event_name, event_data):
    """Broadcast event to all connected clients"""
    if connected_clients:
        await sio.emit(event_name, event_data, skip_sid=None)
        print(f"📢 Broadcast: {event_name} to {len(connected_clients)} clients")

async def process_pending_events():
    """Process queued events (called periodically)"""
    global pending_events
    if pending_events and connected_clients:
        for event_name, event_data in pending_events:
            await broadcast_event(event_name, event_data)
        pending_events = []

async def start_background_tasks(app):
    """Start background task to process events"""
    async def event_processor():
        while True:
            await process_pending_events()
            await asyncio.sleep(0.1)
    
    import asyncio
    asyncio.create_task(event_processor())

async def index(request):
    """Health check endpoint"""
    return web.Response(text='Socket.IO server running', status=HTTPStatus.OK)

# Add routes
app.router.add_get('/', index)

def run_server():
    """Run the Socket.IO server"""
    try:
        print("🚀 Starting Socket.IO server on http://127.0.0.1:8001")
        web.run_app(app, host='127.0.0.1', port=8001, print=lambda x: None)
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == '__main__':
    run_server()
