"""
模拟招聘数据生成器（原计划爬取真实网站，目标网站有反爬，改用模拟数据）
"""
import random


COMPANIES = [
    "字节跳动", "腾讯", "阿里巴巴", "美团", "京东",
    "华为", "小米", "网易", "哔哩哔哩", "滴滴",
    "用友软件", "金蝶", "神州数码", "中软国际", "软通动力",
    "文思海辉", "博彦科技", "浪潮", "东软", "亚信",
]

LOCATIONS = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "东莞", "西安"]

SALARIES = [
    "3-5K", "4-6K", "5-8K", "6-10K", "8-12K",
    "10-15K", "15-20K", "20-30K", "面议",
]

PYTHON_TITLES = [
    "Python开发工程师", "Python后端开发", "Python实习生",
    "Python爬虫工程师", "Python数据分析", "Python自动化测试",
    "后端开发工程师（Python）", "Python运维开发", "Python全栈开发",
    "Python开发（实习）", "Python助理工程师",
]

SKILL_TAGS = [
    "Python", "Django", "Flask", "FastAPI", "MySQL",
    "Redis", "Docker", "Git", "Linux", "MongoDB",
    "PostgreSQL", "Celery", "RabbitMQ", "Nginx", "AWS",
    "JavaScript", "HTML", "CSS", "Vue", "React",
]


def generate_jobs(count=50):
    """生成模拟岗位数据"""
    jobs = []
    for _ in range(count):
        title = random.choice(PYTHON_TITLES)
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        salary = random.choice(SALARIES)

        # 随机选 3-6 个技能标签
        tags = random.sample(SKILL_TAGS, random.randint(3, 6))

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "tags": ", ".join(tags),
        })

    return jobs


if __name__ == "__main__":
    jobs = generate_jobs(50)
    print(f"生成了 {len(jobs)} 条模拟岗位数据")
    for job in jobs[:5]:
        print(f"  {job['title']} | {job['company']} | {job['salary']} | {job['location']} | 技能: {job['tags']}")
