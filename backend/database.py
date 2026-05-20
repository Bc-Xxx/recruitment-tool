import re
import sqlite3
import os

from backend.models import Job

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "jobs.db")


def parse_salary(salary: str) -> float:
    """把薪资字符串转成数值，用于排序。「面议」返回 -1 排在最后"""
    match = re.search(r"(\d+)-(\d+)K?", salary)
    if match:
        low = float(match.group(1))
        high = float(match.group(2))
        return (low + high) / 2
    return -1


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            salary TEXT NOT NULL,
            tags TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_jobs(jobs: list[dict]):
    conn = get_connection()
    for job in jobs:
        conn.execute(
            "INSERT INTO jobs (title, company, location, salary, tags) "
            "VALUES (?, ?, ?, ?, ?)",
            (job["title"], job["company"], job["location"], job["salary"], job["tags"]),
        )
    conn.commit()
    conn.close()


def count_jobs() -> int:
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as cnt FROM jobs").fetchone()
    conn.close()
    return row["cnt"]


def search_jobs(
    keyword: str = "",
    location: str = "",
    sort_by: str = "",
    limit: int = 999,
) -> list[Job]:
    conn = get_connection()
    sql = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if keyword:
        sql += " AND (title LIKE ? OR tags LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if location:
        sql += " AND location = ?"
        params.append(location)

    sql += " LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    jobs = [Job(**dict(row)) for row in rows]

    # 排序在 Python 里做（薪资在数据库里是文本，没法直接排）
    if sort_by == "salary_desc":
        jobs.sort(key=lambda j: parse_salary(j.salary), reverse=True)
    elif sort_by == "salary_asc":
        jobs.sort(key=lambda j: parse_salary(j.salary))

    return jobs


def get_locations() -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT location FROM jobs ORDER BY location"
    ).fetchall()
    conn.close()
    return [row["location"] for row in rows]


def get_city_distribution() -> list[dict]:
    """每个城市的岗位数量（给图表用）"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT location as name, COUNT(*) as value FROM jobs "
        "GROUP BY location ORDER BY value DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_company_distribution() -> list[dict]:
    """每个公司的岗位数量（给图表用）"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT company as name, COUNT(*) as value FROM jobs "
        "GROUP BY company ORDER BY value DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats() -> dict:
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) as cnt FROM jobs").fetchone()["cnt"]

    top_cities = [
        dict(row)
        for row in conn.execute(
            "SELECT location, COUNT(*) as count FROM jobs "
            "GROUP BY location ORDER BY count DESC LIMIT 5"
        ).fetchall()
    ]

    top_companies = [
        dict(row)
        for row in conn.execute(
            "SELECT company, COUNT(*) as count FROM jobs "
            "GROUP BY company ORDER BY count DESC LIMIT 5"
        ).fetchall()
    ]

    conn.close()
    return {
        "total": total,
        "top_cities": top_cities,
        "top_companies": top_companies,
    }
