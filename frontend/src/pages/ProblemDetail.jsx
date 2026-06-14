import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchProblem, submitCode } from "../api";
import CodeEditor from "../components/CodeEditor";
import ResultPanel from "../components/ResultPanel";
import "./ProblemDetail.css";

const DEFAULT_CODE = `# 在此编写你的 Python 代码
`;

export default function ProblemDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState(DEFAULT_CODE);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchProblem(id)
      .then((data) => {
        setProblem(data);
        setCode(DEFAULT_CODE);
        setResult(null);
      })
      .catch(console.error);
  }, [id]);

  const handleSubmit = async () => {
    setSubmitting(true);
    setResult({ status: "judging", details: [] });
    try {
      const res = await submitCode(parseInt(id), code);
      setResult(res);
    } catch (err) {
      setResult({ status: "RE", details: [{ error: "请求失败: " + err.message }] });
    }
    setSubmitting(false);
  };

  if (!problem) {
    return <div className="loading">加载中...</div>;
  }

  return (
    <div className="detail-root">
      {/* 顶栏 */}
      <header className="detail-topbar">
        <button className="back-link" onClick={() => navigate("/problems")}>
          ← 返回列表
        </button>
        <span className="topbar-divider">/</span>
        <span className="topbar-title">{problem.title}</span>
        {problem.solved === 1 && <span className="topbar-badge">已通过</span>}
      </header>

      <div className="detail-split">
        {/* 左侧：题目 */}
        <aside className="desc-pane">
          <section className="desc-section">
            <h3 className="desc-heading">题目描述</h3>
            <div className="desc-body" dangerouslySetInnerHTML={{ __html: problem.description }} />
          </section>

          <section className="desc-section">
            <h3 className="desc-heading">输入格式</h3>
            <div className="desc-body" dangerouslySetInnerHTML={{ __html: problem.input_format }} />
          </section>

          <section className="desc-section">
            <h3 className="desc-heading">输出格式</h3>
            <div className="desc-body" dangerouslySetInnerHTML={{ __html: problem.output_format }} />
          </section>

          <section className="desc-section">
            <h3 className="desc-heading">样例</h3>
            <div className="sample-row">
              <div className="sample-cell">
                <span className="sample-tag">输入</span>
                <pre>{problem.sample_input || "（无）"}</pre>
              </div>
              <div className="sample-cell">
                <span className="sample-tag">输出</span>
                <pre>{problem.sample_output || "（无）"}</pre>
              </div>
            </div>
          </section>

          {problem.hints && (
            <section className="desc-section">
              <h3 className="desc-heading">提示</h3>
              <div className="desc-body" dangerouslySetInnerHTML={{ __html: problem.hints }} />
            </section>
          )}
        </aside>

        {/* 右侧：编辑器 + 结果 */}
        <main className="editor-pane">
          <div className="editor-area">
            <CodeEditor value={code} onChange={setCode} />
          </div>

          <button className="submit-btn" onClick={handleSubmit} disabled={submitting}>
            {submitting ? "评测中..." : "提交代码"}
          </button>

          {result && <ResultPanel result={result} />}
        </main>
      </div>
    </div>
  );
}
