from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, get_db
from models import Base, Problem, Submission
from judge import judge
from seed import seed

app = FastAPI(title="转专业OJ平台", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 启动事件 ----------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    seed()


# ---------- 请求体 ----------
class SubmitRequest(BaseModel):
    problem_id: int
    code: str


# ---------- API ----------
@app.get("/api/problems")
def list_problems(db: Session = Depends(get_db)):
    """获取题目列表"""
    problems = db.query(Problem).order_by(Problem.id).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "solved": p.solved,
            "category": p.category,
        }
        for p in problems
    ]


@app.get("/api/problems/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    """获取题目详情（含最近一次提交的代码）"""
    p = db.query(Problem).filter(Problem.id == problem_id).first()
    if not p:
        return {"error": "题目不存在"}
    # 查最近一次提交的代码
    last = db.query(Submission)\
        .filter(Submission.problem_id == problem_id)\
        .order_by(Submission.id.desc()).first()
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "input_format": p.input_format,
        "output_format": p.output_format,
        "sample_input": p.sample_input,
        "sample_output": p.sample_output,
        "hints": p.hints,
        "solved": p.solved,
        "last_code": last.code if last else None,
    }


@app.post("/api/submit")
def submit(req: SubmitRequest, db: Session = Depends(get_db)):
    """提交代码并评测"""
    problem = db.query(Problem).filter(Problem.id == req.problem_id).first()
    if not problem:
        return {"error": "题目不存在"}

    # 评测
    result = judge(req.code, problem.testcases)

    # 保存提交记录
    sub = Submission(
        problem_id=req.problem_id,
        code=req.code,
        status=result["status"],
        details=result["details"],
    )
    db.add(sub)

    # 如果AC，标记题目已通过
    if result["status"] == "AC":
        problem.solved = 1

    db.commit()
    db.refresh(sub)

    return {
        "id": sub.id,
        "status": result["status"],
        "details": result["details"],
    }


@app.get("/api/submissions")
def list_submissions(problem_id: int = None, db: Session = Depends(get_db)):
    """获取提交历史"""
    q = db.query(Submission).order_by(Submission.id.desc())
    if problem_id:
        q = q.filter(Submission.problem_id == problem_id)
    subs = q.limit(50).all()
    return [
        {
            "id": s.id,
            "problem_id": s.problem_id,
            "status": s.status,
            "code": s.code[:200],
            "created_at": str(s.created_at),
        }
        for s in subs
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
