"""
Dashboard Module for Business Intelligence

Generates visualizations and dashboards for business metrics.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Optional
import os


class DashboardGenerator:
    """Generate business intelligence dashboards and visualizations."""
    
    def __init__(self, analyzer, output_dir: str = 'dashboards'):
        """
        Initialize dashboard generator.
        
        Args:
            analyzer: SalesAnalyzer instance
            output_dir (str): Directory to save dashboard outputs
        """
        self.analyzer = analyzer
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_revenue_dashboard(self, save: bool = True) -> Optional[str]:
        """
        Create revenue analysis dashboard.
        
        Args:
            save (bool): Whether to save the dashboard
            
        Returns:
            str: Path to saved dashboard
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Revenue Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # Monthly trend
        monthly = self.analyzer.get_monthly_trends()
        axes[0, 0].plot(monthly.index.astype(str), monthly['Revenue'], marker='o', linewidth=2)
        axes[0, 0].set_title('Monthly Revenue Trend')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Revenue ($)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Regional breakdown
        regional = self.analyzer.get_regional_analysis()
        axes[0, 1].bar(regional.index, regional['Revenue'], color='steelblue')
        axes[0, 1].set_title('Revenue by Region')
        axes[0, 1].set_ylabel('Revenue ($)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Product performance
        products = self.analyzer.get_product_performance()
        axes[1, 0].barh(products.index, products['Revenue'], color='coral')
        axes[1, 0].set_title('Revenue by Product Category')
        axes[1, 0].set_xlabel('Revenue ($)')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # Transaction count by region
        regional_count = self.analyzer.get_regional_analysis()
        axes[1, 1].pie(regional_count['Transactions'], labels=regional_count.index,
                       autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Transaction Distribution by Region')
        
        plt.tight_layout()
        
        if save:
            path = os.path.join(self.output_dir, 'revenue_dashboard.png')
            plt.savefig(path, dpi=300, bbox_inches='tight')
            plt.close()
            return path
        
        return None
    
    def create_customer_dashboard(self, save: bool = True) -> Optional[str]:
        """
        Create customer analysis dashboard.
        
        Args:
            save (bool): Whether to save the dashboard
            
        Returns:
            str: Path to saved dashboard
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Customer Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # Customer segments
        segments = self.analyzer.get_customer_segmentation()
        segment_counts = segments['segment'].value_counts()
        axes[0, 0].bar(segment_counts.index, segment_counts.values, color='lightgreen')
        axes[0, 0].set_title('Customer Segmentation')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Segment revenue distribution
        segment_revenue = segments.groupby('segment')['lifetime_value'].sum()
        axes[0, 1].pie(segment_revenue, labels=segment_revenue.index,
                       autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Revenue Distribution by Segment')
        
        # Top customers
        top_customers = self.analyzer.get_top_customers(10)
        axes[1, 0].barh(range(len(top_customers)), top_customers['total_spent'],
                       color='skyblue')
        axes[1, 0].set_yticks(range(len(top_customers)))
        axes[1, 0].set_yticklabels(top_customers['customer_id'])
        axes[1, 0].set_title('Top 10 Customers by Revenue')
        axes[1, 0].set_xlabel('Total Spent ($)')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # Customer lifetime value distribution
        axes[1, 1].hist(segments['lifetime_value'], bins=30, color='purple', alpha=0.7)
        axes[1, 1].set_title('Customer Lifetime Value Distribution')
        axes[1, 1].set_xlabel('Lifetime Value ($)')
        axes[1, 1].set_ylabel('Customer Count')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            path = os.path.join(self.output_dir, 'customer_dashboard.png')
            plt.savefig(path, dpi=300, bbox_inches='tight')
            plt.close()
            return path
        
        return None
    
    def create_performance_metrics_dashboard(self, save: bool = True) -> Optional[str]:
        """
        Create KPI and performance metrics dashboard.
        
        Args:
            save (bool): Whether to save the dashboard
            
        Returns:
            str: Path to saved dashboard
        """
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('Key Performance Indicators Dashboard', fontsize=16, fontweight='bold')
        
        kpis = self.analyzer.get_key_metrics()
        
        # Create grid for KPI boxes
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # KPI cards
        kpi_data = [
            ('YTD Revenue', f"${kpis['YTD_Revenue']:,.0f}"),
            ('Avg Monthly', f"${kpis['Avg_Monthly_Revenue']:,.0f}"),
            ('Growth Rate', f"{kpis['Growth_Rate_%']:.2f}%"),
            ('Total Customers', f"{kpis['Customer_Count']:,}"),
            ('Revenue/Customer', f"${kpis['Revenue_Per_Customer']:,.0f}"),
            ('Repeat Rate', f"{kpis['Repeat_Customer_Rate_%']:.1f}%"),
        ]
        
        for idx, (label, value) in enumerate(kpi_data):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            ax.axis('off')
            ax.text(0.5, 0.6, value, ha='center', va='center',
                   fontsize=24, fontweight='bold', transform=ax.transAxes)
            ax.text(0.5, 0.2, label, ha='center', va='center',
                   fontsize=12, transform=ax.transAxes)
            ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9,
                         fill=False, edgecolor='gray', linewidth=2,
                         transform=ax.transAxes))
        
        if save:
            path = os.path.join(self.output_dir, 'metrics_dashboard.png')
            plt.savefig(path, dpi=300, bbox_inches='tight')
            plt.close()
            return path
        
        return None
    
    def generate_all_dashboards(self) -> list:
        """
        Generate all available dashboards.
        
        Returns:
            list: Paths to generated dashboard files
        """
        paths = []
        print("Generating Revenue Dashboard...")
        paths.append(self.create_revenue_dashboard())
        
        print("Generating Customer Dashboard...")
        paths.append(self.create_customer_dashboard())
        
        print("Generating Metrics Dashboard...")
        paths.append(self.create_performance_metrics_dashboard())
        
        print(f"\nAll dashboards saved to: {self.output_dir}")
        return paths
