import io from "socket.io-client";

const SOCKET_URL = "http://127.0.0.1:8001";

let socket = null;
let listeners = {};

export function initSocket() {
  if (socket && socket.connected) return socket;

  const userId = localStorage.getItem("user") || "1";
  
  socket = io(SOCKET_URL, {
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5,
  });

  socket.on("connect", () => {
    console.log("✓ Socket connected to real-time server");
  });

  socket.on("disconnect", () => {
    console.log("✗ Socket disconnected from real-time server");
  });

  socket.on("feed_update", (data) => {
    console.log("📢 Feed update received");
    if (listeners.feedUpdate) {
      listeners.feedUpdate(data);
    }
  });

  socket.on("comment_update", (data) => {
    console.log("💬 Comment update received");
    if (listeners.commentUpdate) {
      listeners.commentUpdate(data);
    }
  });

  socket.on("like_update", (data) => {
    console.log("❤️ Like update received");
    if (listeners.likeUpdate) {
      listeners.likeUpdate(data);
    }
  });

  socket.on("connect_response", (data) => {
    console.log("✓ Socket server response:", data);
  });

  return socket;
}

export function onFeedUpdate(callback) {
  listeners.feedUpdate = callback;
}

export function onCommentUpdate(callback) {
  listeners.commentUpdate = callback;
}

export function onLikeUpdate(callback) {
  listeners.likeUpdate = callback;
}

export function getSocket() {
  return socket || initSocket();
}

export function closeSocket() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
}
