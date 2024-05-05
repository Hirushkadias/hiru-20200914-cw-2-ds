import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from streamlit.logger import get_logger

df = pd.read_csv('./datasets/Processed_GlobalSuperstoreLite.csv')
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

    st.write("## No. of product sold per category")
    # Efficient data preparation using pandas
    df_grouped = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().unstack()

    # Create stacked bar chart with Plotly (using dictionary comprehension)
    data = [
        go.Bar(name=category, x=df_grouped.index, y=df_grouped.iloc[:, i])
        for i, category in enumerate(df_grouped.columns)
    ]
    fig = go.Figure(data=data)

    # Update layout with titles and legend
    fig.update_layout(
        title='Sales by Category and Sub Category',
        xaxis_title='Category',
        yaxis_title='Sales ($)',
        barmode='stack'  # Stack bars for subcategories within each category
    )

    # Display interactive chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    run()
