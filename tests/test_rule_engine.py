"""
File: test_rule_engine.py
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

import pytest
from rules.rule_engine import evaluate_rules

def test_rule_engine():
    test_data = [
        {
            'resource_id': 'pod-a',
            'cpu_utilization': 0.3,
            'memory_utilization': 0.4,
            'days_tracked': 10
        },
        {
            'resource_id': 'pod-b',
            'cpu_utilization': 0.95,
            'memory_utilization': 0.96,
            'days_tracked': 6
        },
        {
            'resource_id': 'pod-c',
            'cpu_utilization': 0.7,
            'memory_utilization': 0.48,
            'days_tracked': 8
        }
    ]

    results = evaluate_rules(test_data)
    resource_recs = {r['resource_id']: r['recommendation'] for r in results}

    assert resource_recs['pod-a'] == 'scale_down_cpu' or resource_recs['pod-a'] == 'scale_down_memory'
    assert resource_recs['pod-b'] == 'scale_up'
    assert isinstance(results, list)
    assert all('resource_id' in r and 'recommendation' in r for r in results)