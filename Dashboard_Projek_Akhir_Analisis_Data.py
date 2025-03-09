import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
st.write(
    """
    # Dashboard Projek Akhir
    Analisis data dengan Phyton
    """
)
day_df = pd.read_csv(r"C:/Users/Lenovo/Documents/Kuliah/Semester 6/Dicoding/day.csv")

def create_BarPenyewaSepeda_SetiapMusim_df(df):
    plt.figure(figsize=(8,5))
    sns.barplot(x="season", y="cnt", data = day_df, estimator=sum)

    plt.xticks(ticks=[0, 1, 2, 3], labels=["Dingin", "Panas", "Gugur", "Semi"])

    plt.xlabel("Musim")
    plt.ylabel("Total Penyewaan Sepeda")
    plt.title("Total Penyewaan Sepeda di Setiap Musim")
    plt.show()

def create_BoxPenyewaSepeda_SetiapMusim_df(df):
    plt.figure(figsize=(8,5))
    sns.boxplot(x="season", y="cnt", data=day_df)

    plt.xticks(ticks=[0, 1, 2, 3], labels=["Dingin", "Panas", "Gugur", "Semi"])
    plt.xlabel("Musim")
    plt.ylabel("Penyewaan Sepeda")
    plt.title("Distribusi Penyewaan Sepeda di Setiap Musim")
    plt.show()

def create_ScatterWindspeed_df(df):
    # Filter data untuk hari kerja
    working_day_df = df[df['workingday'] == 1]

    # Scatter plot
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="windspeed", y="cnt", data=working_day_df, alpha=0.5)
    
    # Tambahkan judul dan label
    plt.title("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda pada Hari Kerja")
    plt.xlabel("Kecepatan Angin")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    
    # Tampilkan plot
    plt.show()

def create_BoxWindspeed_df(df):
    working_day_df = df[df['workingday'] == 1]
    bins = [0.13, 0.18, 0.23, 0.30]  
    labels = ["Rendah", "Sedang", "Tinggi"] 
    working_day_df.loc[:, "wind_category"] = pd.cut(working_day_df["windspeed"], bins=bins, labels=labels).astype("category")

    # Box plot
    plt.figure(figsize=(8,5))
    sns.boxplot(x="wind_category", y="cnt", data=working_day_df)

    plt.xlabel("Kategori Kecepatan Angin")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    plt.title("Distribusi Penyewaan Sepeda Berdasarkan Kecepatan Angin pada Hari Kerja")
    plt.show()

def create_StackedHoliday_df(df):
    holiday_only = day_df[day_df["holiday"] == 1]

    # Menghitung total penyewaan untuk hari libur
    total_casual = holiday_only["casual"].sum()
    total_registered = holiday_only["registered"].sum()

    # Membuat Stacked Bar Chart
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.bar("Hari Libur", total_casual, label="Casual", color="red")
    ax.bar("Hari Libur", total_registered, bottom=total_casual, label="Registered", color="blue")

    # Menambahkan label dan judul
    ax.set_ylabel("Total Penyewaan Sepeda")
    ax.set_title("Perbandingan Penyewaan Sepeda pada Hari Libur")
    ax.legend()

    # Menampilkan plot
    plt.show()

def create_ViolinHoliday_df(df):
    holiday_only = day_df[day_df["holiday"] == 1]

    # Mengubah data ke dalam format yang sesuai untuk seaborn
    violin_df = holiday_only.melt(id_vars=["holiday"], value_vars=["casual", "registered"],
                              var_name="User Type", value_name="Total Penyewaan")

    # Membuat Violin Plot
    plt.figure(figsize=(6, 5))
    sns.violinplot(x="User Type", y="Total Penyewaan", data=violin_df, palette={"casual": "red", "registered": "blue"})

    # Menambahkan judul dan label
    plt.title("Distribusi Penyewaan Sepeda pada Hari Libur")
    plt.xlabel("Jenis Pengguna")
    plt.ylabel("Jumlah Penyewaan Sepeda")

    # Menampilkan plot
    plt.show()

days_df = pd.read_csv(r"C:/Users/Lenovo/Documents/Kuliah/Semester 6/Dicoding/days_df.csv") 

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    
    min_date = days_df["dteday"].min()
    max_date = days_df["dteday"].max()

