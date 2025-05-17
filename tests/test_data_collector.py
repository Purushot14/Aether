"""
File: test_data_collector.py
Author: prakash
Created: 17/05/25.
"""

__author__ = "prakash"
__date__ = "17/05/25"

import pytest
from unittest.mock import patch, MagicMock
import datetime
from data_pipeline.data_collector import (
    fetch_aws_cpu_usage,
    fetch_gcp_cpu_usage,
    fetch_azure_cpu_usage
)

# Mock datetime for consistent test results
@pytest.fixture
def mock_datetime():
    with patch('data_pipeline.data_collector.datetime') as mock_dt:
        mock_dt.datetime.utcnow.return_value = datetime.datetime(2023, 5, 17, 12, 0, 0)
        mock_dt.timedelta = datetime.timedelta
        yield mock_dt

# Test AWS CloudWatch data collection
@patch('data_pipeline.data_collector.boto3')
def test_fetch_aws_cpu_usage(mock_boto3, mock_datetime):
    # Setup mock response
    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    mock_response = {
        'Datapoints': [
            {'Timestamp': datetime.datetime(2023, 5, 17, 10, 0), 'Average': 45.5},
            {'Timestamp': datetime.datetime(2023, 5, 17, 11, 0), 'Average': 53.2}
        ]
    }
    mock_client.get_metric_statistics.return_value = mock_response

    # Call the function
    result = fetch_aws_cpu_usage('i-0123456789abcdef0')

    # Assertions
    assert result == mock_response['Datapoints']
    mock_boto3.client.assert_called_once_with('cloudwatch', region_name='us-east-1')
    mock_client.get_metric_statistics.assert_called_once()

# Test GCP Stackdriver data collection
@patch('data_pipeline.data_collector.monitoring_v3')
def test_fetch_gcp_cpu_usage(mock_monitoring, mock_datetime):
    # Setup mock response
    mock_client = MagicMock()
    mock_monitoring.MetricServiceClient.return_value = mock_client

    mock_ts = MagicMock()
    mock_point = MagicMock()
    mock_ts.points = [mock_point]
    mock_client.list_time_series.return_value = [mock_ts]

    # Call the function
    result = fetch_gcp_cpu_usage('1234567890123456789', 'test-project')

    # Assertions
    assert result == [mock_point.point]
    mock_monitoring.MetricServiceClient.assert_called_once()
    mock_client.list_time_series.assert_called_once()

# Test Azure Monitor data collection
@patch('data_pipeline.data_collector.MonitorManagementClient')
@patch('data_pipeline.data_collector.DefaultAzureCredential')
def test_fetch_azure_cpu_usage(mock_credential, mock_monitor_client, mock_datetime):
    # Setup mock response
    mock_cred_instance = MagicMock()
    mock_credential.return_value = mock_cred_instance

    mock_client = MagicMock()
    mock_monitor_client.return_value = mock_client

    mock_metric = MagicMock()
    mock_metric.timeseries = ['data_point1', 'data_point2']
    mock_client.metrics.list.return_value.value = [mock_metric]

    # Call the function
    result = fetch_azure_cpu_usage('sub-123', 'rg-test', 'vm-test')

    # Assertions
    assert result == [mock_metric.timeseries]
    mock_credential.assert_called_once()
    mock_monitor_client.assert_called_once_with(mock_cred_instance, 'sub-123')
    mock_client.metrics.list.assert_called_once()