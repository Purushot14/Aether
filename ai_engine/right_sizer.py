"""
File: right_sizer
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class RightSizer:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination)

    def prepare_features(self, df):
        """
        Expects a DataFrame with columns: ['cpu_usage_millicores', 'memory_usage_mebibytes']
        Returns scaled numerical features.
        """
        df_clean = df.copy()
        df_clean = df_clean.dropna()
        features = df_clean[['cpu_usage_millicores', 'memory_usage_mebibytes']]
        return features

    def fit(self, df):
        X = self.prepare_features(df)
        self.model.fit(X)
        return self

    def predict(self, df):
        X = self.prepare_features(df)
        preds = self.model.predict(X)
        df_result = df.copy()
        df_result['anomaly'] = preds
        df_result['score'] = self.model.decision_function(X)
        return df_result

    def recommend_resources(self, df, safety_margin=1.25):
        """
        Returns resource recommendations for pods, ignoring outliers.
        """
        clean_df = self.predict(df)
        normal_data = clean_df[clean_df['anomaly'] == 1]  # 1 = normal

        cpu_mean = normal_data['cpu_usage_millicores'].mean()
        mem_mean = normal_data['memory_usage_mebibytes'].mean()

        recommendation = {
            'recommended_cpu_millicores': int(cpu_mean * safety_margin),
            'recommended_memory_mebibytes': int(mem_mean * safety_margin),
            'confidence': round((1 - clean_df['anomaly'].value_counts(normalize=True).get(-1, 0)), 2)
        }
        return recommendation

# Example usage:
if __name__ == "__main__":
    # Simulated input data
    data = {
        'cpu_usage_millicores': [200, 210, 190, 205, 500, 215, 180],
        'memory_usage_mebibytes': [100, 110, 105, 115, 400, 120, 95]
    }
    df = pd.DataFrame(data)

    model = RightSizer()
    model.fit(df)
    result = model.recommend_resources(df)
    print("Right-Sizing Recommendation:", result)