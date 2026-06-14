import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchProblems } from "../api";
import "./ProblemList.css";

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
        <p className="hero-eyebrow">Programming Ability Test</p>
        <h1 className="hero-title">转专业上机考试 · 编程真题集</h1>
        <div className="hero-stats">
          <div className="stat">
            已通过 <span className="stat-number">{ac}</span> / {total} 题
          </div>
        </div>
        {total > 0 && ac === total && (
          <p className="hero-allclear">恭喜！全部题目已通过</p>
        )}
      </header>

      {order.map((cat) =>
        grouped[cat] ? (
          <section key={cat} className="year-section">
            <h2 className="year-heading">{cat}真题</h2>
            <table className="problem-table">
              <thead>
                <tr>
                  <th className="col-id">编号</th>
                  <th className="col-title">题目名称</th>
                  <th className="col-status">状态</th>
                </tr>
              </thead>
              <tbody>
                {grouped[cat].map((p) => (
                  <tr key={p.id} onClick={() => navigate(`/problems/${p.id}`)}>
                    <td className="col-id">{p.id}</td>
                    <td className="col-title">{p.title}</td>
                    <td className="col-status">
                      {p.solved ? (
                        <span className="badge solved">已通过</span>
                      ) : (
                        <span className="badge unsolved">未通过</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        ) : null
      )}
    </div>
  );
}
