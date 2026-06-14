import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchProblem, submitCode } from "../api";
import CodeEditor from "../components/CodeEditor";
import ResultPanel from "../components/ResultPanel";
import "./ProblemDetail.css";

const DEFAULT_CODE = `# 在此编写你的 Python 代码
# 使用 input() 读取输入
# 使用 print() 输出结果
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
        // 有历史代码则恢复，否则用默认模板
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
      setResult({ status: "RE", details: [{ error: "网络请求失败: " + err.message }] });
    }
    setSubmitting(false);
  };

  if (!problem) {
    return <div className="loading">加载中...</div>;
  }

  return (
    <div className="detail-container">
      {/* 顶部标题栏 */}
      <header className="detail-header">
        <button className="back-btn" onClick={() => navigate("/problems")}>
          ← 返回列表
        </button>
        <h1>{problem.title}</h1>
      </header>

      <div className="detail-body">
        {/* 左侧：题目描述 */}
        <div className="description-panel">
          <section>
            <h3>题目描述</h3>
            <div
              className="content"
              dangerouslySetInnerHTML={{ __html: problem.description }}
            />
          </section>

          <section>
            <h3>输入格式</h3>
            <div className="content" dangerouslySetInnerHTML={{ __html: problem.input_format }} />
          </section>

          <section>
            <h3>输出格式</h3>
            <div className="content" dangerouslySetInnerHTML={{ __html: problem.output_format }} />
          </section>

          <section>
            <h3>样例</h3>
            <div className="sample-block">
              <div className="sample-box">
                <span className="sample-label">样例输入</span>
                <pre>{problem.sample_input || "（无）"}</pre>
              </div>
              <div className="sample-box">
                <span className="sample-label">样例输出</span>
                <pre>{problem.sample_output || "（无）"}</pre>
              </div>
            </div>
          </section>

          {problem.hints && (
            <section>
              <h3>提示</h3>
              <div className="content" dangerouslySetInnerHTML={{ __html: problem.hints }} />
            </section>
          )}
        </div>

        {/* 右侧：代码编辑器 + 结果 */}
        <div className="code-panel">
          <div className="editor-wrapper">
            <CodeEditor value={code} onChange={setCode} />
          </div>

          <button className="submit-btn" onClick={handleSubmit} disabled={submitting}>
            {submitting ? "评测中..." : "提交代码"}
          </button>

          {result && <ResultPanel result={result} />}
        </div>
      </div>
    </div>
  );
}
