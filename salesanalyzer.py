"""
Sales Analytics Module for Business Intelligence

This module provides comprehensive sales analysis capabilities including:
- Revenue analysis and trending
- Customer segmentation
- Product performance metrics
- Regional sales analysis
- KPI calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class SalesAnalyzer:
    """
    Business Intelligence tool for sales data analysis.
    
    Provides methods for analyzing sales performance, customer behavior,
    and generating business insights.
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the Sales Analyzer.
        
        Args:
            dataframe (pd.DataFrame): Sales data with columns:
                - order_id: Unique order identifier
                - customer_id: Customer identifier
                - order_date: Date of order
                - amount: Sale amount
                - region: Geographic region
                - product_category: Product category
                - quantity: Items sold
        """
        self.df = dataframe.copy()
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self._validate_data()
    
    def _validate_data(self):
        """Validate that required columns exist."""
        required_cols = [
            'order_id', 'customer_id', 'order_date', 'amount',
            'region', 'product_category', 'quantity'
        ]
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def get_revenue_summary(self) -> Dict:
        """
        Get overall revenue summary statistics.
        
        Returns:
            dict: Contains total revenue, average order value, transaction count
        """
        return {
            'total_revenue': self.df['amount'].sum(),
            'avg_order_value': self.df['amount'].mean(),
            'median_order_value': self.df['amount'].median(),
            'min_order_value': self.df['amount'].min(),
            'max_order_value': self.df['amount'].max(),
            'total_transactions': len(self.df),
            'total_units_sold': self.df['quantity'].sum(),
        }
    
    def get_regional_analysis(self) -> pd.DataFrame:
        """
        Analyze sales performance by region.
        
        Returns:
            pd.DataFrame: Regional sales metrics including revenue, count, avg order
        """
        regional = self.df.groupby('region').agg({
            'amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        regional.columns = ['Revenue', 'Avg_Order_Value', 'Transactions', 
                           'Units_Sold', 'Unique_Customers']
        regional = regional.sort_values('Revenue', ascending=False)
        
        return regional
    
    def get_product_performance(self) -> pd.DataFrame:
        """
        Analyze product category performance.
        
        Returns:
            pd.DataFrame: Product metrics including revenue, quantity, margins
        """
        products = self.df.groupby('product_category').agg({
            'amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        products.columns = ['Revenue', 'Avg_Price', 'Transactions',
                           'Quantity_Sold', 'Unique_Customers']
        products = products.sort_values('Revenue', ascending=False)
        
        return products
    
    def get_monthly_trends(self) -> pd.DataFrame:
        """
        Get monthly revenue and transaction trends.
        
        Returns:
            pd.DataFrame: Monthly metrics with revenue, transactions, growth
        """
        self.df['year_month'] = self.df['order_date'].dt.to_period('M')
        
        monthly = self.df.groupby('year_month').agg({
            'amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).round(2)
        
        monthly.columns = ['Revenue', 'Avg_Order_Value', 'Transactions', 'Units']
        monthly['MoM_Growth_%'] = monthly['Revenue'].pct_change() * 100
        monthly = monthly.round(2)
        
        return monthly
    
    def get_customer_segmentation(self) -> pd.DataFrame:
        """
        Segment customers based on purchase behavior.
        
        Returns:
            pd.DataFrame: Customer segments with metrics
        """
        customer_stats = self.df.groupby('customer_id').agg({
            'amount': ['sum', 'count', 'mean'],
            'order_date': ['min', 'max'],
            'quantity': 'sum'
        }).reset_index()
        
        customer_stats.columns = [
            'customer_id', 'lifetime_value', 'purchase_count', 
            'avg_purchase', 'first_purchase', 'last_purchase', 'total_units'
        ]
        
        # Calculate recency, frequency, monetary (RFM)
        reference_date = self.df['order_date'].max()
        customer_stats['recency_days'] = (
            reference_date - customer_stats['last_purchase']
        ).dt.days
        
        # Segment based on LTV
        def segment(ltv):
            if ltv > customer_stats['lifetime_value'].quantile(0.75):
                return 'VIP'
            elif ltv > customer_stats['lifetime_value'].quantile(0.50):
                return 'Premium'
            elif ltv > customer_stats['lifetime_value'].quantile(0.25):
                return 'Standard'
            else:
                return 'New'
        
        customer_stats['segment'] = customer_stats['lifetime_value'].apply(segment)
        
        return customer_stats.sort_values('lifetime_value', ascending=False)
    
    def get_key_metrics(self) -> Dict:
        """
        Calculate key business metrics.
        
        Returns:
            dict: KPIs including growth rates, margins, and efficiency metrics
        """
        monthly_data = self.get_monthly_trends()
        
        return {
            'YTD_Revenue': monthly_data['Revenue'].sum(),
            'Avg_Monthly_Revenue': monthly_data['Revenue'].mean(),
            'Growth_Rate_%': monthly_data['MoM_Growth_%'].mean(),
            'Customer_Count': self.df['customer_id'].nunique(),
            'Revenue_Per_Customer': self.df['amount'].sum() / self.df['customer_id'].nunique(),
            'Repeat_Customer_Rate_%': (
                (self.df.groupby('customer_id').size() > 1).sum() / 
                self.df['customer_id'].nunique() * 100
            ),
        }
    
    def get_top_customers(self, n: int = 10) -> pd.DataFrame:
        """
        Get top N customers by revenue.
        
        Args:
            n (int): Number of top customers to return
            
        Returns:
            pd.DataFrame: Top customers with their metrics
        """
        top = self.df.groupby('customer_id').agg({
            'amount': ['sum', 'count', 'mean'],
            'quantity': 'sum'
        }).reset_index()
        
        top.columns = ['customer_id', 'total_spent', 'purchase_count',
                      'avg_purchase', 'total_units']
        
        return top.nlargest(n, 'total_spent')
    
    def get_cohort_analysis(self) -> pd.DataFrame:
        """
        Perform cohort analysis based on first purchase month.
        
        Returns:
            pd.DataFrame: Cohort retention matrix
        """
        customer_cohort = self.df.copy()
        customer_cohort['cohort_month'] = customer_cohort.groupby(
            'customer_id'
        )['order_date'].transform('min').dt.to_period('M')
        
        customer_cohort['order_month'] = customer_cohort['order_date'].dt.to_period('M')
        
        cohorts = customer_cohort.groupby('cohort_month').agg({
            'customer_id': 'nunique'
        }).round(0)
        
        return cohorts
    
    def get_sales_forecast_indicators(self) -> Dict:
        """
        Generate indicators for sales forecasting.
        
        Returns:
            dict: Trend indicators and seasonal patterns
        """
        monthly = self.get_monthly_trends()
        
        return {
            'latest_month_revenue': monthly['Revenue'].iloc[-1],
            'previous_month_revenue': monthly['Revenue'].iloc[-2] if len(monthly) > 1 else 0,
            'avg_monthly': monthly['Revenue'].mean(),
            'std_dev': monthly['Revenue'].std(),
            'trend_direction': 'UP' if monthly['Revenue'].iloc[-1] > monthly['Revenue'].mean() else 'DOWN',
            'volatility': monthly['Revenue'].std() / monthly['Revenue'].mean(),
        }
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive text report.
        
        Returns:
            str: Formatted analysis report
        """
        revenue = self.get_revenue_summary()
        regional = self.get_regional_analysis()
        products = self.get_product_performance()
        kpis = self.get_key_metrics()
        
        report = f"""
{'='*70}
                    SALES ANALYTICS REPORT
                    {datetime.now().strftime('%Y-%m-%d')}
{'='*70}

REVENUE SUMMARY
{'-'*70}
Total Revenue:              ${revenue['total_revenue']:,.2f}
Average Order Value:        ${revenue['avg_order_value']:,.2f}
Total Transactions:         {revenue['total_transactions']:,}
Total Units Sold:           {revenue['total_units_sold']:,}

KEY PERFORMANCE INDICATORS
{'-'*70}
YTD Revenue:                ${kpis['YTD_Revenue']:,.2f}
Avg Monthly Revenue:        ${kpis['Avg_Monthly_Revenue']:,.2f}
Growth Rate (MoM):          {kpis['Growth_Rate_%']:.2f}%
Total Customers:            {kpis['Customer_Count']:,}
Revenue Per Customer:       ${kpis['Revenue_Per_Customer']:,.2f}
Repeat Customer Rate:       {kpis['Repeat_Customer_Rate_%']:.2f}%

REGIONAL PERFORMANCE
{'-'*70}
{regional.to_string()}

TOP PRODUCTS
{'-'*70}
{products.head(5).to_string()}

{'='*70}
        End of Report
{'='*70}
"""
        return report


def generate_sample_data(n_records: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Generate sample sales data for demonstration.
    
    Args:
        n_records (int): Number of records to generate
        seed (int): Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Sample sales data
    """
    np.random.seed(seed)
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Electronics', 'Software', 'Services', 'Hardware', 'Consulting']
    
    dates = [
        datetime.now() - timedelta(days=x) 
        for x in np.random.randint(0, 365, n_records)
    ]
    
    data = {
        'order_id': [f'ORD-{i:05d}' for i in range(1, n_records + 1)],
        'customer_id': [f'CUST-{np.random.randint(100, 500):04d}' for _ in range(n_records)],
        'order_date': dates,
        'amount': np.random.gamma(2, 2000, n_records).round(2),
        'region': np.random.choice(regions, n_records),
        'product_category': np.random.choice(categories, n_records),
        'quantity': np.random.randint(1, 20, n_records),
    }
    
    return pd.DataFrame(data)


if __name__ == '__main__':
    # Generate sample data and perform analysis
    print("Generating sample sales data...")
    sales_data = generate_sample_data(n_records=5000)
    
    print("Initializing Sales Analyzer...")
    analyzer = SalesAnalyzer(sales_data)
    
    print(analyzer.generate_report())
