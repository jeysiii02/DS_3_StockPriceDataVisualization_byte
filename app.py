# Import the libraries needed for the interactive stock visualization website
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf


# Configure the Streamlit page and browser tab
st.set_page_config(
    page_title="Stock Price Data Visualization",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Add custom CSS for the dashboard's visual design
st.markdown(
    """
    <style>
        /* Import a modern font for the dashboard */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        /* Apply the font throughout the application */
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        /* Set the main application background */
        .stApp {
            background: #0b1220;
            color: #e5e7eb;
        }

        /* Control the width and spacing of the main content */
        .block-container {
            padding-top: 2.8rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        /* Style the sidebar */
        section[data-testid="stSidebar"] {
            background: #101827;
            border-right: 1px solid #1f2937;
        }

        /* Sidebar title */
        .sidebar-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #f3f4f6;
            letter-spacing: -0.02em;
            margin-bottom: 0.3rem;
        }

        /* Sidebar description */
        .sidebar-description {
            color: #94a3b8;
            font-size: 0.82rem;
            line-height: 1.55;
            margin-bottom: 1.5rem;
        }

        /* Main page title */
        .main-title {
            font-size: 2.35rem;
            font-weight: 700;
            letter-spacing: -0.045em;
            color: #f8fafc;
            margin-bottom: 0.2rem;
        }

        /* Main page subtitle */
        .main-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 2rem;
        }

        /* Small section labels */
        .section-label {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        /* Metric cards */
        .metric-box {
            background: #111c2d;
            border: 1px solid #223047;
            border-radius: 10px;
            padding: 1.15rem 1.2rem;
            min-height: 105px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.12);
        }

        /* Metric labels */
        .metric-label {
            color: #94a3b8;
            font-size: 0.76rem;
            margin-bottom: 0.4rem;
        }

        /* Metric values */
        .metric-value {
            color: #f8fafc;
            font-size: 1.55rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }

        /* Chart containers */
        .chart-container {
            background: #111c2d;
            border: 1px solid #223047;
            border-radius: 10px;
            padding: 1.25rem 1.35rem 0.8rem 1.35rem;
            margin-top: 1.5rem;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.10);
        }

        /* Interpretation section */
        .interpretation {
            background: #111c2d;
            border-left: 3px solid #22c55e;
            border-top: 1px solid #223047;
            border-right: 1px solid #223047;
            border-bottom: 1px solid #223047;
            border-radius: 0 8px 8px 0;
            padding: 1.25rem 1.4rem;
            line-height: 1.7;
            color: #cbd5e1;
        }

        /* Footer */
        .footer-text {
            color: #64748b;
            font-size: 0.76rem;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid #1f2937;
        }

        /* Style the main action button */
        .stButton > button {
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 7px;
            font-weight: 600;
            transition: 0.2s ease;
        }

        /* Button hover state */
        .stButton > button:hover {
            background: #1d4ed8;
            color: white;
        }

        /* Style Streamlit input fields */
        div[data-baseweb="input"],
        div[data-baseweb="select"] {
            background: #111c2d;
        }

        /* Hide Streamlit's default menu */
        #MainMenu {
            visibility: hidden;
        }

        /* Hide Streamlit's default footer */
        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Create the sidebar containing the analysis controls
with st.sidebar:

    # Display the sidebar heading
    st.markdown(
        """
        <div class="sidebar-title">Stock Analysis</div>
        <div class="sidebar-description">
            Select a stock and date range to update the analysis.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Allow the user to enter a stock ticker
    ticker = st.text_input(
        "Ticker",
        value="AAPL",
        help="Enter a valid Yahoo Finance ticker symbol."
    ).upper().strip()

    # Allow the user to select the starting date
    start_date = st.date_input(
        "Start date",
        value=pd.Timestamp("2024-01-01")
    )

    # Allow the user to select the ending date
    end_date = st.date_input(
        "End date",
        value=pd.Timestamp("2025-01-01")
    )

    # Create the button used to refresh the analysis
    analyze = st.button(
        "Update analysis",
        use_container_width=True,
        type="primary"
    )

    # Add a divider between the controls and information
    st.markdown("---")

# Display the data source and analysis information in the sidebar
st.markdown(
    "**Data source**  \n"
    "Yahoo Finance via yfinance"
)

st.markdown(
    "**Analysis**  \n"
    "Closing price · Moving averages · Daily returns"
)


# Validate the selected date range
if start_date >= end_date:
    st.error("The end date must be later than the start date.")
    st.stop()


# Cache downloaded stock data to avoid unnecessary repeated requests
@st.cache_data
def load_stock_data(symbol, start, end):

    # Download daily stock data from Yahoo Finance
    data = yf.download(
        symbol,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        progress=False,
        multi_level_index=False
    )

    # Return an empty DataFrame if no data was found
    if data.empty:
        return pd.DataFrame()

    # Calculate the 20-day moving average
    data["MA20"] = data["Close"].rolling(window=20).mean()

    # Calculate the 50-day moving average
    data["MA50"] = data["Close"].rolling(window=50).mean()

    # Calculate the daily percentage return
    data["Daily_Return"] = data["Close"].pct_change()

    # Return the prepared dataset
    return data


# Download and prepare the selected stock data
df = load_stock_data(
    ticker,
    str(start_date),
    str(end_date)
)


# Stop the application if no stock data was returned
if df.empty:
    st.error(
        f"No data was found for {ticker} during the selected date range. "
        "Check the ticker symbol and try again."
    )
    st.stop()


# Calculate the total return
total_return = (
    df["Close"].iloc[-1] / df["Close"].iloc[0]
) - 1


# Calculate the average daily return
mean_daily_return = df["Daily_Return"].mean()


# Calculate the standard deviation of daily returns
daily_volatility = df["Daily_Return"].std()


# Annualize the daily volatility using approximately 252 trading days
annualized_volatility = daily_volatility * np.sqrt(252)


# Count positive-return trading days
positive_days = (
    df["Daily_Return"] > 0
).sum()


# Count negative-return trading days
negative_days = (
    df["Daily_Return"] < 0
).sum()


# Calculate the largest daily gain
largest_daily_gain = df["Daily_Return"].max()


# Calculate the largest daily loss
largest_daily_loss = df["Daily_Return"].min()


# Display the main page heading
st.markdown(
    f"""
    <div class="main-title">Stock Price Data Visualization</div>

    <div class="main-subtitle">
        {ticker}
        ·
        {pd.Timestamp(start_date).strftime('%b %d, %Y')}
        —
        {pd.Timestamp(end_date).strftime('%b %d, %Y')}
    </div>
    """,
    unsafe_allow_html=True
)


# Display the performance section label
st.markdown(
    '<div class="section-label">Performance snapshot</div>',
    unsafe_allow_html=True
)


# Create four columns for the key metrics
metric_columns = st.columns(4)


# Display total return
with metric_columns[0]:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Total return</div>
            <div class="metric-value">{total_return:.2%}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Display daily volatility
with metric_columns[1]:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Daily volatility</div>
            <div class="metric-value">{daily_volatility:.2%}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Display annualized volatility
with metric_columns[2]:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Annualized volatility</div>
            <div class="metric-value">{annualized_volatility:.2%}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Display the number of positive trading days
with metric_columns[3]:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Positive trading days</div>
            <div class="metric-value">{positive_days}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Create the closing price chart container
st.markdown(
    '<div class="chart-container">',
    unsafe_allow_html=True
)


# Display the chart title
st.markdown("#### Closing Price Trend")


# Create the closing price figure
fig, ax = plt.subplots(figsize=(13, 5))


# Plot the historical closing price using blue
ax.plot(
    df.index,
    df["Close"],
    linewidth=1.8,
    color="#60a5fa"
)


# Configure the closing price chart
ax.set_xlabel("")
ax.set_ylabel("Price (USD)")
ax.grid(True, alpha=0.12, color="#64748b")

# Style the chart tick labels
ax.tick_params(colors="#94a3b8")

# Style the axis labels
ax.xaxis.label.set_color("#94a3b8")
ax.yaxis.label.set_color("#94a3b8")

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#334155")
ax.spines["bottom"].set_color("#334155")


# Adjust the chart spacing
fig.tight_layout()


# Display the chart
st.pyplot(fig, use_container_width=True)


# Close the Matplotlib figure
plt.close(fig)


# Close the chart container
st.markdown("</div>", unsafe_allow_html=True)


# Create the moving averages chart container
st.markdown(
    '<div class="chart-container">',
    unsafe_allow_html=True
)


# Display the chart title
st.markdown("#### Moving Averages")


# Create the moving averages figure
fig, ax = plt.subplots(figsize=(13, 5))


# Plot the closing price in blue
ax.plot(
    df.index,
    df["Close"],
    linewidth=1.6,
    color="#60a5fa",
    label="Closing Price"
)


# Plot the 20-day moving average in green
ax.plot(
    df.index,
    df["MA20"],
    linewidth=1.5,
    color="#22c55e",
    label="20-Day MA"
)


# Plot the 50-day moving average in amber
ax.plot(
    df.index,
    df["MA50"],
    linewidth=1.5,
    color="#f59e0b",
    label="50-Day MA"
)


# Configure the moving average chart
ax.set_xlabel("")
ax.set_ylabel("Price (USD)")
ax.grid(True, alpha=0.12, color="#64748b")

# Style the chart tick labels
ax.tick_params(colors="#94a3b8")

# Style the axis labels
ax.xaxis.label.set_color("#94a3b8")
ax.yaxis.label.set_color("#94a3b8")

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#334155")
ax.spines["bottom"].set_color("#334155")

# Display the legend without a surrounding box
ax.legend(
    frameon=False,
    labelcolor="#cbd5e1"
)


# Adjust the chart spacing
fig.tight_layout()


# Display the chart
st.pyplot(fig, use_container_width=True)


# Close the Matplotlib figure
plt.close(fig)


# Close the chart container
st.markdown("</div>", unsafe_allow_html=True)


# Create the daily returns chart container
st.markdown(
    '<div class="chart-container">',
    unsafe_allow_html=True
)


# Display the chart title
st.markdown("#### Daily Returns Distribution")


# Create the daily returns figure
fig, ax = plt.subplots(figsize=(13, 5))


# Plot the distribution of daily returns
sns.histplot(
    df["Daily_Return"].dropna(),
    bins=50,
    kde=True,
    ax=ax,
    color="#60a5fa"
)


# Style the KDE curve
if len(ax.lines) > 0:
    ax.lines[-1].set_color("#22c55e")
    ax.lines[-1].set_linewidth(2)


# Add a reference line at zero return
ax.axvline(
    0,
    linestyle="--",
    linewidth=1.2,
    color="#f59e0b"
)


# Configure the daily returns chart
ax.set_xlabel("Daily Return")
ax.set_ylabel("Frequency")
ax.grid(True, alpha=0.10, color="#64748b")

# Style the chart tick labels
ax.tick_params(colors="#94a3b8")

# Style the axis labels
ax.xaxis.label.set_color("#94a3b8")
ax.yaxis.label.set_color("#94a3b8")

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#334155")
ax.spines["bottom"].set_color("#334155")


# Adjust the chart spacing
fig.tight_layout()


# Display the chart
st.pyplot(fig, use_container_width=True)


# Close the Matplotlib figure
plt.close(fig)


# Close the chart container
st.markdown("</div>", unsafe_allow_html=True)


# Display the interpretation section label
st.markdown(
    '<div class="section-label" style="margin-top: 2rem;">Interpretation</div>',
    unsafe_allow_html=True
)


# Create a concise interpretation based on the selected data
st.markdown(
    f"""
    <div class="interpretation">
        <strong>{ticker}</strong> recorded a total return of
        <strong>{total_return:.2%}</strong> during the selected period,
        with an average daily return of
        <strong>{mean_daily_return:.4%}</strong>.
        Daily volatility was
        <strong>{daily_volatility:.2%}</strong>, while annualized
        volatility was approximately
        <strong>{annualized_volatility:.2%}</strong>.
        The stock had
        <strong>{positive_days}</strong> positive trading days and
        <strong>{negative_days}</strong> negative trading days.
        The largest daily gain was
        <strong>{largest_daily_gain:.2%}</strong>, while the largest
        daily loss was
        <strong>{largest_daily_loss:.2%}</strong>.
        These figures provide a simple view of the stock's return and
        short-term price variation during the selected period.
    </div>
    """,
    unsafe_allow_html=True
)


# Display project information at the bottom of the page
st.markdown(
    """
    <div class="footer-text">
        Stock Price Data Visualization
        · Data sourced from Yahoo Finance through yfinance
        · Built with Python, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)