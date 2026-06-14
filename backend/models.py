from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from database import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)         # HTML/Markdown
    input_format = Column(Text, nullable=False)
    output_format = Column(Text, nullable=False)
    sample_input = Column(Text, nullable=False)
    sample_output = Column(Text, nullable=False)
    hints = Column(Text, default="")
    testcases = Column(JSON, nullable=False)            # [{"input": "...", "output": "..."}, ...]
    solved = Column(Integer, default=0)                 # 0=未通过, 1=已通过
    category = Column(String(50), default="")           # 板块分类，如"2024年"、"2023年"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="judging")  # AC/WA/TLE/RE/judging
    details = Column(JSON, default=list)
    created_at = Column(DateTime, server_default=func.now())
