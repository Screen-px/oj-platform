import "./ResultPanel.css";

export default function ResultPanel({ result }) {
  if (!result) return null;

  const { status, details } = result;
  const statusConfig = {
    AC: { label: "通过", icon: "✓", cls: "ac" },
    WA: { label: "答案错误", icon: "✗", cls: "wa" },
    TLE: { label: "运行超时", icon: "⏱", cls: "tle" },
    RE: { label: "运行错误", icon: "!", cls: "re" },
    judging: { label: "评测中...", icon: "●", cls: "judging" },
  };
  const cfg = statusConfig[status] || statusConfig.RE;

  return (
    <div className="result-panel">
      <div className={`result-status ${cfg.cls}`}>
        <span className="result-icon">{cfg.icon}</span>
        <span>{cfg.label}</span>
      </div>

      {details && details.length > 0 && (
        <div className="result-details">
          {details.map((d, i) => (
            <div key={i} className={`test-row ${d.status?.toLowerCase() || ""}`}>
              <div className="test-header">
                <span className="test-name">测试 {d.test_index || i + 1}</span>
                <span className={`test-badge ${(d.status || "").toLowerCase()}`}>
                  {d.status}
                </span>
              </div>
              {d.error && <div className="test-error">{d.error}</div>}
              {d.status === "WA" && (
                <div className="test-diff">
                  <div className="diff-line">
                    <span className="diff-label">期望输出</span>
                    <pre>{d.expected}</pre>
                  </div>
                  <div className="diff-line">
                    <span className="diff-label">实际输出</span>
                    <pre>{d.actual}</pre>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
