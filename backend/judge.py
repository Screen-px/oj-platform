import subprocess
import tempfile
import os


TIME_LIMIT = 3


def run_test(code: str, input_data: str, files: dict = None) -> dict:
    result = {"output": "", "error": "", "status": "AC"}
    tmpdir = tempfile.mkdtemp()
    code_path = os.path.join(tmpdir, "solution.py")
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code)
    # 创建题目需要的文件（如 input.txt）
    if files:
        for fname, fcontent in files.items():
            with open(os.path.join(tmpdir, fname), "w", encoding="utf-8") as f:
                f.write(fcontent)
    try:
        proc = subprocess.run(
            ["python", code_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=TIME_LIMIT,
            cwd=tmpdir,
        )
        if proc.returncode != 0:
            result["status"] = "RE"
            result["error"] = proc.stderr.strip()
        else:
            result["output"] = proc.stdout.strip()
            result["status"] = "AC"
    except subprocess.TimeoutExpired:
        result["status"] = "TLE"
        result["error"] = "代码执行超时（超过3秒）"
    except Exception as e:
        result["status"] = "RE"
        result["error"] = str(e)
    finally:
        try:
            import shutil
            shutil.rmtree(tmpdir)
        except OSError:
            pass
    return result


def normalize(s: str) -> str:
    return s.rstrip()


# ---------- 自定义校验器 ----------

def check_cards_equalize(input_data: str, output: str) -> dict:
    """均分纸牌：校验输出是否是一组合法的最优移动方案"""
    lines = output.strip().split("\n")
    try:
        M = int(lines[0].strip())
    except (ValueError, IndexError):
        return {"status": "WA", "error": "第一行应为一个整数（最少移动次数）",
                "expected": "(整数)", "actual": lines[0] if lines else "(空)"}

    # 解析输入
    parts = input_data.strip().split()
    N = int(parts[0])
    cards = list(map(int, parts[1:]))
    avg = sum(cards) // N

    # 理论最少步数 = 前缀和 ≠ i*avg 的次数（i=1..N-1）
    prefix = 0
    min_moves = 0
    for i in range(N - 1):
        prefix += cards[i]
        if prefix != avg * (i + 1):
            min_moves += 1

    if M != min_moves:
        return {"status": "WA",
                "expected": str(min_moves), "actual": str(M),
                "error": f"最少移动次数应为 {min_moves}，你输出 {M}"}

    # 模拟移动（允许中间状态出现负数，仅验证最终结果）
    sim = cards[:]
    for i, line in enumerate(lines[1:M + 1], start=1):
        try:
            x, y, z = map(int, line.strip().split())
        except ValueError:
            return {"status": "WA", "error": f"第{i}行格式错误，应为 x y z"}

        if not (1 <= x <= N and 1 <= y <= N):
            return {"status": "WA", "error": f"第{i}行堆编号越界"}
        if abs(x - y) != 1:
            return {"status": "WA", "error": f"第{i}行：{x}和{y}不相邻"}
        if z <= 0:
            return {"status": "WA", "error": f"第{i}行：移动张数必须为正"}

        sim[x - 1] -= z
        sim[y - 1] += z

    if sim != [avg] * N:
        return {"status": "WA",
                "expected": " ".join(str(avg) for _ in range(N)),
                "actual": " ".join(map(str, sim)),
                "error": "移动后各堆未达到平均数"}

    return {"status": "AC"}


CHECKERS = {
    "cards_equalize": check_cards_equalize,
}


# ---------- 主评测逻辑 ----------

def judge(code: str, testcases: list) -> dict:
    details = []
    final_status = "AC"

    for i, tc in enumerate(testcases):
        input_data = tc.get("input", "")
        checker_name = tc.get("checker", None)

        r = run_test(code, input_data, tc.get("files"))
        r["test_index"] = i + 1

        if r["status"] == "AC" and checker_name and checker_name in CHECKERS:
            cr = CHECKERS[checker_name](input_data, r["output"])
            r.update(cr)
        elif r["status"] == "AC":
            expected = normalize(tc.get("output", ""))
            actual = normalize(r["output"])
            if actual == expected:
                r["status"] = "AC"
            else:
                r["status"] = "WA"
                r["expected"] = expected
                r["actual"] = actual

        details.append(r)
        if r["status"] != "AC" and final_status == "AC":
            final_status = r["status"]

    return {"status": final_status, "details": details}
