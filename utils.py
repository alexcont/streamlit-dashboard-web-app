import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


def upload_file():
    st.title(":house: Home")
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

    data = None

    if uploaded_file is not None:
        progress_bar = st.progress(0)

        with st.spinner("File is uploading..."):
            for i in range(100):
                time.sleep(0.1)
                progress_bar.progress(i + 1)

        if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            data = pd.read_excel(uploaded_file, index_col=None)
            st.success("Your file is uploaded", icon="✅")
            st.divider()
            st.write("### First 5 Rows of the Data")
            st.dataframe(data.head())
            st.divider()
            st.write("### Last 5 Rows of the Data")
            st.dataframe(data.tail())
            data.to_excel("data.xlsx", index=False)
        elif uploaded_file.type == 'text/csv':
            data = pd.read_csv(uploaded_file, index_col=None)
            st.success("Your file is uploaded", icon="✅")
            st.divider()
            st.write("### First 5 Rows of the Data")
            st.dataframe(data.head())
            st.divider()
            st.write("### Last 5 Rows of the Data")
            st.dataframe(data.tail())
            data.to_csv("data.csv", index=False)
        else:
            st.warning("Unsupported file type")
    else:
        st.info("You must upload a CSV or Excel file", icon="ℹ️")

    return data


def display_data_info(dataframe):
    st.markdown("##")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        checkbox1 = st.checkbox("Shape")

    with col2:
        checkbox2 = st.checkbox("Duplicate Value")

    with col3:
        checkbox3 = st.checkbox("Null Values")

    with col4:
        checkbox4 = st.checkbox("Columns")

    st.markdown("#")
    col_first, col_second = st.columns(2)

    with col_first:
        if checkbox1:
            st.write("Dataframe Shape")
            st.success(dataframe.shape)
        if checkbox2:
            st.write("Dataframe Duplicate Values")
            if dataframe.duplicated().sum() > 0:
                st.warning(dataframe.duplicated().sum(), icon="⚠️")
            else:
                st.success("0", icon="✅")
        if checkbox3:
            st.write("Dataframe Null Values")
            if dataframe.isnull().any().any():
                for col in dataframe.columns:
                    if dataframe[col].isnull().sum() > 0:
                        st.warning(f"{col}: {dataframe[col].isnull().sum()}", icon="⚠️")
            else:
                st.success(dataframe.isnull().sum().sum(), icon="✅")

    with col_second:
        if checkbox4:
            st.write("Data Columns")
            st.table(dataframe.columns)

    st.markdown("---")


def filter_date_range(dataframe):
    div1, div2 = st.columns((2))
    dataframe["Order Date"] = pd.to_datetime(dataframe["Order Date"])

    start_date = pd.to_datetime(dataframe["Order Date"]).min()
    end_date = pd.to_datetime(dataframe["Order Date"]).max()

    with div1:
        date1 = pd.to_datetime(st.date_input("Start Date", start_date))

    with div2:
        date2 = pd.to_datetime(st.date_input("End Date", end_date))

    dataframe = dataframe[(dataframe["Order Date"] >= date1) & (dataframe["Order Date"] <= date2)].copy()

    return dataframe


def filter_data(dataframe):
    with st.expander("Filter Settings"):
        region = st.multiselect("Pick your Region", dataframe["Region"].unique())
        if not region:
            df2 = dataframe.copy()
        else:
            df2 = dataframe[dataframe["Region"].isin(region)]

        state = st.multiselect("Pick the State", df2["State"].unique())
        if not state:
            df3 = df2.copy()
        else:
            df3 = df2[df2["State"].isin(state)]

        city = st.multiselect("Pick the City", df3["City"].unique())

    if not region and not state and not city:
        filtered_df = dataframe
        st.info("The entire dataset is presented visually. "
                "You can filter it as you wish in the filter settings section.", icon="ℹ️")
    elif not state and not city:
        filtered_df = dataframe[dataframe["Region"].isin(region)]
    elif not region and not city:
        filtered_df = dataframe[dataframe["State"].isin(state)]
    elif state and city:
        filtered_df = df3[dataframe["State"].isin(state) & df3["City"].isin(city)]
    elif region and city:
        filtered_df = df3[dataframe["Region"].isin(region) & df3["City"].isin(city)]
    elif region and state:
        filtered_df = df3[dataframe["Region"].isin(region) & df3["State"].isin(state)]
    elif city:
        filtered_df = df3[df3["City"].isin(city)]
    else:
        filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

    st.divider()

    return filtered_df


