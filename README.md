[README.md](https://github.com/user-attachments/files/29320593/README.md)
# Twitch 主播大数据可视化

## 项目简介

本项目是《大数据可视化》期末大作业，选择**高阶档**难度，基于 Twitch 平台前 1000 名主播数据，使用 **Python (FastAPI + Pandas)** 进行数据处理与后端服务，**ECharts 5** 进行前端可视化展示。

## 技术栈

| 环节 | 技术 |
|------|------|
| 数据处理 | Python 3.13 + Pandas + NumPy |
| 后端服务 | FastAPI + Uvicorn |
| 前端可视化 | ECharts 5 (echarts.min.js) + 原生 HTML/CSS/JavaScript |
| 数据源 | twitchdata-update.csv |

## 功能概览

### 基础图表（基础档全部要求）
1. **柱状图** — 观看时长 TOP20 主播
2. **环形饼图** — 各语言主播数量分布
3. **散点图** — 直播时长 vs 平均观众（颜色区分签约/未签约）
4. **横向条形图** — 各语言平均在线观众

### 高阶附加（高阶档专有）
- **相关性热力图** — 5 个数值指标的皮尔逊相关系数矩阵
- **KPI 指标卡片** — 总主播数、总直播/观看时长、平均观众、签约占比
- **点击联动** — 点击柱状图主播名 → 散点图自动过滤该主播
- **语言筛选** — 下拉菜单按语言动态过滤散点图
- **数据分析洞察模块** — 内嵌 4 条核心数据洞察

## 目录结构

```
big/
├── main.py                 # FastAPI 后端服务
├── data_process.py         # 数据处理与统计函数
├── static/
│   ├── index.html          # 前端仪表板页面
│   └── echarts.min.js      # ECharts 5 库文件
├── data/
│   └── twitchdata-update.csv  # 原始数据集
├── README.md               # 本文件
└── 报告文档.md              # 数据分析报告
```

## 运行说明

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
pip install fastapi uvicorn pandas numpy
```

> 注：项目使用 FastAPI + Starlette（FastAPI 自带），无需额外安装 requirements.txt。

### 启动服务

在项目根目录 `big/` 下执行：

```bash
python main.py
```

或使用 uvicorn 命令：

```bash
uvicorn main:app --host localhost --port 8000 --reload
```

### 访问页面

打开浏览器，访问：**http://localhost:8000**

- 主页 `/` → 仪表板页面
- API 接口列表：
  - `/api/stats` — 全局统计数据
  - `/api/top20` — TOP20 主播
  - `/api/lang_count` — 各语言主播数量
  - `/api/scatter?lang=all&channel=` — 散点图数据（支持语言和主播筛选）
  - `/api/lang_avg_view` — 各语言平均观众
  - `/api/correlation` — 相关性矩阵

## 难易档选择说明

本项目选择**高阶档（满分 100 分）**，在完成基础档全部 4 个图表的基础上，额外实现了：

| 附加任务 | 内容 | 完成情况 |
|----------|------|----------|
| 附加任务A | 相关性分析（热力图）+ 语言对比分析 | 热力图已实现 |
| 附加任务B | 高级交互（点击联动 + 语言筛选） | 两项均已实现 |
| 附加任务C | 数据分析报告 | 见报告文档 |

## 数据预处理说明

1. 使用 Pandas 加载 CSV，过滤 `Stream time = 0` 的异常数据
2. 派生字段 `watch_efficiency = Watch time / Stream time`
3. 按语言分组统计主播数量、平均观众等
4. 所有 numpy 类型统一转换为 Python 原生类型以保证 JSON 序列化

## 注意事项

- 确保 `data/twitchdata-update.csv` 文件存在于 `data/` 目录下
- 端口 8000 不可被其他程序占用
- 浏览器需支持 ES6+（Fetch API、async/await）
