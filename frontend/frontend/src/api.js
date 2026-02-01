const BASE = "http://127.0.0.1:8000/api";

function getAuthParams() {
  const user = localStorage.getItem("user");
  return user ? `?user_id=${user}` : "";
}

function headers() {
  return {
    "Content-Type": "application/json",
  };
}

export async function getFeed() {
  const res = await fetch(`${BASE}/feed/${getAuthParams()}`, { headers: headers() });
  return res.json();
}

export function likePost(id) {
  return fetch(`${BASE}/like/post/${id}/${getAuthParams()}`, {
    method: "POST",
    headers: headers(),
  });
}

export function unlikePost(id) {
  return fetch(`${BASE}/unlike/post/${id}/${getAuthParams()}`, {
    method: "DELETE",
    headers: headers(),
  });
}

export function likeComment(id) {
  return fetch(`${BASE}/like/comment/${id}/${getAuthParams()}`, {
    method: "POST",
    headers: headers(),
  });
}

export function unlikeComment(id) {
  return fetch(`${BASE}/unlike/comment/${id}/${getAuthParams()}`, {
    method: "DELETE",
    headers: headers(),
  });
}

export async function getLeaderboard() {
  const res = await fetch(`${BASE}/leaderboard/${getAuthParams()}`, { headers: headers() });
  return res.json();
}

export function createPost(content) {
  return fetch(`${BASE}/post/${getAuthParams()}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ content }),
  });
}


export function addComment(postId, content, parent = null) {
  return fetch(`${BASE}/comment/${postId}/${getAuthParams()}`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ content, parent }),
  });
}

export const deletePost = id =>
  fetch(`${BASE}/post/${id}/${getAuthParams()}`, {
    method: "DELETE",
    headers: headers(),
  });

export const deleteComment = id =>
  fetch(`${BASE}/comment/delete/${id}/${getAuthParams()}`, {
    method: "DELETE",
    headers: headers(),
  });

