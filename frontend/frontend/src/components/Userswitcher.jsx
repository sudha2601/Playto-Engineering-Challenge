export default function UserSwitcher() {
  const users = [
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" },
    { id: 3, name: "Charlie" },
  ];

  if (!localStorage.getItem("user")) localStorage.setItem("user", "1");

  return (
    <select
      defaultValue={localStorage.getItem("user")}
      onChange={e => {
        localStorage.setItem("user", e.target.value);
        location.reload();
      }}
      className="bg-slate-700 text-white p-2 rounded"
    >
      {users.map(u => (
        <option key={u.id} value={u.id}>
          {u.name}
        </option>
      ))}
    </select>
  );
}
