import plotly.express as px
import plotly.graph_objects as go

class Visualizer:
    def create_timeline_chart(self, df):
        """Create timeline chart of FSNs"""
        fig = px.line(
            df.groupby('date').size().reset_index(name='count'),
            x='date',
            y='count',
            title='FSNs Over Time',
            labels={'count': 'Number of FSNs', 'date': 'Date'}
        )
        fig.update_layout(
            hovermode='x unified',
            showlegend=False
        )
        return fig
    
    def create_company_chart(self, df):
        """Create company analysis chart"""
        company_counts = df['company'].value_counts().head(10)
        fig = px.bar(
            x=company_counts.index,
            y=company_counts.values,
            title='Top 10 Companies by FSN Count',
            labels={'x': 'Company', 'y': 'Number of FSNs'}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False
        )
        return fig
    
    def create_product_chart(self, df):
        """Create product analysis chart"""
        product_counts = df['product'].value_counts().head(10)
        fig = px.bar(
            x=product_counts.index,
            y=product_counts.values,
            title='Top 10 Products by FSN Count',
            labels={'x': 'Product', 'y': 'Number of FSNs'}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False
        )
        return fig
