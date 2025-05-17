"""
File: s
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

rule_code = """
from durable.lang import *

with ruleset('resource_optimization'):

    # Rule for overprovisioned CPU
    @when_all((m.cpu_utilization < 0.4) & (m.days_tracked >= 7))
    def scale_down_cpu(c):
        print(f"[RULE] CPU underutilized for {c.m.resource_id}: Recommend scaling down.")
        c.assert_fact({
            'resource_id': c.m.resource_id,
            'recommendation': 'scale_down_cpu',
            'reason': 'CPU usage below 40% for 7+ days'
        })

    # Rule for overprovisioned Memory
    @when_all((m.memory_utilization < 0.5) & (m.days_tracked >= 7))
    def scale_down_memory(c):
        print(f"[RULE] Memory underutilized for {c.m.resource_id}: Recommend scaling down.")
        c.assert_fact({
            'resource_id': c.m.resource_id,
            'recommendation': 'scale_down_memory',
            'reason': 'Memory usage below 50% for 7+ days'
        })

    # Rule for consistently high usage (potential scale up)
    @when_all((m.cpu_utilization > 0.9) & (m.memory_utilization > 0.9) & (m.days_tracked >= 5))
    def scale_up(c):
        print(f"[RULE] High resource usage for {c.m.resource_id}: Recommend scaling up.")
        c.assert_fact({
            'resource_id': c.m.resource_id,
            'recommendation': 'scale_up',
            'reason': 'CPU & Memory consistently high for 5+ days'
        })

# Example usage
if __name__ == '__main__':
    from durable.engine import post

    test_data = [
        {
            'resource_id': 'analytics-pod',
            'cpu_utilization': 0.32,
            'memory_utilization': 0.45,
            'days_tracked': 10
        },
        {
            'resource_id': 'ml-model-pod',
            'cpu_utilization': 0.95,
            'memory_utilization': 0.96,
            'days_tracked': 6
        },
        {
            'resource_id': 'frontend-pod',
            'cpu_utilization': 0.70,
            'memory_utilization': 0.48,
            'days_tracked': 8
        }
    ]

    for data in test_data:
        post('resource_optimization', data)
"""

with open("rules/rule_engine.py", "w") as f:
    f.write(rule_code.strip())

if __name__ == "__main__":
    import os
    import sys

    # Check if the script is run directly
    # if len(sys.argv) > 1 and sys.argv[1] == "create":
    #     # Create the folders and files
    #     pass  # The code above will run here
    # else:
    print("Run this script with 'create' argument to set up the scaffolding.")