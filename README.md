# 招聘信息聚合与分析工具

基于 FastAPI + SQLite 的招聘信息聚合平台，支持岗位搜索、筛选、排序、图表可视化与 CSV 导出。



## 技术栈

| 层 | 技术 |
|----|------|
| 爬虫 | requests + BeautifulSoup |
| 后端 | FastAPI + SQLite |
| 前端 | HTML + JavaScript + ECharts |

## 快速启动

```bash
# 1. 创建虚拟环境并安装依赖
python -m venv venv
venv\Scripts\pip.exe install -r requirements.txt

# 2. 启动服务
venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# 3. 浏览器访问
# http://127.0.0.1:8000
```

## 功能

- 岗位搜索（按关键词、城市筛选）
- 分页浏览
- 薪资排序（从高到低 / 从低到高）
- 城市分布柱状图 + 公司分布饼图（ECharts）
- 搜索结果导出 CSV
- 启动时自动初始化数据库并填充模拟数据

## 项目结构

```
├── scraper/           # 爬虫模块
│   └── crawler.py     # 数据生成器（可替换为真实爬虫）
├── backend/           # 后端
│   ├── main.py        # FastAPI 入口 + API 路由
│   ├── database.py    # SQLite 数据库操作
│   └── models.py      # 数据模型
├── frontend/          # 前端
│   └── index.html     # 单页应用
├── data/              # 数据库文件（启动时自动生成）
├── requirements.txt   # 依赖列表
└── README.md
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 前端页面 |
| GET | `/api/jobs` | 搜索岗位（支持 keyword, location, sort_by, page, page_size） |
| GET | `/api/locations` | 城市列表 |
| GET | `/api/stats` | 统计摘要 |
| GET | `/api/charts` | 图表数据 |
| GET | `/api/jobs/export` | 导出 CSV |

## 关于爬虫

`scraper/crawler.py` 当前使用模拟数据。实测主流招聘网站（51job、拉勾、Boss直聘）存在阿里云 WAF 防护、字体反爬等机制。模块输出统一格式的 dict 列表，替换为真实爬虫时不影响后端与前端代码。
