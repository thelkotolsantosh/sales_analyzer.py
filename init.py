"""
BI Analyst - Business Intelligence Analysis Tool

A Python package for sales data analysis and business intelligence.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .sales_analyzer import SalesAnalyzer, generate_sample_data
from .dashboard import DashboardGenerator

__all__ = [
    'SalesAnalyzer',
    'generate_sample_data',
    'DashboardGenerator',
]
