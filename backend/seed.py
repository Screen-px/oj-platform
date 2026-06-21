"""初始化10道题目及其测试用例"""

from database import engine, SessionLocal
from models import Base, Problem


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Problem).count() > 0:
        print("题目已存在，跳过初始化")
        db.close()
        return

    problems = [
        # ========== 第1题 ==========
        {
            "title": "第1题·字符串输出",
            "description": """请编写程序，按照下列要求依次输出四行内容：

① 第一行输出：<code>Welcome to "C Programming" Exam!</code>
② 第二行输出：<code>通过率：85%</code>
③ 第三行输出一个空行（即只换行，不输出任何文字）
④ 第四行输出：<code>(A+B)*C 的结果取决于输入。</code>

<strong>注意：</strong>需与题目要求完全一致（含中英文标点、空格、引号）。""",
            "input_format": "本题无输入。",
            "output_format": "按要求输出四行文本。",
            "sample_input": "",
            "sample_output": """Welcome to "C Programming" Exam!
通过率：85%

(A+B)*C 的结果取决于输入。""",
            "hints": "使用 print() 函数，注意双引号和百分号的输出。",
            "testcases": [
                {"input": "", "output": """Welcome to "C Programming" Exam!\n通过率：85%\n\n(A+B)*C 的结果取决于输入。"""}
            ],
        },

        # ========== 第2题 ==========
        {
            "title": "第2题·A+B 问题",
            "description": """输入两个整数 <strong>a</strong> 和 <strong>b</strong>，输出它们的和。""",
            "input_format": "一行，包含两个整数 a 和 b，中间用空格分隔。",
            "output_format": "一个整数，即 a + b 的结果。",
            "sample_input": "3 5",
            "sample_output": "8",
            "hints": "使用 input().split() 读取，int() 转换类型。",
            "testcases": [
                {"input": "3 5\n",      "output": "8"},
                {"input": "0 0\n",      "output": "0"},
                {"input": "-10 10\n",   "output": "0"},
                {"input": "999 1001\n", "output": "2000"},
            ],
        },

        # ========== 第3题 ==========
        {
            "title": "第3题·阶梯电费",
            "description": """某地区实行阶梯电价：

• 月用电量 0~2880 度（含）：<strong>0.448 元/度</strong>
• 月用电量 2880~4800 度（含）：<strong>0.578 元/度</strong>
• 月用电量 4800 度以上：<strong>0.768 元/度</strong>

输入用户本月用电量 <strong>n</strong>（度），计算本月应缴电费（结果保留两位小数）。""",
            "input_format": "一行，一个非负整数 n，表示用电量（度），n ≤ 10000。",
            "output_format": "一行，一个保留两位小数的浮点数（单位：元）。",
            "sample_input": "2000",
            "sample_output": "896.00",
            "hints": "使用 if-elif-else 分支结构，f-string 格式化输出。",
            "testcases": [
                {"input": "0\n",           "output": "0.00"},
                {"input": "2000\n",        "output": "896.00"},
                {"input": "2880\n",        "output": "1290.24"},
                {"input": "3500\n",        "output": "1648.60"},
                {"input": "4800\n",        "output": "2400.00"},
                {"input": "5000\n",        "output": "2553.60"},
            ],
        },

        # ========== 第4题 ==========
        {
            "title": "第4题·电费进阶——预付费卡",
            "description": """小明家里使用预付费电表，采用<strong>第3题的阶梯电价</strong>计费。

小明在每个月初（1号）向电卡中存入固定金额。电力公司在每月末从卡中扣除当月电费。

如果某月扣除电费后<strong>卡内余额变为负数（&lt; 0）</strong>，则该月发生断电，<strong>输出断电的月份编号（1~12）并立刻终止模拟</strong>（断电后不再有用电和扣费，只输出第一次断电的月份）。
如果全年都未断电，则输出12个月后卡内剩余金额（保留两位小数）。""",
            "input_format": """<strong>第一行：</strong>12个整数，分别表示第1~12月的用电量（度），空格分隔。
<strong>第二行：</strong>12个整数，分别表示第1~12月初存入的金额（元），空格分隔。""",
            "output_format": """如果发生断电：输出一个整数（断电月份，1~12）。
如果全年未断电：输出一个浮点数，保留两位小数（年末余额）。""",
            "sample_input": "300 300 400 350 380 420 360 340 390 370 350 380\n140 140 140 150 150 150 160 160 150 150 160 160",
            "sample_output": "3",
            "hints": "使用列表存储数据，for循环逐月模拟，复用第3题的电费计算逻辑。断电后使用 break 终止循环。",
            "testcases": [
                {
                    "input": "300 300 400 350 380 420 360 340 390 370 350 380\n140 140 140 150 150 150 160 160 150 150 160 160",
                    "output": "3"
                },
                {
                    "input": "200 200 250 300 280 260 240 230 250 270 290 310\n200 200 200 200 200 200 200 200 200 200 200 200",
                    "output": "1020.16"
                },
            ],
        },

        # ========== 第5题 ==========
        {
            "title": "第5题·圆柱体的表面积和体积",
            "description": """输入圆柱体的底面半径 <strong>r</strong> 和高 <strong>h</strong>，计算并输出表面积和体积。

π 取 <strong>3.14159</strong>，结果均保留两位小数。

<strong>公式：</strong>
• 表面积 S = 2πr² + 2πrh（两个底面积 + 侧面积）
• 体积 V = πr²h""",
            "input_format": "一行，两个正浮点数 r 和 h，空格分隔。",
            "output_format": "第一行输出表面积，第二行输出体积，均保留两位小数。",
            "sample_input": "2.5 6.0",
            "sample_output": "133.52\n117.81",
            "hints": "定义常量 PI，注意浮点数计算精度，使用 f-string 格式化。",
            "testcases": [
                {"input": "1.0 1.0\n",   "output": "12.57\n3.14"},
                {"input": "2.5 6.0\n",   "output": "133.52\n117.81"},
                {"input": "3.0 10.0\n",  "output": "245.04\n282.74"},
            ],
        },

        # ========== 第6题 ==========
        {
            "title": "第6题·果茶成本计算",
            "description": """一种果茶由 <strong>n</strong> 种水果混合制成，制作时<strong>每种水果花费的总金额相同</strong>（即每种水果各花 M 元购买）。

现给出每种水果的单价（元/千克），请计算该果茶每千克的成本是多少元，结果保留两位小数。

<strong>推导：</strong>
假设每种水果花费 M 元，则第 i 种水果可购买 M/pᵢ 千克。
总质量 = M × Σ(1/pᵢ) 千克，总花费 = n × M 元。
每千克成本 = n×M / (M×Σ(1/pᵢ)) = <strong>n / Σ(1/pᵢ)</strong>（M 可约去）。""",
            "input_format": """<strong>第一行：</strong>一个整数 n，表示水果种类数（n ≥ 1）。
<strong>第二行：</strong>n 个浮点数，表示每种水果的单价（元/千克），空格分隔。""",
            "output_format": "一个浮点数，保留两位小数，表示每千克果茶的成本。",
            "sample_input": "3\n3.0 6.0 2.0",
            "sample_output": "3.00",
            "hints": "关键在于推导出成本 = n / Σ(1/pᵢ)，用循环或 sum() 求和。",
            "testcases": [
                {"input": "3\n3.0 6.0 2.0\n",                          "output": "3.00"},
                {"input": "3\n5.0 10.0 5.0\n",                         "output": "6.00"},
                {"input": "2\n10.0 10.0\n",                             "output": "10.00"},
            ],
        },

        # ========== 第7题 ==========
        {
            "title": "第7题·从大到小排序",
            "description": """输入 n 个整数，将它们<strong>从大到小</strong>排序后输出。""",
            "input_format": """<strong>第一行：</strong>一个整数 n（1 ≤ n ≤ 1000），表示数字个数。
<strong>第二行：</strong>n 个整数，空格分隔。""",
            "output_format": "一行，排序后的 n 个整数，从大到小，空格分隔。",
            "sample_input": "5\n3 1 4 1 5",
            "sample_output": "5 4 3 1 1",
            "hints": "可使用 Python 内置 sorted() 或 list.sort(reverse=True)，也可手写排序算法。",
            "testcases": [
                {"input": "5\n3 1 4 1 5\n",         "output": "5 4 3 1 1"},
                {"input": "1\n42\n",                  "output": "42"},
                {"input": "6\n-1 -5 0 3 -2 8\n",     "output": "8 3 0 -1 -2 -5"},
                {"input": "3\n100 200 150\n",         "output": "200 150 100"},
            ],
        },

        # ========== 第8题 ==========
        {
            "title": "第8题·小明刷题",
            "description": """小明计划刷完 <strong>n</strong> 道编程题。

他<strong>工作日（周一至周五）每天做 a 道题</strong>，<strong>周末（周六、周日）每天做 b 道题</strong>。
小明从<strong>下周一开始</strong>做题，每天不间断，直到完成全部 n 道题为止。

问一共需要多少天？（<strong>注意：</strong>最后一天可能不需要做满当天的题量，做完即止）""",
            "input_format": "一行，三个整数 a, b, n，空格分隔。0 ≤ a, b ≤ 100，1 ≤ n ≤ 10⁹。",
            "output_format": "一个整数，表示需要的总天数。",
            "sample_input": "2 4 50",
            "sample_output": "20",
            "hints": "用数学方法（整除+取余）避免暴力循环，否则大数据会超时。每周 = 5a+2b 道题。",
            "testcases": [
                {"input": "3 5 100\n",  "output": "28"},
                {"input": "2 4 50\n",   "output": "20"},
                {"input": "10 10 100\n", "output": "10"},
                {"input": "1 1 15\n",   "output": "15"},
            ],
        },

        # ========== 第9题 ==========
        {
            "title": "第9题·孙尚香招亲——BMI选拔",
            "description": """孙尚香举办招亲大会，要求候选者的 <strong>BMI</strong> 在 <strong>[18.0, 24.0]</strong> 范围内才算合格。

<strong>BMI 计算公式：</strong>BMI = 体重(kg) ÷ 身高(m)²

若有多人合格，取 BMI <strong>最接近该区间中位数 21.0</strong> 的人胜出（即 |BMI - 21.0| 最小）。
若距离相同，按输入顺序取靠前者。
<strong>若无人合格，输出 0。</strong>

<strong>注意：</strong>输入的身高单位为 <strong>cm</strong>，需除以 100 转换为 m。""",
            "input_format": """<strong>第一行：</strong>一个整数 n（1 ≤ n ≤ 100），表示候选者人数。
<strong>接下来 n 行：</strong>每行包含候选者的姓名（不含空格）、身高（cm，整数）、体重（kg，整数），空格分隔。""",
            "output_format": "胜出者的姓名；若无人合格，输出 0。",
            "sample_input": "3\nliubei 183 75\nguanyu 210 110\nsunquan 180 70",
            "sample_output": "sunquan",
            "hints": "用列表存储 (name, bmi)，筛选后比较 |bmi-21.0| 的距离。",
            "testcases": [
                {
                    "input": "3\nliubei 183 75\nguanyu 210 110\nsunquan 180 70",
                    "output": "sunquan"
                },
                {
                    "input": "2\nzhangfei 185 110\nzhaoyun 190 80",
                    "output": "zhaoyun"
                },
                {
                    "input": "1\nlvbu 200 50",
                    "output": "0"
                },
            ],
        },

        # ========== 第10题 ==========
        {
            "title": "第10题·密码强度检测",
            "description": """编写程序判断密码的安全等级（复杂度），规则如下：

<strong>非法字符检查（优先判断）：</strong>若密码中包含以下任意字符，直接判定密码<strong>不合法，输出 0</strong>：
<code>@ ¥ ? ! % $</code>

<strong>合法密码按类型数分级：</strong>
• <strong>一级（输出 1）</strong>：仅含大写字母、或仅含小写字母、或仅含数字（只有一种类型字符）；
• <strong>二级（输出 2）</strong>：包含大写字母、小写字母、数字中的<strong>恰好两种</strong>类型；
• <strong>三级（输出 3）</strong>：<strong>同时包含</strong>大写字母、小写字母、数字三种类型。

<strong>注意：</strong>密码中可包含其他字符（如下划线 _ 等），但不计入类型判断。""",
            "input_format": "一行，一个非空字符串（密码），长度不超过 100。",
            "output_format": "一个整数：0（不合法）、1（一级）、2（二级）、3（三级）。",
            "sample_input": "Abc123",
            "sample_output": "3",
            "hints": "遍历字符串，使用 .isupper()/.islower()/.isdigit() 方法，用布尔标志位统计类型数。",
            "testcases": [
                {"input": "Abc123\n",       "output": "3"},
                {"input": "abc@123\n",      "output": "0"},
                {"input": "ABC123\n",       "output": "2"},
                {"input": "hello\n",        "output": "1"},
                {"input": "HELLO\n",        "output": "1"},
                {"input": "12345\n",        "output": "1"},
                {"input": "Abc_123\n",      "output": "3"},
                {"input": "Abc!def\n",      "output": "0"},
            ],
        },

        # ========== 第11题 ==========
        {
            "title": "第11题·判断闰年",
            "description": """输入一个年份，判断其是否为<strong>闰年</strong>。

<strong>闰年规则：</strong>能被4整除但不能被100整除的年份，或者能被400整除的年份。

要求使用<strong>函数封装</strong>判断逻辑，函数返回 True/False，主函数调用并输出结果。""",
            "input_format": "一行，一个整数 year（1 ≤ year ≤ 9999）。",
            "output_format": "如果是闰年输出 YES，否则输出 NO。",
            "sample_input": "2000",
            "sample_output": "YES",
            "hints": "定义 is_leap(year) 函数，返回布尔值。",
            "testcases": [
                {"input": "2000\n", "output": "YES"},
                {"input": "1900\n", "output": "NO"},
                {"input": "2024\n", "output": "YES"},
                {"input": "2025\n", "output": "NO"},
                {"input": "4\n",    "output": "YES"},
                {"input": "100\n",  "output": "NO"},
            ],
        },

        # ========== 第12题 ==========
        {
            "title": "第12题·判断素数",
            "description": """输入一个正整数 <strong>n</strong>，判断其是否为<strong>素数</strong>（质数）。

素数是指大于1且只能被1和自身整除的正整数。

要求用<strong>函数封装</strong>判断过程（函数返回 True/False），主函数调用并输出结果。""",
            "input_format": "一行，一个正整数 n（1 ≤ n ≤ 10000）。",
            "output_format": "如果是素数输出 YES，否则输出 NO。",
            "sample_input": "17",
            "sample_output": "YES",
            "hints": "定义 is_prime(n) 函数，只需遍历到 sqrt(n)，注意 n=1 不是素数。",
            "testcases": [
                {"input": "17\n",  "output": "YES"},
                {"input": "1\n",   "output": "NO"},
                {"input": "2\n",   "output": "YES"},
                {"input": "100\n", "output": "NO"},
                {"input": "97\n",  "output": "YES"},
            ],
        },

        # ========== 第13题 ==========
        {
            "title": "第13题·数组最大值及位置",
            "description": """输入10个整数，找出其中的<strong>最大值</strong>及其<strong>下标位置</strong>（下标从0开始）。

如果有多个最大值，输出<strong>第一个</strong>出现的下标。要求使用<strong>数组（列表）</strong>实现。""",
            "input_format": "一行，10个整数，空格分隔。",
            "output_format": "一行，输出两个整数：最大值 和 其下标位置，空格分隔。",
            "sample_input": "3 8 2 8 5 1 9 4 9 6",
            "sample_output": "9 6",
            "hints": "遍历数组，维护 max_val 和 max_idx，遇到更大的值就更新。",
            "testcases": [
                {"input": "3 8 2 8 5 1 9 4 7 6\n", "output": "9 6"},
                {"input": "1 2 3 4 5 6 7 8 9 10\n", "output": "10 9"},
                {"input": "-1 -5 -3 -8 -2 -4 -6 -7 -9 0\n", "output": "0 9"},
                {"input": "5 5 5 5 5 5 5 5 5 5\n", "output": "5 0"},
            ],
        },

        # ========== 第14题 ==========
        {
            "title": "第14题·字符串逆序",
            "description": """输入一个字符串，输出其<strong>逆序</strong>（反转后的字符串）。

要求<strong>手动实现</strong>逆序逻辑，不使用 Python 内置的 <code>reversed()</code> 或切片 <code>[::-1]</code> 等快捷方式。""",
            "input_format": "一行，一个非空字符串（长度不超过1000，不含空格）。",
            "output_format": "一行，逆序后的字符串。",
            "sample_input": "hello",
            "sample_output": "olleh",
            "hints": "从最后一个字符开始倒序遍历，逐个拼接。",
            "testcases": [
                {"input": "hello\n",    "output": "olleh"},
                {"input": "abc123\n",   "output": "321cba"},
                {"input": "A\n",        "output": "A"},
                {"input": "ab\n",       "output": "ba"},
            ],
        },

        # ========== 第15题 ==========
        {
            "title": "第15题·冒泡排序",
            "description": """输入一个整数数组，使用<strong>冒泡排序</strong>算法对数组进行<strong>从大到小</strong>排序并输出结果。

要求使用<strong>函数</strong>封装冒泡排序过程。""",
            "input_format": """<strong>第一行：</strong>一个整数 n（1 ≤ n ≤ 100），表示数组元素个数。
<strong>第二行：</strong>n 个整数，空格分隔。""",
            "output_format": "一行，排序后的 n 个整数，从大到小，空格分隔。",
            "sample_input": "5\n3 1 4 1 5",
            "sample_output": "5 4 3 1 1",
            "hints": "定义 bubble_sort(arr) 函数，双层循环：外层控制轮数，内层逐对比较交换。",
            "testcases": [
                {"input": "5\n3 1 4 1 5\n",     "output": "5 4 3 1 1"},
                {"input": "4\n10 20 30 40\n",   "output": "40 30 20 10"},
                {"input": "1\n42\n",              "output": "42"},
                {"input": "6\n-1 -5 0 3 -2 8\n", "output": "8 3 0 -1 -2 -5"},
            ],
        },

        # ========== 第16题 ==========
        {
            "title": "第16题·二分查找",
            "description": """在一个<strong>递增有序</strong>数组中查找某个给定的整数，输出其<strong>下标</strong>（从0开始），找不到则输出 <strong>-1</strong>。

要求使用<strong>函数实现二分查找算法</strong>（非顺序查找），时间复杂度 O(log n)。""",
            "input_format": """<strong>第一行：</strong>两个整数 n 和 x，空格分隔，n 为数组长度，x 为目标值。
<strong>第二行：</strong>n 个递增有序的整数，空格分隔。""",
            "output_format": "一个整数，x 在数组中的下标（0-based），找不到输出 -1。",
            "sample_input": "5 7\n1 3 5 7 9",
            "sample_output": "3",
            "hints": "定义 binary_search(arr, x) 函数，维护 left 和 right 指针，每次取 mid 比较。",
            "testcases": [
                {"input": "5 7\n1 3 5 7 9\n",       "output": "3"},
                {"input": "4 3\n1 2 4 5\n",         "output": "-1"},
                {"input": "1 1\n1\n",               "output": "0"},
                {"input": "6 2\n1 2 3 4 5 6\n",     "output": "1"},
                {"input": "7 10\n1 3 5 7 9 10 12\n", "output": "5"},
            ],
        },

        # ========== 第17题 ==========
        {
            "title": "第17题·斐波那契数列",
            "description": """输出斐波那契数列的前 <strong>n</strong> 项（n ≤ 50）。

斐波那契数列定义：F(1)=1, F(2)=1, F(n)=F(n−1)+F(n−2)。

要求使用<strong>数组和循环</strong>方式，<strong>非递归</strong>实现。""",
            "input_format": "一行，一个整数 n（1 ≤ n ≤ 50）。",
            "output_format": "一行，前 n 个斐波那契数，空格分隔。",
            "sample_input": "5",
            "sample_output": "1 1 2 3 5",
            "hints": "初始化列表 fib=[1,1]，然后循环追加 fib[i-1]+fib[i-2]，注意 n=1 的特殊情况。",
            "testcases": [
                {"input": "5\n",    "output": "1 1 2 3 5"},
                {"input": "1\n",    "output": "1"},
                {"input": "2\n",    "output": "1 1"},
                {"input": "10\n",   "output": "1 1 2 3 5 8 13 21 34 55"},
            ],
        },

        # ========== 第18题 ==========
        {
            "title": "第18题·学生成绩排序",
            "description": """定义结构体表示学生（包含<strong>学号、姓名、成绩</strong>），输入若干学生信息，按<strong>成绩从高到低</strong>排序后输出。若成绩相同则<strong>保持输入顺序</strong>。

要求使用<strong>结构体（Python 中可用列表/元组/字典模拟）+ 排序算法</strong>实现。""",
            "input_format": """<strong>第一行：</strong>一个整数 n（1 ≤ n ≤ 100），表示学生人数。
<strong>接下来 n 行：</strong>每行包含学号（字符串）、姓名（字符串）、成绩（整数），空格分隔。""",
            "output_format": "n 行，每行学号、姓名、成绩，按成绩从高到低输出。",
            "sample_input": "3\n001 Alice 85\n002 Bob 92\n003 Carol 78",
            "sample_output": "002 Bob 92\n001 Alice 85\n003 Carol 78",
            "hints": "使用列表存储元组 (id, name, score)，用 sorted() 按 score 降序排序，stable=True。",
            "testcases": [
                {"input": "3\n001 Alice 85\n002 Bob 92\n003 Carol 78\n",
                 "output": "002 Bob 92\n001 Alice 85\n003 Carol 78"},
                {"input": "4\nS001 Zhang 88\nS002 Li 95\nS003 Wang 88\nS004 Zhao 72\n",
                 "output": "S002 Li 95\nS001 Zhang 88\nS003 Wang 88\nS004 Zhao 72"},
                {"input": "1\nX01 Test 60\n",
                 "output": "X01 Test 60"},
            ],
        },

        # ========== 第19题 ==========
        {
            "title": "第19题·判断回文数",
            "description": """输入一个正整数，判断它是否为<strong>回文数</strong>（正着读和反着读一样）。

例如：12321 是回文数，12345 不是回文数。

要求：<strong>不能使用字符串转换</strong>（不能用 str()、切片等），只能使用<strong>整型运算</strong>（取余、整除等）实现。""",
            "input_format": "一行，一个正整数 n（1 ≤ n ≤ 10⁹）。",
            "output_format": "是回文数输出 YES，否则输出 NO。",
            "sample_input": "12321",
            "sample_output": "YES",
            "hints": "通过 %10 取个位，//10 去掉个位，构建反转数，最后与原数比较。",
            "testcases": [
                {"input": "12321\n",   "output": "YES"},
                {"input": "12345\n",   "output": "NO"},
                {"input": "1\n",       "output": "YES"},
                {"input": "11\n",      "output": "YES"},
                {"input": "10\n",      "output": "NO"},
                {"input": "123321\n",  "output": "YES"},
            ],
        },

        # ========== 第20题 ==========
        {
            "title": "第20题·统计文件字符类型个数",
            "description": """打开文本文件 <code>input.txt</code>，读取全部内容，统计其中：

• <strong>字母</strong>个数（a-z, A-Z）
• <strong>数字</strong>个数（0-9）
• <strong>空格</strong>个数（仅空格 ' '，不含换行、制表符）
• <strong>其他字符</strong>个数（除字母、数字、空格外的所有字符，含标点、换行等）

<strong>注意：</strong>评测时会在代码同级目录准备好 input.txt 文件，直接用 <code>open('input.txt')</code> 打开即可。""",
            "input_format": "无控制台输入（数据在 input.txt 文件中）。",
            "output_format": "四行，每行一个整数，依次为：字母个数、数字个数、空格个数、其他字符个数。",
            "sample_input": "",
            "sample_output": "14\n3\n2\n2",
            "hints": "用 open('input.txt', encoding='utf-8') 打开，.read() 读取全部内容，遍历每个字符用 .isalpha() / .isdigit() 或 ASCII 码判断。",
            "testcases": [
                {
                    "input": "",
                    "files": {"input.txt": "Hello World! 123\nTest"},
                    "output": "14\n3\n2\n2"
                },
                {
                    "input": "",
                    "files": {"input.txt": "abc123@#$"},
                    "output": "3\n3\n0\n3"
                },
                {
                    "input": "",
                    "files": {"input.txt": "A B 9"},
                    "output": "2\n1\n2\n0"
                },
            ],
        },
    ]

    # 前10题归2024年，后10题归2023年
    for i, p in enumerate(problems):
        p["category"] = "2025年" if i < 10 else "2024年"
        db.add(Problem(**p))

    db.commit()
    db.close()
    print(f"成功初始化 {len(problems)} 道题目！")


if __name__ == "__main__":
    seed()
