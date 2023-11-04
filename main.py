import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(
        page_title="UAS Pemrograman Python",
        layout="wide",
    )

st.markdown(
    """
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write("""
         # Python Kelompok Sampurasun

         **Nama Anggota :**
         - Andreas Rhemadanu        <span style="float:right;">210103088</span>
         - Muhammad Hafid Krisna    <span style="float:right;">210103106</span>
         - Muhammad Yusuf           <span style="float:right;">210103110</span>
         - Rafif Rizqy Alfiansyah   <span style="float:right;">210103114</span>

         ## Dashboard UAS Pemrograman Python.
         """, unsafe_allow_html=True)

st.markdown("---")

st.text("")

def manga_yusuf():

    st.markdown("<h2 class='centered'>Best Selling Manga</h2>", unsafe_allow_html=True)

    # Baca data dari file CSV
    csv_file = "./data/manga.csv"
    df = pd.read_csv(csv_file)

    with st.expander("Tampilkan Dataframe"): 
        st.write(df)
        
    # Sidebar dengan filter berdasarkan Demografi
    st.sidebar.header("Filter Manga")
    selected_demographic = st.sidebar.selectbox("Demografi:", df['Demographic'].unique())

    # Urutkan data berdasarkan penjualan dalam jutaan kopi
    df_sorted = df.sort_values(by='Approximate sales in million(s)', ascending=False)

    # Terapkan filter berdasarkan Demografi
    filtered_df = df_sorted[df_sorted['Demographic'] == selected_demographic]

    # Ambil 15 manga teratas
    top_manga = filtered_df.head(15)

    # Buat visualisasi dengan Plotly Express
    fig = px.bar(top_manga, x='Approximate sales in million(s)', y='Manga series', orientation='h',
                labels={'Manga series': 'Judul Manga', 'Approximate sales in million(s)': 'Penjualan (jutaan kopi)'},
                color= 'Manga series')

    fig.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)  # Gaya grid pada sumbu X
    fig.update_traces(showlegend=False)  # Hilangkan legend

    # Tampilkan visualisasi dalam aplikasi Streamlit
    st.markdown("<h2 class='centered'>Peringkat Manga Terlaris berdasarkan Penjualan</h2>", unsafe_allow_html=True)

    st.plotly_chart(fig)

    st.text("")
    st.text("")

    # Pilih manga di sidebar
    st.sidebar.header("Detail Manga")
    selected_manga = st.sidebar.selectbox("Pilih Manga:", df["Manga series"])

    # Cari data manga yang sesuai dengan pilihan pengguna
    manga_data = df[df["Manga series"] == selected_manga]

    # Tampilkan data manga yang dipilih di bagian utama
    st.markdown("<h2 class='centered'>Detail Manga</h2>", unsafe_allow_html=True)

    if selected_manga:
        st.markdown(f'<h1 style= color:#FF5733;">{selected_manga}</h1>', unsafe_allow_html=True)
        st.markdown(f"**Penulis:** {manga_data['Author(s)'].values[0]}")
        st.markdown(f"**Penerbit:** {manga_data['Publisher'].values[0]}")
        st.markdown(f"**Demografik:** {manga_data['Demographic'].values[0]}")
        st.markdown(f"**Jumlah Volume:** {manga_data['No. of collected volumes'].values[0]}")
        st.markdown(f"**Tahun Serialisasi:** {manga_data['Serialized'].values[0]}")
        st.markdown(f"**Penjualan Total (jutaan kopi):** {manga_data['Approximate sales in million(s)'].values[0]}")
        st.markdown(f"**Penjualan Rata-rata per Volume (jutaan kopi):** {manga_data['Average sales per volume in million(s)'].values[0]}")
    else:
        st.warning("Pilih manga dari dropdown di sidebar.") 

    st.text("")
    st.text("")

    col1, col2, col3,col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Penjualan",
            value=df['Approximate sales in million(s)'].sum(),
        )
    with col2:
        st.metric(
            label="Jumlah Judul Manga",
            value=df['Manga series'].nunique(),
        )
    with col3:
        st.metric(
            label="Jumlah Penerbit",
            value=df['Publisher'].nunique(),
        )
    with col4:
        st.metric(
            label="Jumlah Demografi",
            value=df['Demographic'].nunique(),
        )

    st.text("")
    st.text("")

    data = df.groupby('Demographic')['Approximate sales in million(s)'].sum().reset_index()
    data = data.rename(columns={'Approximate sales in million(s)': 'Jumlah Penjualan (jutaan kopi)'})

    # Buat visualisasi dengan Plotly Express
    fig = px.pie(data, names='Demographic', values='Jumlah Penjualan (jutaan kopi)', hole=0.3,)

    # Tampilkan visualisasi dalam aplikasi Streamlit
    st.markdown("<h2 class='centered'>Distribusi Penjualan Manga berdasarkan Demografi</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Hitung jumlah manga terlaris yang diterbitkan oleh setiap penerbit
    popular_publishers = df.groupby('Publisher')['Manga series'].count().reset_index()

    # Temukan penerbit dengan jumlah manga terlaris terbanyak
    most_popular_publisher = popular_publishers[popular_publishers['Manga series'] == popular_publishers['Manga series'].max()]

    # Tampilkan chart batang untuk penerbit populer
    fig = px.bar(popular_publishers, x='Publisher', y='Manga series', 
                labels={'Publisher': 'Penerbit', 'Manga series': 'Jumlah Manga Terlaris'},
                color='Publisher')
    fig.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)

    st.markdown("<h2 class='centered'>Penerbit Manga Terlaris</h2>", unsafe_allow_html=True)

    st.plotly_chart(fig)

    st.text("")
    st.text("")

    # Cek jika terdapat beberapa penerbit dengan jumlah manga terlaris terbanyak
    if most_popular_publisher.shape[0] == 1:
        st.markdown("### Penerbit jumlah manga terlaris: ")
        st.write(f"**{most_popular_publisher['Publisher'].values[0]}**")
        st.markdown("### Jumlah manga terlaris")
        st.write(f"**{most_popular_publisher['Manga series'].values[0]}**")
    else:
        st.header("Terdapat beberapa penerbit dengan jumlah manga terlaris terbanyak:")
        for index, row in most_popular_publisher.iterrows():
            st.subheader(f"Penerbit: **{row['Publisher']}**")
            st.write(f"Jumlah manga terlaris yang mereka terbitkan: {row['Manga series']}")

    st.text("")
    st.text("")

    # Buat scatter plot untuk menggambarkan korelasi
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="No. of collected volumes", y="Average sales per volume in million(s)")

    # Tambahkan label sumbu
    plt.xlabel("Jumlah Volume yang Terkumpul")
    plt.ylabel("Penjualan Rata-Rata per Volume (juta)")

    # Tampilkan grafik
    plt.title("Korelasi antara Jumlah Volume dan Penjualan per Volume")
    plt.grid(True)
    plt.show()

    # Buat scatter plot untuk menggambarkan korelasi
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="No. of collected volumes", y="Average sales per volume in million(s)")

    # Tambahkan label sumbu
    plt.xlabel("Jumlah Volume yang Terkumpul")
    plt.ylabel("Penjualan Rata-Rata per Volume (juta)")

    # Tampilkan grafik
    plt.title("Korelasi antara Jumlah Volume dan Penjualan per Volume")
    plt.grid(True)

    # Tampilkan grafik menggunakan Seaborn
    plt.show()

    st.text("")
    st.text("")

    # Tambahkan judul menggunakan Streamlit
    st.markdown("<h2 class='centered'>Perbandingan Manga</h2>", unsafe_allow_html=True)

    # Pilihan untuk jenis perbandingan
    comparison_type = st.selectbox("Pilih jenis perbandingan:", ["Penjualan per Volume", "Jumlah Volume Terkumpul"])

    if comparison_type == "Penjualan per Volume":
        # Sortir data berdasarkan penjualan per volume
        sorted_df = df.sort_values(by="Average sales per volume in million(s)", ascending=False)
        
        # Ambil 15 manga teratas
        top_15_sales = sorted_df.head(15)
        
        # Buat grafik perbandingan penjualan per volume menggunakan Plotly
        fig = px.bar(
            top_15_sales,
            x="Manga series",
            y="Average sales per volume in million(s)",
            title="Top 15 Manga berdasarkan Penjualan per Volume",
        )
        
        st.plotly_chart(fig)

    elif comparison_type == "Jumlah Volume Terkumpul":
        # Sortir data berdasarkan jumlah volume yang terkumpul
        sorted_df = df.sort_values(by="No. of collected volumes", ascending=False)
        
        # Ambil 15 manga teratas
        top_15_volumes = sorted_df.head(15)
        
        # Buat grafik perbandingan jumlah volume yang terkumpul menggunakan Plotly
        fig = px.bar(
            top_15_volumes,
            x="Manga series",
            y="No. of collected volumes",
            title="Top 15 Manga berdasarkan Jumlah Volume Terkumpul",
        )
        
        st.plotly_chart(fig)

    st.text("")
    st.text("")


    # Pisahkan manga lama dan manga baru berdasarkan tahun serialisasi
    current_year = 2023
    df['Start Year'] = df['Serialized'].str.extract(r'(\d{4})').astype(float)
    df['Duration'] = current_year - df['Start Year']

    # Bagi data menjadi manga lama dan manga baru
    manga_lama = df[df['Duration'] >= 10]  # Misalnya, manga yang sudah berumur lebih dari 10 tahun dianggap lama
    manga_baru = df[df['Duration'] < 10]

    # Hitung penjualan rata-rata per volume
    penjualan_rata_rata_lama = manga_lama['Approximate sales in million(s)'].sum() / manga_lama['No. of collected volumes'].sum()
    penjualan_rata_rata_baru = manga_baru['Approximate sales in million(s)'].sum() / manga_baru['No. of collected volumes'].sum()

    # Tampilkan hasil sebagai metric
    st.markdown("<h2 class='centered'>Perbandingan Penjualan Per Volume</h2>", unsafe_allow_html=True)
    st.write("manga yang sudah berumur lebih dari 10 tahun dianggap lama")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Manga Lama",
            value=penjualan_rata_rata_lama,
            delta=penjualan_rata_rata_lama - penjualan_rata_rata_baru
        )

    with col2:
        st.metric(
            label="Manga Baru",
            value=penjualan_rata_rata_baru,
            delta=penjualan_rata_rata_baru - penjualan_rata_rata_lama
        )

def ml_rhema():

    st.title("Data Mobile Legends")
    st.header("Data Mobile Legends")

    # Baca dataset
    dataset = pd.read_csv('./data/mlhero.csv')

    # Menampilkan dataset (Opsional)
    st.write(dataset)

    # Membuat grafik garis dengan Plotly Express
    fig_line = px.line(dataset, x='Name', y='Hp', title='Grafik Hero sesuai dengan hp')
    st.plotly_chart(fig_line)

    # Membuat grafik diagram batang dengan Plotly Express
    fig_bar = px.bar(dataset, x='Name', y='Mana', title='Grafik diagram batang dengan komposisi mana')
    st.plotly_chart(fig_bar)

    # Membuat grafik diagram area dengan Plotly Express
    fig_area = px.area(dataset, x='Name', y='Lane', title='Grafik Area: ROLE HERO masing-masing')
    st.plotly_chart(fig_area)

    # Membuat grafik diagram kotak dengan Plotly Express
    fig_box = px.box(dataset, x='Lane', y='Mana', title='Diagram Kotak: Berdasarkan jumlah mana awal dari role hero')
    st.plotly_chart(fig_box)


def krisna():
    st.title('Visualisasi Produksi Beras')
    file_path = "data/rice.csv"
    df = pd.read_csv(file_path)

    st.write("Data Produksi Beras:")
    st.write(df)

    with st.sidebar:
        st.header('Pilihan Data')
        selected_chart = st.selectbox('Pilih Jenis Grafik', ['Bar Chart', 'Pie Chart', 'Area Chart'])

    if selected_chart == 'Bar Chart':
        st.subheader("Grafik Produksi Beras per Provinsi (Bar Chart):")
        provinsi_list = df['Provinsi'].unique()
        selected_provinsi = st.multiselect('Pilih Provinsi', provinsi_list, default=[])
        if len(selected_provinsi) == 0:
            st.plotly_chart(px.bar(df, x='Provinsi', y='Production.(ton)', labels={'Provinsi': 'Provinsi', 'Production.(ton)': 'Produksi (ton)'},
                    title='Produksi Beras per Provinsi'))
        else:
            filtered_data = df[df['Provinsi'].isin(selected_provinsi)]
            st.plotly_chart(px.bar(filtered_data, x='Provinsi', y='Production.(ton)', labels={'Provinsi': 'Provinsi', 'Production.(ton)': 'Produksi (ton)'},
                    title='Produksi Beras per Provinsi'))

    elif selected_chart == 'Pie Chart':
        st.subheader("Grafik Pie Chart Produksi Beras per Provinsi:")
        selected_provinsi = st.multiselect('Pilih Provinsi', df['Provinsi'].unique(), default=[])
        if len(selected_provinsi) == 0:
            st.plotly_chart(px.pie(df, values='Production.(ton)', names='Provinsi', title='Produksi Beras per Provinsi', hole=0.2))
        else:
            fig = go.Figure(data=[go.Pie(labels=df['Provinsi'], hole=0.2, values=df['Production.(ton)'])])
            fig.update_traces(textposition='inside')
            st.plotly_chart(fig)

    else:
        st.subheader("Area Chart Produksi Beras per Provinsi:")
        provinsi_list = df['Provinsi'].unique()
        selected_provinsi = st.multiselect('Pilih Provinsi', provinsi_list, default=[])
        if len(selected_provinsi) == 0:
            st.plotly_chart(px.area(df, x='Provinsi', y='Production.(ton)', title='Produksi Beras per Provinsi'))
        else:
            filtered_data = df[df['Provinsi'].isin(selected_provinsi)]
            st.plotly_chart(px.area(filtered_data, x='Provinsi', y='Production.(ton)', title='Produksi Beras per Provinsi'))

def rafif():
    st.title("Data Customer Shopping")
    st.header("Data Customer Shopping")

    # Baca dataset
    dataset = pd.read_csv('./data/shop.csv')

    # Menampilkan dataset (Opsional)
    st.write(dataset)

    # Membuat grafik diagram batang dengan Plotly Express
    fig_bar = px.bar(dataset, x='quantity', y='category', title='Grafik batang: Komposisi qualitas dan kategori')
    st.plotly_chart(fig_bar)

    # Membuat grafik diagram area dengan Plotly Express
    fig_area = px.area(dataset, x='price', y='age', title='Grafik Area: dari harga dan rata-rata usia')
    st.plotly_chart(fig_area)

    # Membuat grafik diagram kotak dengan Plotly Express
    fig_box = px.box(dataset, x='category', y='price', title='Diagram Kotak: diambil dari category dan harga')
    st.plotly_chart(fig_box)
    color_discrete_sequence=['red']

def main():
    st.text("")

if __name__ == '__main__':
    main()
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Manga", "ML Hero", "Rice", "Shop"],
            icons=["bi-book", "bi-phone", "bi-basket", "bi-cart"],
            default_index=0,
        )

    if selected == "Manga":
        manga_yusuf()
    elif selected == "ML Hero":
        ml_rhema()
    elif selected == "Rice":
        krisna()
    elif selected == "Shop":
        rafif()
