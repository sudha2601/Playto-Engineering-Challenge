"""
Socket.IO event emitter - Connect to standalone server and emit events
"""
import socketio
import threading

# Connect to the Socket.IO server
sio_client = socketio.Client(
    reconnection=True,
    reconnection_delay=1,
    reconnection_delay_max=5,
    reconnection_attempts=5,
    logger=False,
    engineio_logger=False
)

server_url = "http://127.0.0.1:8001"
is_connected = False

@sio_client.event
def connect():
    global is_connected
    is_connected = True
    print("✓ Connected to Socket.IO server")

@sio_client.event
def disconnect():
    global is_connected
    is_connected = False
    print("✗ Disconnected from Socket.IO server")

def init_socket_client():
    """Initialize connection to Socket.IO server"""
    try:
        if not is_connected:
            thread = threading.Thread(target=connect_to_server, daemon=True)
            thread.start()
    except Exception as e:
        print(f"Socket client init error: {e}")

def connect_to_server():
    """Connect to the standalone Socket.IO server"""
    try:
        sio_client.connect(server_url, wait_timeout=10)
    except Exception as e:
        print(f"Connection failed: {e}")

def emit_event(event_name, event_data):
    """Emit event to connected clients"""
    try:
        if is_connected:
            sio_client.emit(event_name, event_data, namespace='/')
        else:
            print(f"Socket server not connected, queuing event: {event_name}")
    except Exception as e:
        print(f"Emit error: {e}")

# Auto-connect on import
init_socket_client()
