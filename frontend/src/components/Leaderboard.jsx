export default function Leaderboard({ data }) {
  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 sticky top-24">
      <h2 className="text-xl font-bold text-white mb-6">🏆 Leaderboard</h2>

      {data.length === 0 && (
        <p className="text-slate-400">No data yet</p>
      )}

      {data.map((u, i) => (
        <div key={i} className="flex justify-between mb-3 text-slate-200">
          <span>{i + 1}. {u.username}</span>
          <span className="text-blue-400">{u.total}</span>
        </div>
      ))}
    </div>
  );
}
