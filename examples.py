"""
BI Analyst Examples

This script demonstrates how to use the BI Analyst library
for sales data analysis and business intelligence.
"""

from bi_analyst.sales_analyzer import SalesAnalyzer, generate_sample_data
from bi_analyst.dashboard import DashboardGenerator


def example_1_basic_analysis():
    """Example 1: Basic Sales Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Sales Analysis")
    print("="*70)
    
    # Generate sample data
    print("\nGenerating sample sales data...")
    sales_data = generate_sample_data(n_records=5000, seed=42)
    
    # Create analyzer
    analyzer = SalesAnalyzer(sales_data)
    
    # Get revenue summary
    summary = analyzer.get_revenue_summary()
    print(f"\nRevenue Summary:")
    print(f"  Total Revenue: ${summary['total_revenue']:,.2f}")
    print(f"  Avg Order Value: ${summary['avg_order_value']:,.2f}")
    print(f"  Total Transactions: {summary['total_transactions']:,}")
    print(f"  Total Units Sold: {summary['total_units_sold']:,}")


def example_2_regional_analysis():
    """Example 2: Regional Performance Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Regional Performance Analysis")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get regional analysis
    regional = analyzer.get_regional_analysis()
    print("\nRevenue by Region:")
    print(regional)
    
    # Find best and worst regions
    best_region = regional['Revenue'].idxmax()
    worst_region = regional['Revenue'].idxmin()
    
    print(f"\nBest Region: {best_region} (${regional.loc[best_region, 'Revenue']:,.2f})")
    print(f"Worst Region: {worst_region} (${regional.loc[worst_region, 'Revenue']:,.2f})")


def example_3_product_analysis():
    """Example 3: Product Performance Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Product Performance Analysis")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get product performance
    products = analyzer.get_product_performance()
    print("\nRevenue by Product Category:")
    print(products)
    
    # Top product
    top_product = products['Revenue'].idxmax()
    print(f"\nTop Product: {top_product}")
    print(f"  Revenue: ${products.loc[top_product, 'Revenue']:,.2f}")
    print(f"  Quantity Sold: {products.loc[top_product, 'Quantity_Sold']:.0f} units")


def example_4_customer_segmentation():
    """Example 4: Customer Segmentation"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Customer Segmentation")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get customer segments
    segments = analyzer.get_customer_segmentation()
    
    # Segment summary
    print("\nCustomer Segments Distribution:")
    segment_summary = segments.groupby('segment').agg({
        'customer_id': 'count',
        'lifetime_value': ['sum', 'mean']
    }).round(2)
    segment_summary.columns = ['Count', 'Total_Value', 'Avg_Value']
    print(segment_summary)
    
    # VIP analysis
    vip_customers = segments[segments['segment'] == 'VIP']
    print(f"\nVIP Customers:")
    print(f"  Count: {len(vip_customers)}")
    print(f"  Total Revenue: ${vip_customers['lifetime_value'].sum():,.2f}")
    print(f"  Avg LTV: ${vip_customers['lifetime_value'].mean():,.2f}")


def example_5_monthly_trends():
    """Example 5: Monthly Trends and Growth Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Monthly Trends and Growth Analysis")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get monthly trends
    monthly = analyzer.get_monthly_trends()
    print("\nMonthly Revenue Trends:")
    print(monthly)
    
    # Calculate metrics
    print(f"\nGrowth Metrics:")
    print(f"  Avg Growth Rate: {monthly['MoM_Growth_%'].mean():.2f}%")
    print(f"  Max Monthly Revenue: ${monthly['Revenue'].max():,.2f}")
    print(f"  Min Monthly Revenue: ${monthly['Revenue'].min():,.2f}")


def example_6_key_metrics():
    """Example 6: Key Business Metrics (KPIs)"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Key Business Metrics (KPIs)")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get KPIs
    metrics = analyzer.get_key_metrics()
    
    print("\nKey Performance Indicators:")
    print(f"  YTD Revenue: ${metrics['YTD_Revenue']:,.2f}")
    print(f"  Avg Monthly Revenue: ${metrics['Avg_Monthly_Revenue']:,.2f}")
    print(f"  Growth Rate (MoM): {metrics['Growth_Rate_%']:.2f}%")
    print(f"  Total Customers: {metrics['Customer_Count']:,}")
    print(f"  Revenue Per Customer: ${metrics['Revenue_Per_Customer']:,.2f}")
    print(f"  Repeat Customer Rate: {metrics['Repeat_Customer_Rate_%']:.2f}%")


def example_7_top_customers():
    """Example 7: Top Customers Analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Top Customers Analysis")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get top customers
    top_customers = analyzer.get_top_customers(n=10)
    print("\nTop 10 Customers by Revenue:")
    print(top_customers)


def example_8_comprehensive_report():
    """Example 8: Generate Comprehensive Report"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Comprehensive Business Report")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Generate report
    report = analyzer.generate_report()
    print(report)


def example_9_dashboard_generation():
    """Example 9: Generate Dashboards"""
    print("\n" + "="*70)
    print("EXAMPLE 9: Dashboard Generation")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Create dashboards
    dashboard = DashboardGenerator(analyzer, output_dir='dashboards')
    
    print("\nGenerating dashboards...")
    dashboard.create_revenue_dashboard()
    print("✓ Revenue dashboard created")
    
    dashboard.create_customer_dashboard()
    print("✓ Customer dashboard created")
    
    dashboard.create_performance_metrics_dashboard()
    print("✓ Metrics dashboard created")
    
    print("\nAll dashboards saved to 'dashboards/' directory")


def example_10_forecast_indicators():
    """Example 10: Sales Forecast Indicators"""
    print("\n" + "="*70)
    print("EXAMPLE 10: Sales Forecast Indicators")
    print("="*70)
    
    sales_data = generate_sample_data(n_records=5000, seed=42)
    analyzer = SalesAnalyzer(sales_data)
    
    # Get forecast indicators
    indicators = analyzer.get_sales_forecast_indicators()
    
    print("\nForecast Indicators:")
    print(f"  Latest Month Revenue: ${indicators['latest_month_revenue']:,.2f}")
    print(f"  Previous Month Revenue: ${indicators['previous_month_revenue']:,.2f}")
    print(f"  Average Monthly: ${indicators['avg_monthly']:,.2f}")
    print(f"  Trend Direction: {indicators['trend_direction']}")
    print(f"  Volatility: {indicators['volatility']:.3f}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("        BI ANALYST - BUSINESS INTELLIGENCE EXAMPLES")
    print("="*70)
    
    # Run all examples
    example_1_basic_analysis()
    example_2_regional_analysis()
    example_3_product_analysis()
    example_4_customer_segmentation()
    example_5_monthly_trends()
    example_6_key_metrics()
    example_7_top_customers()
    example_8_comprehensive_report()
    example_9_dashboard_generation()
    example_10_forecast_indicators()
    
    print("\n" + "="*70)
    print("                    END OF EXAMPLES")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
