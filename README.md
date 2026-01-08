# BI Analyst - Business Intelligence Analysis Tool

A Python-based Business Intelligence analysis tool designed for data-driven decision making. Analyze sales data, identify trends, segment customers, and generate comprehensive business reports.

#Features

✨ **Core Capabilities**
- **Revenue Analysis**: Track total revenue, average order value, and transactions
- **Regional Performance**: Analyze sales by geographic region
- **Product Analytics**: Evaluate product category performance
- **Customer Segmentation**: Classify customers (VIP, Premium, Standard, New)
- **Monthly Trends**: Monitor revenue trends and month-over-month growth
- **Key Metrics**: Calculate important KPIs (repeat rate, revenue per customer, etc.)
- **Cohort Analysis**: Track customer cohorts over time
- **Dashboard Generation**: Create professional visualizations

📊 **Visualizations**
- Revenue trend charts
- Regional sales distribution
- Product performance comparisons
- Customer lifetime value distributions
- KPI dashboards
- Pie charts and bar charts

📈 **Business Insights**
- Growth rate analysis
- Customer lifetime value (LTV)
- Recency, Frequency, Monetary (RFM) analysis
- Forecast indicators
- Comprehensive text reports

#Installation

##Prerequisites
- Python 3.8 or higher
- pip or conda

##Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/bi-analyst.git
cd bi-analyst
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

##Install from PyPI (when available)
```bash
pip install bi-analyst
```

#Quick Start Guide

##Basic Usage

```python
from bi_analyst.sales_analyzer import SalesAnalyzer, generate_sample_data

# Generate sample data
sales_data = generate_sample_data(n_records=5000)

# Initialize analyzer
analyzer = SalesAnalyzer(sales_data)

# Get revenue summary
summary = analyzer.get_revenue_summary()
print(f"Total Revenue: ${summary['total_revenue']:,.2f}")
print(f"Average Order Value: ${summary['avg_order_value']:,.2f}")

# Analyze by region
regional = analyzer.get_regional_analysis()
print(regional)

# Generate report
report = analyzer.generate_report()
print(report)
```

##Generate Dashboards

```python
from bi_analyst.dashboard import DashboardGenerator

# Create dashboard generator
dashboard = DashboardGenerator(analyzer, output_dir='dashboards')

# Generate all dashboards
dashboard.generate_all_dashboards()
```

#API Reference

##SalesAnalyzer Class

Main class for business intelligence analysis.

###Methods

**`__init__(dataframe: pd.DataFrame)`**
- Initialize with sales data
- Required columns: order_id, customer_id, order_date, amount, region, product_category, quantity

**`get_revenue_summary() -> Dict`**
- Returns: Dictionary with total_revenue, avg_order_value, median_order_value, etc.

**`get_regional_analysis() -> pd.DataFrame`**
- Returns: DataFrame with revenue, avg order value, transactions by region

**`get_product_performance() -> pd.DataFrame`**
- Returns: DataFrame with revenue, quantity sold, unique customers by product

**`get_monthly_trends() -> pd.DataFrame`**
- Returns: DataFrame with monthly revenue, transactions, and month-over-month growth

**`get_customer_segmentation() -> pd.DataFrame`**
- Returns: DataFrame with customer segments, lifetime value, and RFM metrics

**`get_key_metrics() -> Dict`**
- Returns: Dictionary with YTD revenue, growth rate, repeat customer rate, etc.

**`get_top_customers(n: int = 10) -> pd.DataFrame`**
- Args: n - number of customers to return
- Returns: DataFrame with top N customers by revenue

**`get_cohort_analysis() -> pd.DataFrame`**
- Returns: Cohort-based analysis DataFrame

**`get_sales_forecast_indicators() -> Dict`**
- Returns: Dictionary with trend indicators and volatility metrics

**`generate_report() -> str`**
- Returns: Formatted text report with all major metrics

##DashboardGenerator Class

Generates visualizations and dashboards.

**`create_revenue_dashboard(save: bool = True) -> Optional[str]`**
- Creates revenue analysis dashboard (2x2 subplots)
- Returns: Path to saved image

**`create_customer_dashboard(save: bool = True) -> Optional[str]`**
- Creates customer analysis dashboard
- Returns: Path to saved image

**`create_performance_metrics_dashboard(save: bool = True) -> Optional[str]`**
- Creates KPI metrics dashboard
- Returns: Path to saved image

**`generate_all_dashboards() -> list`**
- Generates all available dashboards
- Returns: List of file paths

#Data Format

Your sales data should have these columns:

| Column | Type | Description |
|--------|------|-------------|
| order_id | str | Unique order identifier |
| customer_id | str | Customer identifier |
| order_date | datetime | Date of order |
| amount | float | Sale amount in dollars |
| region | str | Geographic region |
| product_category | str | Product category |
| quantity | int | Number of units sold |

##Example Data Format

```python
import pandas as pd

data = {
    'order_id': ['ORD-00001', 'ORD-00002', ...],
    'customer_id': ['CUST-0100', 'CUST-0101', ...],
    'order_date': ['2024-01-15', '2024-01-16', ...],
    'amount': [4500.50, 2300.00, ...],
    'region': ['North', 'South', ...],
    'product_category': ['Electronics', 'Software', ...],
    'quantity': [5, 3, ...]
}

df = pd.DataFrame(data)
```

