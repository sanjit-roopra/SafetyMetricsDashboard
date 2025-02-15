# FSN KPI Dashboard

## Overview
A sophisticated Streamlit-based Field Safety Notice (FSN) KPI dashboard for comprehensive business performance analysis. This dashboard provides interactive visualizations and insights for tracking Field Safety Notices across multiple companies and products.

## Key Features
- **Interactive Multi-Company Analysis**: Compare FSN patterns across different companies
- **Dynamic Data Filtering**: Filter by date range, companies, and categories
- **Real-time KPI Tracking**: Monitor key metrics including total FSNs, companies, products, and categories
- **Rich Visualizations**:
  - Time-based analysis with interactive timeline
  - Company-level comparison charts
  - Product analysis visualizations
- **Detailed Data View**: Searchable and sortable table of all FSN entries

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd fsn-dashboard
```

2. Install required packages:
```bash
pip install streamlit pandas plotly
```

3. Create the required directory structure:
```
.
├── .streamlit/
│   └── config.toml
├── assets/
│   └── styles.css
├── utils/
│   ├── data_processor.py
│   └── visualization.py
└── main.py
```

## Running the Dashboard

1. Start the Streamlit server:
```bash
streamlit run main.py
```

2. Access the dashboard in your web browser at `http://localhost:5000`

## Data Structure
The dashboard expects JSON data in the following format:
```json
{
    "product": "Product Name",
    "company": "Company Name",
    "date": "YYYY-MM-DD",
    "title": "FSN Title",
    "category": "Category Name",
    "reference_number": "Reference ID",
    "link": "URL to PDF document"
}
```

## Usage Guide

### Available Filters
- **Date Range**: Select specific time periods for analysis
- **Companies**: Choose one or multiple companies for comparison
- **Categories**: Filter by specific FSN categories

### Views
1. **Time Analysis**: Visualizes FSN trends over time
2. **Company Analysis**: Shows FSN distribution across companies
3. **Product Analysis**: Displays top products by FSN count
4. **FSN Details**: Detailed table view with all FSN information

## Development

### Project Structure
- `main.py`: Main application file and UI components
- `utils/data_processor.py`: Data processing and filtering logic
- `utils/visualization.py`: Chart generation and visualization components
- `assets/styles.css`: Custom styling
- `.streamlit/config.toml`: Streamlit configuration

### Configuration
The dashboard can be configured through `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#007bff"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#212529"
```

## License
[License Information]

## Contributing
[Contribution Guidelines]
