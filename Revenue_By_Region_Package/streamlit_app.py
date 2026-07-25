
import streamlit as st
import pandas as pd

regions = [
    "Maharashtra","Karnataka","Tamil Nadu","Delhi NCR",
    "Gujarat","West Bengal","Uttar Pradesh","Rajasthan"
]

revenue = [1875,1620,1480,1325,1180,1050,980,860]

df = pd.DataFrame({
    "Region": regions,
    "Revenue": revenue
})

st.set_page_config(page_title="Revenue by Region", layout="wide")
st.title("Revenue by Region")

st.bar_chart(df.set_index("Region"))
st.dataframe(df)
