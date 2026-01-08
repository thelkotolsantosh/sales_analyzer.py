"""
Unit tests for Sales Analyzer module.
"""

import pytest
import pandas as pd
import numpy as np
from bi_analyst.sales_analyzer import SalesAnalyzer, generate_sample_data


class TestSalesAnalyzer:
    """Test suite for SalesAnalyzer class."""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        return generate_sample_data(n_records=1000, seed=42)
    
    @pytest.fixture
    def analyzer(self, sample_data):
        """Create analyzer instance."""
        return SalesAnalyzer(sample_data)
    
    def test_initialization(self, analyzer):
        """Test that analyzer initializes correctly."""
        assert analyzer.df is not None
        assert len(analyzer.df) > 0
        assert 'order_id' in analyzer.df.columns
    
    def test_get_revenue_summary(self, analyzer):
        """Test revenue summary calculation."""
        summary = analyzer.get_revenue_summary()
        
        assert 'total_revenue' in summary
        assert 'avg_order_value' in summary
        assert 'total_transactions' in summary
        assert summary['total_revenue'] > 0
        assert summary['avg_order_value'] > 0
        assert summary['total_transactions'] > 0
    
    def test_get_regional_analysis(self, analyzer):
        """Test regional analysis."""
        regional = analyzer.get_regional_analysis()
        
        assert isinstance(regional, pd.DataFrame)
        assert 'Revenue' in regional.columns
        assert len(regional) > 0
        assert regional['Revenue'].sum() > 0
    
    def test_get_product_performance(self, analyzer):
        """Test product performance analysis."""
        products = analyzer.get_product_performance()
        
        assert isinstance(products, pd.DataFrame)
        assert 'Revenue' in products.columns
        assert len(products) > 0
    
    def test_get_monthly_trends(self, analyzer):
        """Test monthly trends."""
        monthly = analyzer.get_monthly_trends()
        
        assert isinstance(monthly, pd.DataFrame)
        assert 'Revenue' in monthly.columns
        assert 'MoM_Growth_%' in monthly.columns
    
    def test_get_customer_segmentation(self, analyzer):
        """Test customer segmentation."""
        segments = analyzer.get_customer_segmentation()
        
        assert isinstance(segments, pd.DataFrame)
        assert 'segment' in segments.columns
        assert 'lifetime_value' in segments.columns
        
        # Check that segments are valid
        valid_segments = {'VIP', 'Premium', 'Standard', 'New'}
        assert set(segments['segment'].unique()).issubset(valid_segments)
    
    def test_get_key_metrics(self, analyzer):
        """Test key metrics calculation."""
        metrics = analyzer.get_key_metrics()
        
        assert 'YTD_Revenue' in metrics
        assert 'Avg_Monthly_Revenue' in metrics
        assert 'Customer_Count' in metrics
        assert 'Repeat_Customer_Rate_%' in metrics
        
        assert metrics['Customer_Count'] > 0
        assert 0 <= metrics['Repeat_Customer_Rate_%'] <= 100
    
    def test_get_top_customers(self, analyzer):
        """Test top customers retrieval."""
        top = analyzer.get_top_customers(n=5)
        
        assert len(top) <= 5
        assert 'customer_id' in top.columns
        assert 'total_spent' in top.columns
        
        # Check that values are sorted
        assert top['total_spent'].is_monotonic_decreasing
    
    def test_get_cohort_analysis(self, analyzer):
        """Test cohort analysis."""
        cohorts = analyzer.get_cohort_analysis()
        
        assert isinstance(cohorts, pd.DataFrame)
        assert len(cohorts) > 0
    
    def test_get_sales_forecast_indicators(self, analyzer):
        """Test forecast indicators."""
        indicators = analyzer.get_sales_forecast_indicators()
        
        assert 'latest_month_revenue' in indicators
        assert 'trend_direction' in indicators
        assert indicators['trend_direction'] in ['UP', 'DOWN']
    
    def test_generate_report(self, analyzer):
        """Test report generation."""
        report = analyzer.generate_report()
        
        assert isinstance(report, str)
        assert 'SALES ANALYTICS REPORT' in report
        assert 'REVENUE SUMMARY' in report
        assert '$' in report
    
    def test_missing_columns_raises_error(self):
        """Test that missing required columns raise error."""
        incomplete_data = pd.DataFrame({
            'order_id': [1, 2, 3],
            'amount': [100, 200, 300]
        })
        
        with pytest.raises(ValueError):
            SalesAnalyzer(incomplete_data)
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        empty_df = pd.DataFrame({
            'order_id': [],
            'customer_id': [],
            'order_date': [],
            'amount': [],
            'region': [],
            'product_category': [],
            'quantity': []
        })
        
        analyzer = SalesAnalyzer(empty_df)
        summary = analyzer.get_revenue_summary()
        
        assert summary['total_revenue'] == 0
        assert summary['total_transactions'] == 0


