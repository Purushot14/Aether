"""
File: rule_engine
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

def evaluate_rules(resource_data):
    recommendations = []

    for entry in resource_data:
        resource_id = entry['resource_id']
        cpu_util = entry['cpu_utilization']
        mem_util = entry['memory_utilization']
        days = entry['days_tracked']

        if cpu_util < 0.4 and days >= 7:
            recommendations.append({
                'resource_id': resource_id,
                'recommendation': 'scale_down_cpu',
                'reason': 'CPU usage below 40% for 7+ days'
            })

        if mem_util < 0.5 and days >= 7:
            recommendations.append({
                'resource_id': resource_id,
                'recommendation': 'scale_down_memory',
                'reason': 'Memory usage below 50% for 7+ days'
            })

        if cpu_util > 0.9 and mem_util > 0.9 and days >= 5:
            recommendations.append({
                'resource_id': resource_id,
                'recommendation': 'scale_up',
                'reason': 'CPU & Memory consistently high for 5+ days'
            })

    return recommendations


# Example usage
if __name__ == '__main__':
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

    results = evaluate_rules(test_data)
    for r in results:
        print(f"[RECOMMENDATION] {r['resource_id']}: {r['recommendation']} — {r['reason']}")

