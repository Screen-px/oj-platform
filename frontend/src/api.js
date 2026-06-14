const BASE = "/api";

export async function fetchProblems() {
  const res = await fetch(`${BASE}/problems`);
  return res.json();
}

export async function fetchProblem(id) {
  const res = await fetch(`${BASE}/problems/${id}`);
  return res.json();
}

export async function submitCode(problem_id, code) {
  const res = await fetch(`${BASE}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ problem_id, code }),
  });
  return res.json();
}
