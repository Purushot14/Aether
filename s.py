"""
File: s
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"
import os
# 2. Create .github/workflows/ci.yml
os.makedirs(".github/workflows", exist_ok=True)

ci_workflow = """
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Poetry
        run: |
          pip install poetry

      - name: Install Dependencies
        run: |
          cd aether
          poetry install

      - name: Run Tests
        run: |
          cd aether
          poetry run pytest tests
"""

with open(".github/workflows/ci.yml", "w") as f:
    f.write(ci_workflow.strip())

if __name__ == "__main__":
    import os
    import sys

    # Check if the script is run directly
    # if len(sys.argv) > 1 and sys.argv[1] == "create":
    #     # Create the folders and files
    #     pass  # The code above will run here
    # else:
    print("Run this script with 'create' argument to set up the scaffolding.")