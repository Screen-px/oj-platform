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

  // 按 category 分组
  const grouped = {};
  for (const p of problems) {
    const cat = p.category || "其他";
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(p);
  }

  // 保持板块顺序
  const order = ["2024年", "2023年"];

  return (
    <div className="list-container">
      <header className="list-header">
        <h1>转专业上机考试 · 刷题平台</h1>
        <p>共 {problems.length} 道真题</p>
      </header>

      {order.map((cat) =>
        grouped[cat] ? (
          <div key={cat} className="category-section">
            <h2 className="category-title">{cat}真题</h2>
            <table className="problem-table">
              <thead>
                <tr>
                  <th className="col-id">#</th>
                  <th className="col-title">题目</th>
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
          </div>
        ) : null
      )}
    </div>
  );
}
