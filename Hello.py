import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from streamlit.logger import get_logger

df = pd.read_csv('./datasets/Processed_GlobalSuperstoreLite.csv')

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="Coursework | Dashboard",
    page_icon="./logo.svg"
)

def run():
    # App Title and description
    st.header("Individual Coursework | Hirushka Dias")
    st.write("This interactive dashboard explores sales data from a global retail superstore.")

    # Processed data table
    st.subheader("Processed Dataset")
    st.dataframe(df.style.set_properties(all_rows={'font-size': '11pt'}))

    # Graph 1: Sales per Category and Sub-Category

    # Group data, sort by category and sub-category
    df_grouped = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().unstack()

    # Interative stacked bar chart
    fig = go.Figure()
    data = [
        go.Bar(
            name=category,
            x=df_grouped.index,
            y=df_grouped.iloc[:, i],
        )
        for i, category in enumerate(df_grouped.columns)
    ]
    fig.add_traces(data)

    fig.update_layout(
        title='Sales per Category and Sub Category',
        xaxis_title='Category',
        yaxis_title='Sales ($)',
        barmode='stack',
        legend_title_text='Sub Category'  # Adjust legend title
    )

    fig.update_traces(marker_line_color='black', marker_line_width=0.5)  # Add bar border+

    st.plotly_chart(fig)

    # Graph 2: Sales per Product by Month

    # Extract month
    df['Month'] = pd.to_datetime(df['Order Date']).dt.month_name()
    # Order the months to be in order
    df['Month'] = pd.Categorical(df['Month'], categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    def plot_sales_by_product_month(year):
        # Filter data by the selected year
        df_filtered = df[pd.to_datetime(df['Order Date']).dt.year == year]

        # Pivot table to group sales by month and product
        pivot_table = pd.pivot_table(df_filtered, values='Sales', index='Month', columns='Product Name', aggfunc='sum')

        st.subheader(f"Sales per Product by Month (Year: {year})")
        st.bar_chart(pivot_table, height=500)

    # Year selector
    years = pd.to_datetime(df['Order Date']).dt.year.unique()
    selected_year = st.selectbox("Select Year to View Sales", years)

    # Plot sales for selected year
    plot_sales_by_product_month(selected_year)

    # Finding the top 5 products
    top_products = df.groupby(['Product Name', 'Category', 'Sub-Category'])['Sales'].sum().sort_values(ascending=False).head(5)

    # Display top 5 products
    st.subheader("Top 5 Selling Products")
    st.table(top_products)

if __name__ == "__main__":
    run()
