import warnings
import os
import pandas as pd
from streamlit_option_menu import option_menu
from utils import *

warnings.simplefilter("ignore")
st.set_page_config("Streamlit Dashboard", page_icon=':bar_chart:', layout='wide')

with st.sidebar:
    st.write(
        """
        <style>
        img {
            margin-top: -35px;
            width: 210px;
            margin-left: 50px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.image("logo.png")
    select = option_menu(
        menu_title="Streamlit Dashboard",
        options=["Home", "About", "Visualization", "How to Use?"],
        icons=["house", "file-earmark", "bar-chart"],
        default_index=0,
        styles={
            "menu-title": {'font-size': '20px',
                           'margin-bottom': '10px',
                           "font-weight": "bold"
                           },
            "container": {"background-color": "transparent"},
            "icon": {"font-size": "20px"},
            "nav-link": {
                "font-size": "17px",
                "font-weight": "normal",
                "--hover-color": "rgba(255, 0, 0, 0.2)"
            }
        }
    )

if select == 'Home':
    df = upload_file()

if select == 'About':
    st.title(":spiral_note_pad: Data Information")
    st.markdown("##")

    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        display_data_info(df)

    elif os.path.exists("data.xlsx"):
        df = pd.read_excel("data.xlsx")
        display_data_info(df)
    else:
        st.info("Please upload a CSV or Excel file", icon="ℹ️")

if select == 'Visualization':

    st.title(":chart: Dashboard")
    st.markdown("##")

    if os.path.exists("data.csv"):
        df = pd.read_excel("data.xlsx")
        df = filter_date_range(df)
        filtered_df = filter_data(df)
        display_category_region_sales_chart(filtered_df)
        display_category_region_data_summary(filtered_df)
        display_time_series_analysis(filtered_df)
        display_hierarchical_sales_chart(filtered_df)
        display_segment_category_wise_sales_chart(filtered_df)
        display_monthly_subcategory_sales_summary(filtered_df)
        display_data_table(filtered_df)

    elif os.path.exists("data.xlsx"):
        df = pd.read_excel("data.xlsx")
        df = filter_date_range(df)
        filtered_df = filter_data(df)
        display_category_region_sales_chart(filtered_df)
        display_category_region_data_summary(filtered_df)
        display_time_series_analysis(filtered_df)
        display_hierarchical_sales_chart(filtered_df)
        display_segment_category_wise_sales_chart(filtered_df)
        display_monthly_subcategory_sales_summary(filtered_df)
        display_data_table(filtered_df)

    else:
        st.info("Please upload a CSV or Excel file", icon="ℹ️")

if select == 'How to Use?':
    usage_guide()
