# Stock-Analysis-Dashboard

This project is an interactive web application for financial stock analysis, built with Streamlit and Python. It allows users to perform detailed technical and fundamental analysis on one or two stocks simultaneously, providing a comprehensive view for making informed decisions.

The dashboard uses a hybrid data approach, leveraging the **OpenBB** toolkit for robust historical price data and the **yfinance** library for reliable fundamental and news data.

## Features

  * **Dual Stock Comparison:** Analyze two stocks in a vertically stacked layout to easily compare performance and metrics.
  * **Interactive Financial Charts:** Professional-grade, multi-panel charts powered by Plotly, featuring:
      * **Candlestick Price View:** Shows the daily Open, High, Low, and Close prices for detailed price action analysis.
      * **Volume Analysis:** An integrated volume bar chart to gauge the strength and confirmation of price movements.
  * **Selectable Technical Indicators:** A dynamic secondary chart panel with a dropdown menu to choose between popular momentum indicators:
      * **MACD (Moving Average Convergence Divergence)**
      * **RSI (Relative Strength Index)**
  * **Fundamental Data at a Glance:** A dedicated section for each stock displaying key financial metrics, including:
      * Market Cap
      * P/E Ratio
      * EPS (Earnings Per Share)
      * 52-Week High
  * **Detailed Company Profile:** Includes a full business summary and sector/industry information to provide context behind the numbers.
  * **Real-time News Feed:** A list of the latest company-specific news headlines to understand what's driving the stock's performance.
  * **Customizable Analysis:** An interactive sidebar allows users to select any stock tickers and a custom date range for historical analysis.

## Technologies Used

  * **Web Framework:** Streamlit
  * **Data Manipulation:** pandas
  * **Data Sources:** OpenBB & yfinance
  * **Charting:** Plotly
  * **Technical Indicators:** pandas\_ta
  * **Language:** Python

## How to Run the Project Locally

Follow these steps to set up and run the dashboard on your own machine.

**1. Prerequisites -**
Ensure you have Python 3.8 or newer installed on your system.

**2. Download the Python File -**
Download the `stock_dashboard.py` file.

**3. Install Dependencies -**
Install all the required Python libraries using pip. This single command will install everything you need.

*Note: This command specifically installs a version of NumPy that is compatible with all other libraries to avoid potential version conflicts.*

```
pip install streamlit pandas openbb yfinance plotly pandas_ta "numpy<2.0"
```

**4. Run the Streamlit App -**
Execute the following command in your terminal from the folder where the file is located.

```
streamlit run stock_dashboard.py
```

Your web browser will automatically open with the running application.

## Dashboard Screenshots

![image](https://github.com/user-attachments/assets/25d2d45d-18e4-4a50-9c93-957fedcfb547)

![image](https://github.com/user-attachments/assets/8830beb9-3027-491f-8233-4834f7d59671)

