import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.write("Test1")

# Load dataset
data = pd.read_csv('data.csv', delimiter=';')

st.write("Test2")
st.write(data)

# Mapping dari kode fasilitator ke nama fasilitator
fasilitator_mapping = {
    'DA01': 'Data Analytics - Adib Ahmad Istiqlal',
    'DA02': 'Data Analytics - Affan Ikhsan',
    'DA03': 'Data Analytics - Andrew Benedictus Jamesie',
    'DA04': 'Data Analytics - Bramantio Galih Arintoko',
    'DA05': 'Data Analytics - Camelia Regista ',
    'DA06': 'Data Analytics - Cindy Steffani',
    'DA07': 'Data Analytics - Eka Dwi Sariningsih',
    'DA08': 'Data Analytics - Fariz Fadila',
    'DA09': 'Data Analytics - Giselle Halim',
    'DA10': 'Data Analytics - Halim sajidi',
    'DA11': 'Data Analytics - Ida Sri Afiqah',
    'DA12': 'Data Analytics - Irfan Rizqulloh',
    'DA13': 'Data Analytics - Lutfi Herdiansyah Ws',
    'DA14': 'Data Analytics - Yayang Dwijayani Panggi',
    'DA15': 'Data Analytics - Bagus Akhlaq',
    'PM01': 'Project Management - Anggoro Yudho Nuswantoro',
    'PM02': 'Project Management - Cynthia Caroline',
    'PM03': 'Project Management - Fadasa Rizki Barata',
    'PM04': 'Project Management - Mufti Alie Satriawan',
    'PM05': 'Project Management - Muhammad Ali Umar',
    'PM06': 'Project Management - Muhammad Faris Afif Putra',
    'PM07': 'Project Management - Rahma Rizky Alifia',
    'PM08': 'Project Management - Roby Ismail Adi Putra',
    'PM09': 'Project Management - Wandi Oktapiadi',
    'PM10': 'Project Management - Togihon Josia Paber Simaremare',
    'PM11': 'Project Management - Andrey Prabowo',
    'PM12': 'Project Management - Anita Fitriyawati',
    'IS01': 'IT Support - Fauzia Anis Sekar Ningrum',
    'IS02': 'IT Support - Jajang Jamaludin',
    'IS03': 'IT Support - Kanaya Novivian Tabitha Angel',
    'UX01': 'UX Design - Hafizh Daffa Septianto',
    'UX02': 'UX Design - Maulana Akbar Kusuma',
    'UX03': 'UX Design - Muhamad Ibnu Farizky',
    'UX04': 'UX Design - Nisa Fatimatuz Zahro',
    'AD01': 'Advanced Data Analytics - Alif Khusain Bilfaqih',
    'AD02': 'Advanced Data Analytics - Erik Feri Fadli',
    'AD03': 'Advanced Data Analytics - Muhammad Aliif Nurrahman',
    'AD04': 'Advanced Data Analytics - Muhammad Sahrul',
    'AD05': 'Advanced Data Analytics - Rais Sulaiman Rusid',
    'AD06': 'Advanced Data Analytics - Yosriko Rahmat Karoni Sabelekake',
    'BI01': 'Business Intelligence - Darmawan Kristiaji',
    'BI02': 'Business Intelligence - Muhamad Ihsan Ashari',
    'BI03': 'Business Intelligence - Muhammad Fahmy Fakhrija',
    'BI04': 'Business Intelligence - Yonvi Satria',
    'CS01': 'Cybersecurity - Adrianus Yoga Arsa Sadana',
    'CS02': 'Cybersecurity - Arif Mulyono',
    'CS03': 'Cybersecurity - Daffa akhdan Fadhillah ',
    'CS04': 'Cybersecurity - Hendrik Roland Hutapea',
    'CS05': 'Cybersecurity - Affandy Murad',
    'DM01': 'Digital Marketing - Muhammad Rizqi Adha',
    'DM02': 'Digital Marketing - Azzam Fitra Nuraiman',
    'DM03': 'Digital Marketing - Ghalda Khairunnisa',
    'DM04': 'Digital Marketing - Wahyu Nudiya',
    'DM05': 'Digital Marketing - Trio Sellin Nur Kholis ',
    'DM06': 'Digital Marketing - Raffa Arya Nugraha',
    'DM07': 'Digital Marketing - Arijal Ibnu Jati',
    'IA01': 'IT Automation - Marcel Aditya Pamungkas',
    'IA02': 'IT Automation - Mario Angelo Prabawa'
}
st.write("Test3")


# Gantikan kode fasilitator dengan nama fasilitator
data['Kelompok Fasilitator'] = data['Kelompok Fasilitator'].map(fasilitator_mapping)

# Pastikan semua nilai dalam kolom 'Kelompok Fasilitator' adalah tipe string
data['Kelompok Fasilitator'] = data['Kelompok Fasilitator'].astype(str)
st.write("Test4")
# Sidebar for facilitator selection
st.sidebar.header('Filter Fasilitator')
fasilitator_options = ['Semua'] + sorted(data['Kelompok Fasilitator'].unique().tolist())
selected_fasilitator = st.sidebar.selectbox('Pilih Kelompok Fasilitator:', fasilitator_options)

