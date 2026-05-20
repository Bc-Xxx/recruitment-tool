import csv
import io
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.database import (
    init_db, insert_jobs, count_jobs,
    search_jobs, get_locations, get_stats,
    get_city_distribution, get_company_distribution,
)
from scraper.crawler import generate_jobs

app = FastAPI()

FRONTEND_HTML = (Path(__file__).parent.parent / "frontend" / "index.html").read_text(encoding="utf-8")


@app.on_event("startup")
def startup():
    init_db()
    if count_jobs() == 0:
        jobs = generate_jobs(50)
        insert_jobs(jobs)
        print(f"已填充 {len(jobs)} 条模拟岗位数据")


@app.get("/", response_class=HTMLResponse)
def index():
    return FRONTEND_HTML


@app.get("/api/jobs")
def list_jobs(
    keyword: str = Query(default=""),
    location: str = Query(default=""),
    sort_by: str = Query(default="", description="salary_desc 或 salary_asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
):
    all_jobs = search_jobs(keyword=keyword, location=location, sort_by=sort_by)
    total = len(all_jobs)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
        "jobs": all_jobs[start:end],
    }


@app.get("/api/locations")
def list_locations():
    return {"locations": get_locations()}


@app.get("/api/stats")
def job_stats():
    return get_stats()


@app.get("/api/charts")
def chart_data():
    """返回图表所需数据"""
    return {
        "city_distribution": get_city_distribution(),
        "company_distribution": get_company_distribution(),
    }


@app.get("/api/jobs/export")
def export_csv(
    keyword: str = Query(default=""),
    location: str = Query(default=""),
):
    """导出搜索结果到 CSV 文件"""
    jobs = search_jobs(keyword=keyword, location=location)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["岗位名称", "公司", "城市", "薪资", "技能要求"])
    for job in jobs:
        writer.writerow([job.title, job.company, job.location, job.salary, job.tags])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": "attachment; filename=jobs.csv"},
    )
