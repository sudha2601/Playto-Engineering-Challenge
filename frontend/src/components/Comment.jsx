import { useState } from "react";
import { likeComment, unlikeComment, addComment, deleteComment } from "../api";

function timeAgo(date) {
  const seconds = Math.floor((new Date() - new Date(date)) / 1000);
  if (seconds < 60) return `${seconds}s ago`;

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;

  return `${Math.floor(hours / 24)}d ago`;
}

export default function Comment({ comment, postId, refresh }) {
  const [reply, setReply] = useState("");
  const [showReply, setShowReply] = useState(false);
  const user = localStorage.getItem("user");

  const toggleLike = async () => {
    if (!comment.liked) await likeComment(comment.id);
    else await unlikeComment(comment.id);
    refresh();
  };

  const submitReply = async e => {
    if (e.key === "Enter" && reply.trim()) {
      await addComment(postId, reply, comment.id);
      setReply("");
      setShowReply(false);
      refresh();
    }
  };

  return (
    <div className="bg-slate-700/40 p-4 rounded-xl">
      <div className="flex justify-between">
        <div>
          <p className="text-white">{comment.author}</p>
          <p className="text-xs text-slate-400">{timeAgo(comment.created_at)}</p>
        </div>

        {String(comment.author_id) === user && (
          <button
            onClick={async () => {
              await deleteComment(comment.id);
              refresh();
            }}
            className="text-red-400 text-xs"
          >
            Delete
          </button>
        )}
      </div>

      <p className="text-slate-300 mt-1">{comment.content}</p>

      <div className="flex gap-4 mt-2 text-sm">
        <button onClick={toggleLike}>👍 {comment.like_count}</button>
        <button onClick={() => setShowReply(!showReply)}>Reply</button>
      </div>

      {showReply && (
        <input
          autoFocus
          value={reply}
          onChange={e => setReply(e.target.value)}
          onKeyDown={submitReply}
          className="mt-2 w-full bg-slate-900 p-2 rounded"
          placeholder="Write reply..."
        />
      )}

      {comment.children?.length > 0 && (
        <div className="ml-4 mt-3 space-y-2 border-l pl-3">
          {comment.children.map(c => (
            <Comment key={c.id} comment={c} postId={postId} refresh={refresh} />
          ))}
        </div>
      )}
    </div>
  );
}