st.write("Test5")
# <Tambahan

# Menghitung persentase kelulusan per kelompok fasilitator (TIDAK dipengaruhi oleh pemilihan)
kelulusan_counts = data.groupby('Kelompok Fasilitator')['Progress Belajar Percentage'].apply(
    lambda x: (x == '100%').sum()
)
st.write("Test5.1")
st.write(kelulusan_counts)
total_counts = data.groupby('Kelompok Fasilitator')['Jumlah Course yang Telah Diselesaikan'].count()
st.write("Test5.5")
st.write(total_counts)
# Menghitung persentase
persentase_kelulusan = (kelulusan_counts / total_counts * 100).fillna(0).round(2)
st.write("Test6")
# Mengubah ke DataFrame untuk tampilan tabel
kelulusan_df = pd.DataFrame({
    'Nama Fasilitator': persentase_kelulusan.index,
    'Persentase Kelulusan (%)': persentase_kelulusan.values
}).reset_index(drop=True)
st.write("Test7")
# Mengurutkan DataFrame dari persentase tertinggi ke terendah
# kelulusan_df.sort_values(by='Persentase Kelulusan (%)', ascending=False, inplace=True)

# Tambahan>

# Filter data based on the selected facilitator
if selected_fasilitator != 'Semua':
    data = data[data['Kelompok Fasilitator'] == selected_fasilitator]

st.title('Visualisasi Kelulusan dan Progress Peserta')

# Daftar peserta yang telah menyelesaikan seluruh course
st.header('Selamat kepada peserta berikut yang telah menyelesaikan seluruh course')

# Filter peserta yang telah menyelesaikan 8 course
completed_all_courses = data[data['Progress Belajar Percentage'] == '100%']['Nama'].tolist()

# Display the names of participants who completed all courses
jumlah = len(completed_all_courses)
completed_all_courses.sort()
col1, col2, col3 = st.columns(3)
name1 = []
name2 = []
name3 = []
count_name = 0
if completed_all_courses:
    for name in completed_all_courses:
        count_name = count_name + 1
        if count_name == 1:
            name1 = [name]
        elif count_name == 2:
            name2 = [name]
        elif count_name == 3:
            name3 = [name]
        if count_name > 3:
            if count_name % 3 == 1:
                name1 = name1 + [name]
            elif count_name % 3 == 2:
                name2 = name2 + [name]
            elif count_name % 3 == 0:
                name3 = name3 + [name]
    with col1:
        for name in name1:
                st.write(f"- {name}")
    with col2:
        for name in name2:
                st.write(f"- {name}")
    with col3:
        for name in name3:
                st.write(f"- {name}")
else:
    st.write("Belum ada peserta yang menyelesaikan seluruh course.")

# Display the names of participants who completed all courses
#if completed_all_courses:
#    for name in completed_all_courses:
#        st.write(f"- {name}")
#else:
#    st.write("Belum ada peserta yang menyelesaikan seluruh course.")

# Tingkat kelulusan per course (Bar chart)
note01 = '''
st.header('1. Tingkat Kelulusan per Course')

course_columns = [
    'Foundations of Cybersecurity', 
    'Play It Safe: Manage Security Risks', 
    'Connect and Protect: Networks and Network Security', 
    'Tools of the Trade: Linux and SQL', 
    'Assets, Threats, and Vulnerabilities', 
    'Sound the Alarm: Detection and Response', 
    'Automate Cybersecurity Tasks with Python', 
    'Put It to Work: Prepare for Cybersecurity Jobs'
]

# Calculate the number of participants who passed each course
kelulusan_data = {course: (data[course] == 'Lulus').sum() for course in course_columns}

fig_bar = px.bar(
    x=list(kelulusan_data.keys()),
    y=list(kelulusan_data.values()),
    labels={'x': 'Course', 'y': 'Jumlah Peserta Lulus'},
    title='Tingkat Kelulusan per Course'
)
st.plotly_chart(fig_bar)
'''


# Tingkat penyelesaian peserta (Pie chart)
st.header('2. Tingkat Penyelesaian Peserta')

# Calculate completion rates for participants based on the number of completed courses
completion_counts = data['Jumlah Course yang Telah Diselesaikan'].value_counts().sort_index()
completion_labels = [f'{i} Course' for i in completion_counts.index]

# Define color map to match each label
color_mapping = {
    '0 Course': '#FF0000',  # Merah untuk 0 course
    '1 Course': '#FF4500',  # Gradasi untuk 1 course
    '2 Course': '#FF7F00',  # Gradasi untuk 2 course
    '3 Course': '#FFFF00',  # Gradasi untuk 3 course
    '4 Course': '#7FFF00',  # Gradasi untuk 4 course
    '5 Course': '#00FF00',  # Gradasi untuk 5 course
    '6 Course': '#00FFFF',  # Gradasi untuk 6 course
    '7 Course': '#00BFFF',  # Gradasi untuk 7 course
    '8 Course': '#1E90FF'   # Kebiruan untuk 8 course
}

