import pandas as pd
from datetime import datetime
from typing import List, Optional

class DataProcessor:
    def __init__(self, df):
        self.df = df
        self.df['date'] = pd.to_datetime(self.df['date'])

    def filter_data(self, start_date, end_date, companies: Optional[List[str]]=None, category=None):
        """Filter dataframe based on date range and optional company/category"""
        mask = (self.df['date'].dt.date >= start_date) & (self.df['date'].dt.date <= end_date)

        filtered_df = self.df[mask].copy()

        if companies:
            filtered_df = filtered_df[filtered_df['company'].isin(companies)]

        if category:
            filtered_df = filtered_df[filtered_df['category'] == category]

        return filtered_df

    def get_company_metrics(self, df):
        """Calculate company-level metrics"""
        return df.groupby('company').agg({
            'product': 'count',
            'category': 'nunique'
        }).reset_index()

    def get_product_metrics(self, df):
        """Calculate product-level metrics"""
        return df.groupby('product').agg({
            'company': 'count',
            'category': 'nunique'
        }).reset_index()

    def get_time_series_data(self, df, group_by=None):
        """Prepare time series data with optional grouping"""
        if group_by:
            return df.groupby(['date', group_by]).size().reset_index(name='count')
        return df.groupby('date').size().reset_index(name='count')