with st.sidebar:
    st.header("Penyewaan Sepeda")
    # Menambahkan gambar
    st.image("C:/Users/Lenovo/Documents/Kuliah/Semester 6/Dicoding/Penyewaan sepeda.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    main_df = days_df[(days_df["dteday"] >= str(start_date)) & 
                (days_df["dteday"] <= str(end_date))]
    
    BarPenyewaSepeda_SetiapMusim_df = create_BarPenyewaSepeda_SetiapMusim_df
    BoxPenyewaSepeda_SetiapMusim_df = create_BoxPenyewaSepeda_SetiapMusim_df
    ScatterWindspeed_df = create_ScatterWindspeed_df
    BoxWindspeed_df = create_BoxWindspeed_df
    StackeHoliday_df = create_StackedHoliday_df
    ViolinHoliday_df = create_ViolinHoliday_df
    
st.header("🚲 Dashboard Bike Sharing Dataset")
st.subheader("📅 Season")

# Menghitung total penyewaan sepeda di setiap musim
season_df = day_df.groupby("season")["cnt"].sum().reset_index()

# Mapping nama musim
season_names = {1: "Musim Dingin", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Semi"}
season_df["season_name"] = season_df["season"].map(season_names)

# Buat dua kolom untuk menampilkan data dalam format 2x2
col1, col2 = st.columns(2)

for index, row in enumerate(season_df.itertuples()):
    if index % 2 == 0:
        with col1:
            st.metric(label=f"Total Penyewaan - {row.season_name}", value=row.cnt)
    else:
        with col2:
            st.metric(label=f"Total Penyewaan - {row.season_name}", value=row.cnt)

# Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.subheader("📊 Penyewaan Sepeda di Setiap Musim")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_df["season_name"], y=season_df["cnt"], palette="viridis", ax=ax)
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Jumlah Penyewaan Sepeda di Setiap Musim")
st.pyplot(fig)

# Header
st.subheader("🌬️ Windspeed Analysis")

# Kategorisasi Windspeed menjadi Rendah, Sedang, dan Tinggi
bins = [0.13, 0.18, 0.23, 0.30]  
labels = ["Rendah", "Sedang", "Tinggi"]
day_df["windspeed_category"] = pd.cut(day_df["windspeed"], bins=bins, labels=labels)

# **Scatter Plot Windspeed vs Penyewaan Sepeda**
st.subheader("📈 Scatter Plot Windspeed")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=day_df["windspeed"], y=day_df["cnt"], alpha=0.5, ax=ax)
plt.xlabel("Windspeed")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Hubungan Windspeed dan Penyewaan Sepeda")
st.pyplot(fig)

# **Boxplot Windspeed dengan Kategori**
st.subheader("📊 Boxplot Windspeed (Kategori)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x=day_df["windspeed_category"], y=day_df["windspeed"], ax=ax, palette="Set2")
plt.xlabel("Kategori Windspeed")
plt.ylabel("Windspeed")
plt.title("Distribusi Windspeed Berdasarkan Kategori")
st.pyplot(fig)

# Header
st.subheader("📊 Analisis Penyewaan Sepeda pada Hari Libur")

holiday_only = day_df[day_df["holiday"] == 1]

# STACKED BAR CHART #
st.subheader("📊 Perbandingan penyewaan sepeda antara pengguna kasual dan pengguna terdaftar pada Hari Libur")

# Menghitung total penyewaan
casual_counts = holiday_only["casual"].sum()
registered_counts = holiday_only["registered"].sum()

# Membuat visualisasi Stacked Bar Chart
fig, ax = plt.subplots(figsize=(6, 5))
ax.bar("Hari Libur", casual_counts, label="Casual", color="red")
ax.bar("Hari Libur", registered_counts, bottom=casual_counts, label="Registered", color="blue")

# Menambahkan label dan judul
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Perbandingan Penyewaan Sepeda pada Hari Libur")
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# VIOLIN CHART #
st.subheader("🎻 Distribusi Penyewaan Sepeda pada Hari Libur")

# Mengubah data ke format yang sesuai untuk seaborn
violin_df = holiday_only.melt(id_vars=["holiday"], value_vars=["casual", "registered"],
                              var_name="User Type", value_name="Total Penyewaan")

# Membuat Violin Chart
fig, ax = plt.subplots(figsize=(6, 5))
sns.violinplot(x="User Type", y="Total Penyewaan", data=violin_df, palette={"casual": "red", "registered": "blue"}, ax=ax)

# Menambahkan judul dan label
ax.set_title("Distribusi Penyewaan Sepeda pada Hari Libur")
ax.set_xlabel("Jenis Pengguna")
ax.set_ylabel("Jumlah Penyewaan Sepeda")

# Menampilkan plot di Streamlit
st.pyplot(fig)