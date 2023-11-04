import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.title('Visualisasi Produksi Beras')

    # Membaca data dari file CSV
    file_path = "data/rice.csv"
    df = pd.read_csv(file_path)

    st.write("Data Produksi Beras:")
    st.write(df)

    st.sidebar.header('Pilihan Data')
    selected_chart = st.sidebar.selectbox('Pilih Jenis Grafik', ['Bar Chart', 'Pie Chart', 'Area Chart'])

    if selected_chart == 'Bar Chart':
        st.subheader("Grafik Produksi Beras per Provinsi (Bar Chart):")
        provinsi_list = df['Provinsi'].unique()
        selected_provinsi = st.sidebar.multiselect('Pilih Provinsi', provinsi_list, default=[])
        if len(selected_provinsi) == 0:
            st.plotly_chart(px.bar(df, x='Provinsi', y='Production.(ton)', labels={'Provinsi': 'Provinsi', 'Production.(ton)': 'Produksi (ton)'},
                     title='Produksi Beras per Provinsi'))
        else:
            filtered_data = df[df['Provinsi'].isin(selected_provinsi)]
            st.plotly_chart(px.bar(filtered_data, x='Provinsi', y='Production.(ton)', labels={'Provinsi': 'Provinsi', 'Production.(ton)': 'Produksi (ton)'},
                     title='Produksi Beras per Provinsi'))

    elif selected_chart == 'Pie Chart':
        st.subheader("Grafik Pie Chart Produksi Beras per Provinsi:")
        selected_provinsi = st.sidebar.multiselect('Pilih Provinsi',df['Provinsi'].unique(), default=[])
        if len(selected_provinsi) == 0:
            st.plotly_chart(px.pie(df, values='Production.(ton)', names='Provinsi', title='Produksi Beras per Provinsi',hole=0.2))
        else:
            fig = go.Figure(data=[go.Pie(labels=df['Provinsi'],hole=0.2, values=df['Production.(ton)'])])
            fig.update_traces(textposition='inside')
            st.plotly_chart(fig)

    else:
        st.subheader("Area Chart Produksi Beras per Provinsi:")
        provinsi_list = df['Provinsi'].unique()
        selected_provinsi = st.sidebar.multiselect('Pilih Provinsi', provinsi_list, default=[])
        if len(selected_provinsi) == 0:
            st.plotly_chart(px.area(df, x='Provinsi', y='Production.(ton)', title='Produksi Beras per Provinsi'))
        else:
            filtered_data = df[df['Provinsi'].isin(selected_provinsi)]
            st.plotly_chart(px.area(filtered_data, x='Provinsi', y='Production.(ton)', title='Produksi Beras per Provinsi'))

if __name__ == '__main__':
    main()
