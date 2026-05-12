# 算法可视化演示系统

北京邮电大学场景下的动态规划与贪心算法可视化演示系统。

## 项目简介

本项目实现了两种经典算法在北邮实际场景中的应用：
- **动态规划算法**：解决学生选课优化问题（带时间约束的0-1背包问题）
- **贪心算法**：解决教室资源分配问题（区间调度问题）

## 项目结构

```
class_work_02/
├── algorithms/              # 算法实现
│   ├── dynamic_programming.py   # 动态规划算法
│   ├── greedy.py               # 贪心算法
│   └── comparison.py           # 算法对比分析
├── data/                    # 数据文件
│   ├── courses.json            # 课程数据（40门）
│   ├── activities.json         # 活动数据（80个）
│   ├── classrooms.json         # 教室数据（201个）
│   ├── test_cases.json         # 测试用例
│   ├── comparison_report.json  # 对比报告
│   ├── time_complexity.png     # 时间复杂度图表
│   └── generate_data.py        # 数据生成脚本
├── tests/                   # 单元测试
│   └── test_algorithms.py      # 算法测试（13个测试用例）
├── web/                     # Web应用
│   ├── app.py                  # Flask后端
│   ├── templates/              # HTML模板
│   │   ├── index.html
│   │   ├── dynamic_programming.html
│   │   ├── greedy.html
│   │   └── comparison.html
│   └── static/                 # 静态资源
│       └── css/
│           └── style.css
├── requirements.txt         # Python依赖
├── conversation_log.md      # 对话记录
└── phase1_analysis.md       # 第一阶段分析
```

## 环境配置

### 1. 创建虚拟环境

```bash
cd /Users/qiu_star/code_project/class_work
python3 -m venv class_work_02
```

### 2. 激活虚拟环境

```bash
source class_work_02/bin/activate
```

### 3. 安装依赖

```bash
cd class_work_02
pip install -r requirements.txt
```

## 运行方式

### 1. 运行单元测试

```bash
cd tests
python test_algorithms.py
```

### 2. 运行算法对比分析

```bash
cd algorithms
python comparison.py
```

### 3. 启动Web应用

```bash
cd web
python app.py
```

然后在浏览器中访问：
- 首页: http://127.0.0.1:5000/
- 动态规划: http://127.0.0.1:5000/dynamic-programming
- 贪心算法: http://127.0.0.1:5000/greedy
- 算法对比: http://127.0.0.1:5000/comparison

## 功能特性

### 动态规划算法
- 课程选择优化，最大化学分
- 自动检测时间冲突
- 支持最低学分约束
- 生成可视化课程表
- 详细的执行日志

### 贪心算法
- 教室资源分配，最大化活动数量
- 按结束时间贪心策略
- 支持优先级权重
- 教室利用率统计
- 活动时间线可视化

### 算法对比
- 时间复杂度对比图表
- 空间复杂度分析
- 优缺点详细对比
- 适用场景建议
- 性能测试数据

## 数据集说明

- **课程数据**：40门北邮真实课程，包含课程名、学分、教师、时间段、教室等信息
- **活动数据**：80个活动，涵盖专业课、讲座、社团活动、考试等8种类型
- **教室数据**：201个教室，分布在教三、教四、科研楼、学活等建筑

## 算法性能

### 动态规划
- 时间复杂度：O(n × 2^m)
- 空间复杂度：O(n × 2^m)
- 适用规模：n < 30
- 保证全局最优

### 贪心算法
- 时间复杂度：O(n log n)
- 空间复杂度：O(n + m)
- 适用规模：n > 1000
- 保证全局最优（区间调度问题）

## 测试结果

单元测试：13/13 全部通过 ✓

## 技术栈

- **后端**：Python 3.9, Flask 3.1
- **前端**：HTML5, CSS3, JavaScript (Vanilla)
- **数据处理**：JSON
- **可视化**：Matplotlib
- **测试**：unittest

## 作者

邱秀豪 - 北京邮电大学

## 许可证

本项目仅用于课程作业学习目的。
