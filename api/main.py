"""
File: main
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from ai_engine.right_sizer import RightSizer
from rules.rule_engine import evaluate_rules

app = FastAPI(title="Aether API", version="0.1.0")

class ResourceInput(BaseModel):
    resource_id: str
    cpu_utilization: float
    memory_utilization: float
    days_tracked: int

@app.get("/")
def root():
    return {"message": "Aether - Cost Optimization API is running"}

@app.post("/recommend/ai")
def recommend_ai(data: List[ResourceInput]):
    df = pd.DataFrame([d.dict() for d in data])
    df['cpu_usage_millicores'] = df['cpu_utilization'] * 1000
    df['memory_usage_mebibytes'] = df['memory_utilization'] * 2048
    model = RightSizer()
    model.fit(df)
    return model.recommend_resources(df)

@app.post("/recommend/rules")
def recommend_rules(data: List[ResourceInput]):
    resource_data = [d.dict() for d in data]
    return evaluate_rules(resource_data)
