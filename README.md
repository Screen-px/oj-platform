# 转专业OJ刷题平台 · 启动说明

## 第一次使用

### 1. 检查环境

确保电脑已安装 Python 3.10+ 和 Node.js 18+。

```bash
python --version   # 应显示 Python 3.10 或更高
node --version     # 应显示 v18 或更高
```

### 2. 安装依赖（仅首次需要）

打开 CMD（命令提示符），分别安装后端和前端的依赖：

```bash
cd 你存放的路径\oj-platform\backend
pip install -r requirements.txt

cd 你存放的路径\oj-platform\frontend
npm install
```

## 每次启动（需要两个终端窗口）

### 终端1：启动后端

打开 CMD，运行：

```bash
cd 你存放的路径\oj-platform\backend
python main.py
```

看到 `Uvicorn running on http://127.0.0.1:8000` 表示后端启动成功。**这个窗口不要关。**

### 终端2：启动前端

再打开一个 CMD，运行：

```bash
cd 你存放的路径\oj-platform\frontend
npm run dev
```

看到 `http://localhost:5173` 表示前端启动成功。**这个窗口也不要关。**

### 3. 打开浏览器

访问 **http://localhost:5173** 即可开始刷题。

## 常见问题

**Q: 提交代码报错"网络请求失败"？**
A: 后端没启动。确认终端1正常运行。

**Q: 页面打不开？**
A: 前端没启动。确认终端2正常运行。

**Q: PowerShell 报"禁止运行脚本"？**
A: 换成 CMD（命令提示符）运行，不要用 PowerShell。

**Q: pip install 报错？**
A: 尝试 `python -m pip install -r requirements.txt`

**Q: npm install 很慢？**
A: 运行 `npm config set registry https://registry.npmmirror.com` 后再试。

## 评测说明

- 每题有多组隐藏测试用例，结果包括：AC(通过) / WA(答案错误) / TLE(超时) / RE(运行错误)
- 每组测试限时 3 秒
- 输出对比会忽略末尾多余的空白字符
- 每次提交的代码和结果会保存在本地数据库中
