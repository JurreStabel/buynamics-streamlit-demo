import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title='Buynamics dashboard',
    page_icon='assets/WTP-icon_buynamics.png',
    layout='centered',
    initial_sidebar_state='collapsed'
)

with st.sidebar:
    st.image(image='assets/WTP-logo-buynamics-oranje-KB.svg', width=120)
    st.title('Menu')
    option = st.selectbox("Options:", ['Start', 'Instructions', 'Analyze data', 'Visualize data'])

if option == 'Start':
    st.markdown(
        """
        <h1 style='text-align: center;'>
            Welcome to <span style='color: #FF6F00;'>Buynamics</span> dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])  
    with col2:
        st.image('assets/WTP-logo-buynamics-oranje-KB.svg', width=360)

elif option == 'Instructions':
    st.title(':orange[Instructions]')
    st.divider()
    st.subheader('1. Select analyze data from the sidebar')
    st.divider()
    st.subheader('2. Upload a csv file with data')
    st.divider()
    st.subheader('3. Select visualize data to see charts')
    st.divider()

elif option == 'Analyze data':
    st.title(':orange[Upload a file to start data analysis (.csv only)]')
    file = st.file_uploader('Please upload a csv.', type='csv')

    if file:
        st.success('File uploaded successfully')
        df = pd.read_csv(file)

        os.makedirs('upload_folder', exist_ok=True)
        save_path = os.path.join('upload_folder', 'data.csv')

        df.to_csv(save_path, index=False)

        st.dataframe(df.head())

elif option == 'Visualize data':
    st.title(':orange[Data Visualization]')
    st.subheader('Uploaded dataset: ')
    df = pd.read_csv('upload_folder\data.csv')

    df['Date'] = pd.to_datetime(df['Date'])
    st.dataframe(df.head())

    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()

    date_range = st.date_input("Select a date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    if isinstance(date_range, tuple) and len(date_range) == 2:
        filtered_df = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]

        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        unique_symbols = filtered_df['Symbol'].unique()

        st.subheader("Select price metrics to display:")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            show_open = st.checkbox("Open", value=False)
        
        with col2:
            show_high = st.checkbox("High", value=False)

        with col3:
            show_low = st.checkbox("Low", value=False)

        with col4:
            show_close = st.checkbox("Close", value=False)

        selected_metrics = []
        if show_open: selected_metrics.append("Open")
        if show_high: selected_metrics.append("High")
        if show_low: selected_metrics.append("Low")
        if show_close: selected_metrics.append("Close")

        if not selected_metrics:
            st.warning("Please select at least one metric to display.")

        if selected_metrics:
            for symbol in unique_symbols:
                symbol_df = filtered_df[filtered_df['Symbol'] == symbol].copy()
                symbol_df.set_index('Date', inplace=True)
                chart_data = symbol_df[selected_metrics]

                st.subheader(f"Price Movement for {symbol}")
                st.line_chart(chart_data)
