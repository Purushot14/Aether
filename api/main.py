"""
File: main
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

# FastAPI entrypoint

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to Aether - Cost Optimization API"}
