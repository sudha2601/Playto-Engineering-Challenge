import { useEffect, useState } from "react";
import {
  getFeed,
  likePost,
  unlikePost,
  createPost,
  addComment,
  deletePost
} from "../api";
import Comment from "./Comment";

function timeAgo(date) {
  const seconds = Math.floor((new Date() - new Date(date)) / 1000);
  if (seconds < 60) return `${seconds}s ago`;

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;

  return `${Math.floor(hours / 24)}d ago`;
}

export default function Feed({ refreshLeaderboard }) {
  const [posts, setPosts] = useState([]);
  const [text, setText] = useState("");
  const [likedPosts, setLikedPosts] = useState(new Set());

  const refresh = () => {
    getFeed().then(setPosts);
    refreshLeaderboard();
  };

  useEffect(() => {
    refresh();
  }, []);

  const toggleLike = async id => {
    if (!likedPosts.has(id)) {
      await likePost(id);
      setLikedPosts(new Set([...likedPosts, id]));
    } else {
      await unlikePost(id);
      const s = new Set(likedPosts);
      s.delete(id);
      setLikedPosts(s);
    }
    refresh();
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 p-6 rounded-xl">
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="What's on your mind?"
          className="w-full bg-slate-900 p-4 rounded text-white h-24"
        />

        <button
          onClick={async () => {
            if (!text.trim()) return;
            await createPost(text);
            setText("");
            refresh();
          }}
          className="mt-3 bg-blue-500 px-6 py-2 rounded"
        >
          Post
        </button>
      </div>

      {posts.map(p => (
        <div key={p.id} className="bg-slate-800 p-6 rounded-xl">
          <div className="flex justify-between">
            <div>
              <p className="text-white font-semibold">{p.author}</p>
              <p className="text-xs text-slate-400">{timeAgo(p.created_at)}</p>
            </div>

            {String(p.author_id) === localStorage.getItem("user") && (
              <button
                onClick={async () => {
                  await deletePost(p.id);
                  refresh();
                }}
                className="text-red-400 text-sm"
              >
                Delete
              </button>
            )}
          </div>

          <p className="text-slate-300 mt-2">{p.content}</p>

          <button onClick={() => toggleLike(p.id)} className="mt-2">
            ❤️ {p.like_count}
          </button>

          <input
            className="mt-3 w-full bg-slate-900 p-2 rounded"
            placeholder="Write comment..."
            onKeyDown={async e => {
              if (e.key === "Enter" && e.target.value.trim()) {
                await addComment(p.id, e.target.value);
                e.target.value = "";
                refresh();
              }
            }}
          />

          <div className="mt-4 space-y-3">
            {p.comments.map(c => (
              <Comment key={c.id} comment={c} postId={p.id} refresh={refresh} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
