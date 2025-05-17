"""
File: test_ai_engine
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

import pytest
import pandas as pd
from ai_engine.right_sizer import RightSizer

def test_ai_recommendation():
    data = {
        'cpu_usage_millicores': [100, 120, 110, 115, 500],
        'memory_usage_mebibytes': [100, 105, 110, 108, 400]
    }
    df = pd.DataFrame(data)
    model = RightSizer()
    model.fit(df)
    rec = model.recommend_resources(df)
    assert 'recommended_cpu_millicores' in rec
    assert 'recommended_memory_mebibytes' in rec
    assert rec['confidence'] >= 0.0 and rec['confidence'] <= 1.0