def display_category_region_sales_chart(filtered_dataframe):
    div1, div2 = st.columns(2)

    with div1:
        st.subheader("Category & Sales")
        category_df = filtered_dataframe.groupby(by=["Category"], as_index=False)["Sales"].sum()
        fig = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                     color="Category", template="plotly", color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_traces(
            texttemplate='%{text}',
            textfont=dict(
                family="Arial",
                size=14,
                color="black"
            )
        )
        st.plotly_chart(fig, use_container_width=True, height=200, width=200)

    with div2:
        st.subheader("Region & Sales")
        fig = px.pie(filtered_dataframe, values="Sales", names="Region", hole=0.5,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(text=filtered_dataframe["Region"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)


def display_category_region_data_summary(filtered_dataframe):
    column1, column2 = st.columns(2)

    with column1:
        with st.expander("Category Data Summary"):
            st.write(filtered_dataframe.style.background_gradient(cmap="YlOrRd"))
            csv = filtered_dataframe.to_csv(index=False).encode('utf-8')

            st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    with column2:
        with st.expander("Region Data Summary"):
            region = filtered_dataframe.groupby(by="Region", as_index=False)["Sales"].sum()
            st.write(region.style.background_gradient(cmap="PuBuGn"))
            csv = region.to_csv(index=False).encode('utf-8')

            st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    st.markdown("---")


def display_time_series_analysis(filtered_dataframe):
    filtered_dataframe["month_year"] = filtered_dataframe["Order Date"].dt.to_period("M")

    st.subheader('Time Series Analysis')

    linechart = pd.DataFrame(
        filtered_dataframe.groupby(filtered_dataframe["month_year"].dt.strftime("%Y - %m"))["Sales"].sum()
    ).reset_index()

    fig2 = px.line(
        linechart,
        x="month_year",
        y="Sales",
        labels={"Sales": "Amount"},
        height=400,
        width=800,
        template="plotly",
        line_shape='spline',
        color_discrete_sequence=px.colors.qualitative.Set1,
    )

    fig2.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales Amount",
        title="Monthly Sales Trends",
        title_x=0.5,
        font=dict(size=14),
        margin=dict(l=0, r=0, b=0, t=30),
    )

    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("View Data of TimeSeries:"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')

    st.markdown("---")


def display_hierarchical_sales_chart(filtered_dataframe):
    st.subheader("Hierarchical Sales Analysis")
    fig3 = px.treemap(
        filtered_dataframe,
        path=["Region", "Category", "Sub-Category"],
        values="Sales",
        hover_data=["Sales"],
        color="Sub-Category",
        color_discrete_sequence=px.colors.qualitative.Set3_r
    )
    fig3.update_layout(width=800, height=650)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")


def display_segment_category_wise_sales_chart(filtered_dataframe):
    chart1, chart2 = st.columns((2))

    with chart1:
        st.subheader('Segment Wise Sales')
        fig = px.pie(
            filtered_dataframe,
            values="Sales",
            names="Segment",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set2_r,
            hole=0.4,
        )
        max_percentage_index = filtered_dataframe["Sales"].idxmax()
        pull_values = [0.2 if i != max_percentage_index else 0.4 for i in
                       range(len(filtered_dataframe))]
        fig.update_traces(textinfo="percent+label", pull=pull_values, textposition="inside")
        st.plotly_chart(fig, use_container_width=True)

    with chart2:
        st.subheader('Category Wise Sales')
        fig = px.pie(
            filtered_dataframe,
            values="Sales",
            names="Category",
            template="gridon",
            color_discrete_sequence=px.colors.qualitative.Set1_r,
            hole=0.4,
        )
        max_percentage_index = filtered_dataframe["Category"].idxmax()
        pull_values = [0.2 if i != max_percentage_index else 0.4 for i in
                       range(len(filtered_dataframe))]
        fig.update_traces(textinfo="percent+label", pull=pull_values, textposition="inside")
        st.plotly_chart(fig, use_container_width=True)


def display_monthly_subcategory_sales_summary(filtered_dataframe):
    st.subheader("Monthly Sub-Category Sales Analysis")
    with st.expander("Summary Table"):
        df_sample = filtered_dataframe[0:10][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Monthly Sub-Category Sales Data Table")
        filtered_dataframe["month"] = filtered_dataframe["Order Date"].dt.month_name()
        sub_category_Year = pd.pivot_table(data=filtered_dataframe, values="Sales", index=["Sub-Category"],
                                           columns="month")
        st.write(sub_category_Year.style.background_gradient(cmap="Blues"))


def display_data_table(filtered_dataframe):
    with st.expander("View Data"):
        st.write(filtered_dataframe.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))


def usage_guide():
    st.markdown(
        """
        <style>
        .user-guide-title {
            font-size: 35px;
            font-weight: bold;
            margin-left: 70px;
        }
        .home-guide-text-home {
        font-size: 25px;
        font-weight: bold;
        margin-left: 80px;
        }
        .home-guide-text {
            font-size: 16px;
            margin-bottom: 20px;
            margin-left: 110px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="user-guide-title">📖 Welcome to User Guide</p>', unsafe_allow_html=True)
    st.markdown("#")
    st.markdown('<p class="home-guide-text-home">1. Home</p>', unsafe_allow_html=True)
    st.markdown('<p class="home-guide-text">When you run the application, the main page will appear first. '
                'On this page, you need to upload the dataset provided to you.</p>', unsafe_allow_html=True)
    st.markdown('<p class="home-guide-text">- To begin, select the "Home" tab from the menu.</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="home-guide-text">- You\'ll see an option to upload your data. Click on it.</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="home-guide-text">- Choose a CSV or Excel file containing your data and upload it.</p>',
                unsafe_allow_html=True)
    st.markdown("#")

    home_image = "home_page.png"
    st.image(home_image, caption='Home Page', width=800)

    st.divider()

    st.markdown(
        """
        <style>
        .about-guide-text-about {
        font-size: 25px;
        font-weight: bold;
        margin-left: 80px;
        }
        .about-guide-text {
            font-size: 16px;
            margin-bottom: 20px;
            margin-left: 110px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="about-guide-text-about">2. About</p>', unsafe_allow_html=True)
    st.markdown('<p class="about-guide-text">- The system will check if the data file '
                '("data.csv" or "data.xlsx") exists in the directory. ', unsafe_allow_html=True)
    st.markdown('<p class="about-guide-text">- If found, it will display information about the data, '
                'including shape, duplicate values, null values, and column names.</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="about-guide-text">- If the data file doesn\'t exist, '
                'you will receive a message prompting you to upload a CSV or Excel file.</p>',
                unsafe_allow_html=True)

    st.markdown("#")

    about_image = "about_page.png"
    st.image(about_image, caption='About Page', width=800)

    st.divider()

    st.markdown(
        """
        <style>
        .visualize-guide-text-visualize {
        font-size: 25px;
        font-weight: bold;
        margin-left: 80px;
        }
        .visualize-guide-text {
            font-size: 16px;
            margin-bottom: 20px;
            margin-left: 110px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="visualize-guide-text-visualize">3. Visualization</p>', unsafe_allow_html=True)
    st.markdown('<p class="visualize-guide-text">- The system will check if the data file '
                '("data.csv" or "data.xlsx") exists in the directory. ', unsafe_allow_html=True)
    st.markdown('<p class="visualize-guide-text">- If found, it will allow you to apply '
                'filters to the data based on region, state, and city.</p>', unsafe_allow_html=True)
    st.markdown('<p class="visualize-guide-text">- After applying filters, various interactive '
                'visualizations will be displayed, including category and region sales charts, '
                'data summaries, time series analysis, hierarchical sales charts, and more.</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="visualize-guide-text">- You can explore and analyze the data'
    'visually through these charts and tables. </p> ', unsafe_allow_html=True)

    st.markdown("#")

    visualize_image = "visualize_page.png"
    st.image(visualize_image, caption='Visualization Page', width=800)