# Buat DataFrame dari names dan values
df_pie = pd.DataFrame({'names': completion_labels, 'values': completion_counts})

fig_pie_completion = px.pie(
    data_frame=df_pie,  # Gunakan DataFrame sebagai data_frame
    names='names',  # Kolom 'names' dalam DataFrame
    values='values',  # Kolom 'values' dalam DataFrame
    title='Tingkat Penyelesaian Semua Peserta',
    color='names',  # Gunakan 'names' sebagai kolom untuk pemetaan warna
    color_discrete_map=color_mapping
)
st.plotly_chart(fig_pie_completion)



df = data

# Menghapus tanda persentase dan mengkonversi ke numerik 
df['Progress Belajar Percentage'] = df['Progress Belajar Percentage'].str.replace('%', '').astype(float

# Mendefinisikan kategori
bins = [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
labels = ['>0% - 12.5%', '>12.5% - 25%', '>25% - 37.5%', '>37.5% - 50%', '>50% - 62.5%', '>62.5% - 75%', '>75% - 87.5%', '>87.5% - 100%']

# Mengelompokkan data ke dalam kategori
df['Kategori'] = pd.cut(df['Progress Belajar Percentage'], bins=bins, labels=labels, include_lowest=True)

# Menghitung jumlah peserta dalam setiap kategori
category_counts = df['Kategori'].value_counts().sort_index()

# Menambahkan kategori 0% secara manual
category_counts.loc['0%'] = (df['Progress Belajar Percentage'] == 0).sum()

# Membuat pie chart
plt.figure(figsize=(10, 7))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribusi Kategori Progress Belajar Peserta")
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()










# Distribusi status progress peserta (Pie chart)
st.header('3. Status Progress Peserta')

# Calculate distribution of progress status
progress_counts = data['Status Progress'].value_counts()
progress_labels = [f'{i}' for i in progress_counts.index]

# Define color map to match each label
color_mapping = {
    'Belum Terdaftar': '#FF0000', 
    'Belum Berprogress': '#FF4500',
    'Progress Dibawah Rekomendasi': '#FF7F00',
    'Progress Diatas/Sesuai Rekomendasi': '#00BFFF',
    'Sudah Lulus Spesialisasi': '#1E90FF',
}

# Buat DataFrame dari names dan values
df_pie = pd.DataFrame({'names': progress_labels, 'values': progress_counts})

fig_pie_completion = px.pie(
    data_frame=df_pie,  # Gunakan DataFrame sebagai data_frame
    names='names',  # Kolom 'names' dalam DataFrame
    values='values',  # Kolom 'values' dalam DataFrame
    title='Status Progress Peserta',
    color='names',  # Gunakan 'names' sebagai kolom untuk pemetaan warna
    color_discrete_map=color_mapping
)
st.plotly_chart(fig_pie_completion)

# Tampilkan daftar nama peserta dan tingkat penyelesaiannya
st.header('4. Daftar Peserta dan Tingkat Penyelesaian')

# Display a table with participants' names and their course completion status
completion_table = data[['Name', 'Total Course yang Sudah Diselesaikan']].sort_values(by='Total Course yang Sudah Diselesaikan', ascending=False)
completion_table = completion_table.rename(columns={'Name': 'Nama Peserta', 'Total Course yang Sudah Diselesaikan': 'Jumlah Course yang Diselesaikan'})
st.dataframe(completion_table)

# Menampilkan tabel
st.subheader('5. Persentase Kelulusan Per Kelompok Fasilitator')

st.write(kelulusan_df)

# Menyiapkan warna untuk grafik batang
colors = ['#4682B4'] * len(kelulusan_df)  # Warna Steel Blue
top_three_indices = kelulusan_df.nlargest(3, 'Persentase Kelulusan (%)').index.tolist()  # Indeks tiga teratas
for index in top_three_indices:
    colors[index] = '#1E90FF'  # Warna Dodger Blue untuk tiga teratas

# Membuat grafik batang menggunakan Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(kelulusan_df['Nama Fasilitator'], kelulusan_df['Persentase Kelulusan (%)'], color=colors)
plt.xlabel('Nama Fasilitator')
plt.ylabel('Persentase Kelulusan (%)')
plt.title('Persentase Kelulusan Per Kelompok Fasilitator')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 100)  # Mengatur batas y antara 0 dan 100

# Menambahkan garis horizontal
thresholds = [50, 72, 79, 86, 95]
for threshold in thresholds:
    plt.axhline(y=threshold, color='red', linestyle='--', linewidth=1)  # Garis horizontal merah putus-putus

# Menampilkan grafik di Streamlit
st.pyplot(plt)

# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
