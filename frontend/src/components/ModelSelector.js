export default function ModelSelector({ model, setModel }) {
  return (
    <select
      value={model}
      onChange={e => setModel(e.target.value)}
      className="border p-2 w-full"
    >
      <option value="gpt-4">GPT-4</option>
      <option value="fallback">Fallback AI</option>
    </select>
  );
}
