import pandas as pd
import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit.logger import get_logger

df = pd.read_csv('./datasets/Processed_GlobalSuperstoreLite.csv')

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="Coursework | Dashboard",
    page_icon="👋"
)

def run():
    st.write("# Individual Coursework | Hirushka Dias")

    ### Table 1 ###
    st.write("## Processed Dataset")
    # Shows the dataset as a table, but a smaller version of the st.table()
    df

    ### Graph 1 ###
    st.write("## No. of product sold per category and sub category")
    # Data is sorted by category and sub category
    df_grouped = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().unstack()

    # Creating a stacked plot
    data = [
        go.Bar(name=category, x=df_grouped.index, y=df_grouped.iloc[:, i])
        for i, category in enumerate(df_grouped.columns)
    ]
    fig = go.Figure(data=data)

    # Title and axis names
    fig.update_layout(
        title='Sales per Category and Sub Category',
        xaxis_title='Category',
        yaxis_title='Sales ($)',
        barmode='stack'  # Stack bars for subcategories within each category
    )

    # Display interactive chart
    st.plotly_chart(fig)

    ### Graph 2 ###
    st.write("## Product sales per month for selected year")
    # Extract the month from the 'Order Date' column
    df['Month'] = pd.to_datetime(df['Order Date']).dt.month_name()

    def plot_sales_by_product_month(df, year):
        st.write(f'### Sales per Product by Month (Year: {year})')
        # Filter data for the selected year
        df_filtered = df[pd.to_datetime(df['Order Date']).dt.year == year]

        # Create a pivot table to group sales by month and product
        pivot_table = pd.pivot_table(df_filtered, values='Sales', index='Month', columns='Product Name', aggfunc=sum)

        # Create a Streamlit bar chart
        st.bar_chart(pivot_table)

    # Get all unique years from the data
    years = pd.to_datetime(df['Order Date']).dt.year.unique()

    # Year selection dropdown
    selected_year = st.selectbox("Select Year to View Sales", years)

    # Bar chart for the selected year
    plot_sales_by_product_month(df.copy(), selected_year)

if __name__ == "__main__":
    run()