class TestGenerateSampleData:
    """Test suite for sample data generation."""
    
    def test_generates_correct_size(self):
        """Test that correct number of records are generated."""
        data = generate_sample_data(n_records=500, seed=42)
        assert len(data) == 500
    
    def test_has_required_columns(self):
        """Test that all required columns are present."""
        data = generate_sample_data()
        
        required_cols = [
            'order_id', 'customer_id', 'order_date', 'amount',
            'region', 'product_category', 'quantity'
        ]
        
        for col in required_cols:
            assert col in data.columns
    
    def test_reproducibility(self):
        """Test that same seed produces same data."""
        data1 = generate_sample_data(n_records=100, seed=42)
        data2 = generate_sample_data(n_records=100, seed=42)
        
        pd.testing.assert_frame_equal(data1, data2)
    
    def test_different_seeds_different_data(self):
        """Test that different seeds produce different data."""
        data1 = generate_sample_data(n_records=100, seed=42)
        data2 = generate_sample_data(n_records=100, seed=43)
        
        assert not data1.equals(data2)
    
    def test_data_types(self):
        """Test that columns have correct data types."""
        data = generate_sample_data()
        
        assert data['order_id'].dtype == object
        assert data['customer_id'].dtype == object
        assert pd.api.types.is_datetime64_any_dtype(data['order_date'])
        assert data['amount'].dtype in [np.float64, float]
        assert data['quantity'].dtype in [np.int64, int]


class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow."""
        # Generate data
        data = generate_sample_data(n_records=5000, seed=42)
        
        # Create analyzer
        analyzer = SalesAnalyzer(data)
        
        # Run all analyses
        summary = analyzer.get_revenue_summary()
        regional = analyzer.get_regional_analysis()
        products = analyzer.get_product_performance()
        metrics = analyzer.get_key_metrics()
        segments = analyzer.get_customer_segmentation()
        
        # Verify results are consistent
        assert summary['total_revenue'] > 0
        assert len(regional) > 0
        assert len(products) > 0
        assert metrics['Customer_Count'] > 0
        assert len(segments) > 0
    
    def test_custom_data_workflow(self):
        """Test with custom data."""
        custom_data = pd.DataFrame({
            'order_id': ['ORD-001', 'ORD-002', 'ORD-003'],
            'customer_id': ['CUST-001', 'CUST-002', 'CUST-001'],
            'order_date': pd.date_range('2024-01-01', periods=3),
            'amount': [1000, 2000, 1500],
            'region': ['North', 'South', 'North'],
            'product_category': ['Electronics', 'Software', 'Electronics'],
            'quantity': [2, 1, 3]
        })
        
        analyzer = SalesAnalyzer(custom_data)
        summary = analyzer.get_revenue_summary()
        
        assert summary['total_revenue'] == 4500
        assert summary['total_transactions'] == 3
