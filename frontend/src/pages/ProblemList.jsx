import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchProblems } from "../api";
import "./ProblemList.css";

function ProblemCard({ p, onClick }) {
  const solved = p.solved === 1;
  return (
    <div className={`problem-card ${solved ? "solved" : ""}`} onClick={onClick}>
      <div className="card-left">
        <span className="card-id">{String(p.id).padStart(2, "0")}</span>
      </div>
      <div className="card-body">
        <span className="card-title">{p.title}</span>
      </div>
      <div className="card-right">
        <span className={`card-status ${solved ? "ac" : "pending"}`}>
          {solved ? "已通过" : "未通过"}
        </span>
      </div>
    </div>
  );
}

export default function ProblemList() {
  const [problems, setProblems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProblems().then(setProblems).catch(console.error);
  }, []);

  const grouped = {};
  for (const p of problems) {
    const cat = p.category || "其他";
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(p);
  }
  const order = ["2024年", "2023年"];

  const total = problems.length;
  const ac = problems.filter((p) => p.solved).length;

  return (
    <div className="list-root">
      <header className="list-hero">
        <p className="hero-eyebrow">Transfer Exam · Online Judge</p>
        <h1 className="hero-title">转专业上机真题</h1>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-number">{ac}</span>
            <span className="stat-label">已通过</span>
          </div>
          <div className="stat-divider" />
          <div className="stat">
            <span className="stat-number">{total}</span>
            <span className="stat-label">共 {total} 题</span>
          </div>
        </div>
        {total > 0 && ac === total && (
          <p className="hero-allclear">全部通关！</p>
        )}
      </header>

      <div className="list-content">
        {order.map((cat) =>
          grouped[cat] ? (
            <section key={cat} className="year-section">
              <h2 className="year-heading">{cat}真题</h2>
              <div className="card-group">
                {grouped[cat].map((p) => (
                  <ProblemCard
                    key={p.id}
                    p={p}
                    onClick={() => navigate(`/problems/${p.id}`)}
                  />
                ))}
              </div>
            </section>
          ) : null
        )}
      </div>
    </div>
  );
}
