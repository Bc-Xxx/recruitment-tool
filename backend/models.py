from pydantic import BaseModel


class Job(BaseModel):
    """一条招聘信息的数据结构"""
    id: int | None = None
    title: str
    company: str
    location: str
    salary: str
    tags: str