#Usage Examples

##Example 1: Basic Analysis

```python
from bi_analyst.sales_analyzer import SalesAnalyzer, generate_sample_data

# Generate sample data
sales_data = generate_sample_data(n_records=10000)

# Create analyzer
analyzer = SalesAnalyzer(sales_data)

# Get key metrics
metrics = analyzer.get_key_metrics()
print(f"YTD Revenue: ${metrics['YTD_Revenue']:,.2f}")
print(f"Customer Count: {metrics['Customer_Count']}")
```

##Example 2: Regional Analysis

```python
# Analyze performance by region
regional = analyzer.get_regional_analysis()
print(regional)

# Top performing region
best_region = regional['Revenue'].idxmax()
print(f"Best Region: {best_region}")
```

##Example 3: Customer Segmentation

```python
# Segment customers
segments = analyzer.get_customer_segmentation()

# VIP customers
vip_customers = segments[segments['segment'] == 'VIP']
print(f"VIP Customer Count: {len(vip_customers)}")
print(f"VIP Revenue: ${vip_customers['lifetime_value'].sum():,.2f}")
```

##Example 4: Generate Report

```python
# Generate comprehensive text report
report = analyzer.generate_report()
print(report)

# Save to file
with open('sales_report.txt', 'w') as f:
    f.write(report)
```

##Example 5: Create Visualizations

```python
from bi_analyst.dashboard import DashboardGenerator

# Create dashboards
dashboards = DashboardGenerator(analyzer, output_dir='reports')
dashboards.create_revenue_dashboard()
dashboards.create_customer_dashboard()
dashboards.create_performance_metrics_dashboard()
```

#Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bi_analyst

# Run specific test file
pytest tests/test_sales_analyzer.py -v
```

#Project Structure

```
bi-analyst/
├── bi_analyst/
│   ├── __init__.py
│   ├── sales_analyzer.py          # Main analysis module
│   ├── dashboard.py               # Dashboard generation
│   └── utils.py                   # Utility functions
├── tests/
│   ├── test_sales_analyzer.py
│   └── test_dashboard.py
├── examples/
│   ├── basic_analysis.py
│   ├── dashboard_example.py
│   └── data_example.csv
├── dashboards/                    # Generated visualizations
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
├── README.md                      # This file
├── LICENSE                        # MIT License
└── .gitignore                     # Git ignore rules
```

#Key Metrics Explained

- **YTD Revenue**: Total revenue for the year-to-date
- **Avg Monthly Revenue**: Average monthly sales
- **Growth Rate (%)**: Month-over-month percentage change
- **Customer Count**: Total unique customers
- **Revenue Per Customer**: Average revenue generated per customer
- **Repeat Customer Rate (%)**: Percentage of customers with multiple purchases
- **Customer Lifetime Value (LTV)**: Total amount spent by a customer
- **RFM Analysis**: Recency (days since last purchase), Frequency (purchase count), Monetary (total spent)

#Visualization Dashboards

##Revenue Dashboard
- Monthly revenue trend line
- Revenue by region (bar chart)
- Top products (horizontal bar)
- Transaction distribution by region (pie chart)

##Customer Dashboard
- Customer segmentation distribution
- Revenue by customer segment
- Top 10 customers
- Customer lifetime value distribution

##Metrics Dashboard
- 6 key KPI cards
- YTD Revenue
- Average Monthly Revenue
- Growth Rate
- Total Customers
- Revenue Per Customer
- Repeat Customer Rate

#Performance

- **Data Processing**: Handles 10,000+ records efficiently
- **Memory Usage**: Minimal overhead with DataFrame operations
- **Visualization**: High-resolution PNG output (300 DPI)
- **Execution Time**: < 2 seconds for typical analysis

#Troubleshooting

##Missing Columns Error
Ensure your DataFrame has all required columns:
```python
required = ['order_id', 'customer_id', 'order_date', 'amount', 
            'region', 'product_category', 'quantity']
```

##Date Format Issues
Make sure dates are in standard format or convert them:
```python
df['order_date'] = pd.to_datetime(df['order_date'])
```

##Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

#Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

#License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

#Support

For issues, questions, or suggestions:
- Open an [GitHub Issue](https://github.com/yourusername/bi-analyst/issues)
- Contact: your.email@example.com

#Roadmap

- [ ] Add SQL database integration
- [ ] Implement real-time dashboards
- [ ] Add forecasting models (ARIMA, Prophet)
- [ ] Create web-based dashboard (Flask/Django)
- [ ] Add export to Excel/PDF
- [ ] Implement machine learning for anomaly detection
- [ ] Add multi-currency support
- [ ] Create API endpoint

#Changelog

##Version 1.0.0 (2024-01-06)
- Initial release
- Core analysis functionality
- Dashboard generation
- Comprehensive documentation
- Test suite

#Authors

- **Your Name** - Initial work

#Acknowledgments

- Built with pandas, numpy, and matplotlib
- Inspired by business intelligence best practices
- Data science community

#Related Projects

- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [NumPy Documentation](https://numpy.org/)

**Ready to analyze!** Start with the [Quick Start Guide](#quick-start-guide) above.
