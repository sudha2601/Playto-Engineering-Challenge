import { useEffect, useState } from "react";
import Feed from "./components/Feed";
import Leaderboard from "./components/Leaderboard";
import UserSwitcher from "./components/UserSwitcher";
import { getLeaderboard } from "./api";

export default function App() {
  const [leaderboard, setLeaderboard] = useState([]);

  const refreshLeaderboard = () => {
    getLeaderboard().then(setLeaderboard);
  };

  useEffect(() => {
    refreshLeaderboard();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <nav className="bg-black/40 backdrop-blur p-4 flex justify-between">
        <h1 className="text-xl font-bold">Playto</h1>
        <UserSwitcher />
      </nav>

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 p-8">
        <div className="lg:col-span-2">
          <Feed refreshLeaderboard={refreshLeaderboard} />
        </div>

        <Leaderboard data={leaderboard} />
      </div>
    </div>
  );
}
