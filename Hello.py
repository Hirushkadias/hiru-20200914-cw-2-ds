import pandas as pd
import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit.logger import get_logger

df = pd.read_csv('./datasets/Processed_GlobalSuperstoreLite.csv')
# if all(df['Order Date'].str.contains('-')):  # Check for hyphens in all dates
#     datetime_obj = datetime.datetime.strptime(df['Order Date'], '%Y-%m-%d')
#     df['Order Date'] = datetime_obj.strftime('%d/%m/%Y')
categories = df['Category'].to_numpy()
sub_category = df['Sub-Category'].to_numpy()
sales = df['Sales'].to_numpy()

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="Coursework | Dashboard",
    page_icon="👋"
)

def run():
    st.write("# Hello World!!!")

    st.write("## Processed Dataset")
    # Shows the dataset as a table, but a smaller version of the st.table()
    df

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

    # st.write("## Chart 2")
    # # Year selection dropdown
    # selected_year = st.selectbox("Select Year", df['Order Date'].dt.year.unique())

    # # Filter data for selected year
    # df_filtered = df[df['Order Date'].dt.year == selected_year]

    # # Prepare data for bar chart (assuming 'products sold' is a count or sum)
    # df_grouped = df_filtered.groupby([df_filtered['Order Date'].dt.month_name(), 'Category'])['Sales'].sum().unstack()
    # month_names = df_grouped.index.to_list()
    # categories = df_grouped.columns.to_list()

    # # Create stacked bar chart with Plotly
    # data = []
    # for i, category in enumerate(categories):
    #     data.append(go.Bar(name=category, x=month_names, y=df_grouped.iloc[:, i]))
    # fig = go.Figure(data=data)

    # # Update layout with titles and legend
    # fig.update_layout(
    #     title=f'Products Sold per Month (Year: {selected_year})',
    #     xaxis_title='Month',
    #     yaxis_title='Products Sold',
    #     barmode='stack'  # Stack bars for categories within each month
    # )

    # # Display interactive chart in Streamlit
    # st.plotly_chart(fig)


if __name__ == "__main__":
    run()
