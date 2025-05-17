"""
File: data_collector.py
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"


import boto3
from google.cloud import monitoring_v3
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
import datetime

# Time range (last 24 hours)
end_time = datetime.datetime.utcnow()
start_time = end_time - datetime.timedelta(days=1)

# ---------------- AWS CloudWatch Example ----------------
def fetch_aws_cpu_usage(instance_id, region='us-east-1'):
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Average']
    )
    return response['Datapoints']

# ---------------- GCP Stackdriver Example ----------------
def fetch_gcp_cpu_usage(instance_id, project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": int(end_time.timestamp())},
         "start_time": {"seconds": int(start_time.timestamp())}}
    )
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type="compute.googleapis.com/instance/cpu/utilization" AND '
                      f'resource.label.instance_id="{instance_id}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        }
    )
    return [point.point for ts in results for point in ts.points]

# ---------------- Azure Monitor Example ----------------
def fetch_azure_cpu_usage(subscription_id, resource_group, vm_name, location="eastus"):
    credential = DefaultAzureCredential()
    monitor_client = MonitorManagementClient(credential, subscription_id)
    metrics = monitor_client.metrics.list(
        resource_uri=f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}",
        timespan=f"{start_time}/{end_time}",
        interval='PT1H',
        metricnames='Percentage CPU',
        aggregation='Average'
    )
    return [metric.timeseries for metric in metrics.value]

# Example usage (placeholders below should be replaced with real IDs)
if __name__ == "__main__":
    print("Fetching AWS metrics...")
    aws_data = fetch_aws_cpu_usage(instance_id="i-0123456789abcdef0")
    print(aws_data)

    print("Fetching GCP metrics...")
    gcp_data = fetch_gcp_cpu_usage(instance_id="1234567890123456789", project_id="your-gcp-project")
    print(gcp_data)

    print("Fetching Azure metrics...")
    azure_data = fetch_azure_cpu_usage(subscription_id="your-subscription-id", resource_group="your-rg", vm_name="your-vm")
    print(azure_data)
