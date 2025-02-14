import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
data_raw = pd.read_csv('data.csv', delimiter=';')

# Mapping dari kode fasilitator ke nama fasilitator
fasilitator_mapping = {
    'DA01': 'Adib Ahmad Istiqlal',
    'DA02': 'Affan Ikhsan',
    'DA03': 'Andrew Benedictus Jamesie',
    'DA04': 'Bramantio Galih Arintoko',
    'DA05': 'Camelia Regista ',
    'DA06': 'Cindy Steffani',
    'DA07': 'Eka Dwi Sariningsih',
    'DA08': 'Fariz Fadila',
    'DA09': 'Giselle Halim',
    'DA10': 'Halim sajidi',
    'DA11': 'Ida Sri Afiqah',
    'DA12': 'Irfan Rizqulloh',
    'DA13': 'Lutfi Herdiansyah Ws',
    'DA14': 'Yayang Dwijayani Panggi',
    'DA15': 'Bagus Akhlaq',
    'PM01': 'Anggoro Yudho Nuswantoro',
    'PM02': 'Cynthia Caroline',
    'PM03': 'Fadasa Rizki Barata',
    'PM04': 'Mufti Alie Satriawan',
    'PM05': 'Muhammad Ali Umar',
    'PM06': 'Muhammad Faris Afif Putra',
    'PM07': 'Rahma Rizky Alifia',
    'PM08': 'Roby Ismail Adi Putra',
    'PM09': 'Wandi Oktapiadi',
    'PM10': 'Togihon Josia Paber Simaremare',
    'PM11': 'Andrey Prabowo',
    'PM12': 'Anita Fitriyawati',
    'IS01': 'Fauzia Anis Sekar Ningrum',
    'IS02': 'Jajang Jamaludin',
    'IS03': 'Kanaya Novivian Tabitha Angel',
    'UX01': 'Hafizh Daffa Septianto',
    'UX02': 'Maulana Akbar Kusuma',
    'UX03': 'Muhamad Ibnu Farizky',
    'UX04': 'Nisa Fatimatuz Zahro',
    'AD01': 'Alif Khusain Bilfaqih',
    'AD02': 'Erik Feri Fadli',
    'AD03': 'Muhammad Aliif Nurrahman',
    'AD04': 'Muhammad Sahrul',
    'AD05': 'Rais Sulaiman Rusid',
    'AD06': 'Yosriko Rahmat Karoni Sabelekake',
    'BI01': 'Darmawan Kristiaji',
    'BI02': 'Muhamad Ihsan Ashari',
    'BI03': 'Muhammad Fahmy Fakhrija',
    'BI04': 'Yonvi Satria',
    'CS01': 'Adrianus Yoga Arsa Sadana',
    'CS02': 'Arif Mulyono',
    'CS03': 'Daffa akhdan Fadhillah ',
    'CS04': 'Hendrik Roland Hutapea',
    'CS05': 'Affandy Murad',
    'DM01': 'Muhammad Rizqi Adha',
    'DM02': 'Azzam Fitra Nuraiman',
    'DM03': 'Ghalda Khairunnisa',
    'DM04': 'Wahyu Nudiya',
    'DM05': 'Trio Sellin Nur Kholis ',
    'DM06': 'Raffa Arya Nugraha',
    'DM07': 'Arijal Ibnu Jati',
    'IA01': 'Marcel Aditya Pamungkas',
    'IA02': 'Mario Angelo Prabawa'
}

# Gantikan kode fasilitator dengan nama fasilitator
data_raw['Kelompok Fasilitator'] = data_raw['Kelompok Fasilitator'].map(fasilitator_mapping)
# Pastikan semua nilai dalam kolom 'Kelompok Fasilitator' adalah tipe string
data_raw['Kelompok Fasilitator'] = data_raw['Kelompok Fasilitator'].astype(str)

# Sidebar for facilitator selection
st.sidebar.header('Pilihan Spesialisasi dan Fasilitator')

spesialisasi_options = data_raw['Spesialisasi'].unique().tolist()
selected_spesialisasi = st.sidebar.selectbox('Pilih Spesialisasi:', spesialisasi_options)

# Kita akan menyaring dataframe untuk hanya menyimpan baris di mana kolom 'Spesialisasi' adalah sesuai pilihan
data = data_raw[data_raw['Spesialisasi'] == selected_spesialisasi].reset_index()

fasilitator_options = ['Semua'] + sorted(data['Kelompok Fasilitator'].unique().tolist())
selected_fasilitator = st.sidebar.selectbox('Pilih Kelompok Fasilitator:', fasilitator_options)

# Mengambil nilai dari baris pertama pada kolom 'Jumlah_course'
jumlah_course = int(data.loc[0, 'Jumlah Course yang Perlu Diselesaikan'])

# Menghitung persentase kelulusan per kelompok fasilitator (TIDAK dipengaruhi oleh pemilihan)
kelulusan_counts = data.groupby('Kelompok Fasilitator')['Jumlah Course yang Telah Diselesaikan'].apply(
    lambda x: (x == jumlah_course).sum()
)
total_counts = data.groupby('Kelompok Fasilitator')['Jumlah Course yang Telah Diselesaikan'].count()

# Menghitung persentase
persentase_kelulusan = (kelulusan_counts / total_counts * 100).fillna(0).round(2)

# Mengubah ke DataFrame untuk tampilan tabel
kelulusan_df = pd.DataFrame({
    'Nama Fasilitator': persentase_kelulusan.index,
    'Persentase Kelulusan (%)': persentase_kelulusan.values
}).reset_index(drop=True)

# Mengurutkan DataFrame dari persentase tertinggi ke terendah
# kelulusan_df.sort_values(by='Persentase Kelulusan (%)', ascending=False, inplace=True)

# Tambahan>

# Filter data based on the selected facilitator
if selected_fasilitator != 'Semua':
    data = data[data['Kelompok Fasilitator'] == selected_fasilitator]

st.title('Visualisasi Kelulusan dan Progress Peserta')

# Daftar peserta yang telah menyelesaikan seluruh course
st.header('Selamat kepada peserta berikut yang telah menyelesaikan seluruh course')

# Filter peserta yang telah menyelesaikan 6 course
completed_all_courses = data[data['Jumlah Course yang Telah Diselesaikan'] == jumlah_course]['Nama'].tolist()

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

# Tingkat kelulusan per course (Bar chart)
st.header('1. Tingkat Kelulusan per Course')

# Filter data to exclude participants with 0 completed courses
filtered_data = data[data['Jumlah Course yang Telah Diselesaikan'] > 0]

# Create a list of course counts (1 to 6)
courses = list(range(1, jumlah_course+1))

# Initialize the dictionary
courses_data = {}

# Calculate the number of students completed for each course count
for course in courses:
    count = sum(filtered_data['Jumlah Course yang Telah Diselesaikan'] >= course)
    courses_data[course] = count

# Nama-nama kursus yang diinginkan sebagai kunci baru
if selected_spesialisasi == 'Google Data Analytics Professional Certificate':
    new_keys = [
        'Foundations: Data, Data, Everywhere',
        'Ask Questions to Make Data-Driven Decisions',
        'Prepare Data for Exploration',
        'Process Data from Dirty to Clean',
        'Analyze Data to Answer Questions',
        'Share Data Through the Art of Visualization',
        'Data Analysis with R Programming',
        'Google Data Analytics Capstone: Complete a Case Study'
    ]
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
elif selected_spesialisasi == 'Google Project Management Professional Certificate':
    new_keys = [
        'Foundations of Project Management',
        'Project Initiation: Starting a Successful Project',
        'Project Planning: Putting It All Together',
        'Project Execution: Running the Project',
        'Agile Project Management',
        'Capstone: Applying Project Management in the Real World'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#FF7F00',  # Gradasi untuk 2 course
        '3 Course': '#FFFF00',  # Gradasi untuk 3 course
        '4 Course': '#00FFFF',  # Gradasi untuk 4 course
        '5 Course': '#00BFFF',  # Gradasi untuk 5 course
        '6 Course': '#1E90FF'   # Kebiruan untuk 6 course
    }
elif selected_spesialisasi == 'Google IT Support Professional Certificate':
    new_keys = [
        'Technical Support Fundamentals',
        'The Bits and Bytes of Computer Networking',
        'Operating Systems and You: Becoming a Power User',
        'System Administration and IT Infrastructure Services',
        'IT Security: Defense against the digital dark arts'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#FF7F00',  # Gradasi untuk 2 course
        '3 Course': '#00FFFF',  # Gradasi untuk 3 course
        '4 Course': '#00BFFF',  # Gradasi untuk 4 course
        '5 Course': '#1E90FF'   # Kebiruan untuk 5 course
    }
elif selected_spesialisasi == 'Google UX Design Professional Certificate':
    new_keys = [
        'Foundations of User Experience (UX) Design',
        'Start the UX Design Process: Empathize, Define, and Ideate',
        'Build Wireframes and Low-Fidelity Prototypes',
        'Conduct UX Research and Test Early Concepts',
        'Create High-Fidelity Designs and Prototypes in Figma',
        'Build Dynamic User Interfaces (UI) for Websites',
        'Design a User Experience for Social Good & Prepare for Jobs'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#FF7F00',  # Gradasi untuk 2 course
        '3 Course': '#FFFF00',  # Gradasi untuk 3 course
        '4 Course': '#00FF00',  # Gradasi untuk 4 course
        '5 Course': '#00FFFF',  # Gradasi untuk 5 course
        '6 Course': '#00BFFF',  # Gradasi untuk 6 course
        '7 Course': '#1E90FF'   # Kebiruan untuk 7 course
    }
elif selected_spesialisasi == 'Google Advanced Data Analytics Professional Certificate':
    new_keys = [
        'Foundations of Data Science',
        'Get Started with Python',
        'Go Beyond the Numbers: Translate Data into Insights',
        'The Power of Statistics',
        'Regression Analysis: Simplify Complex Data Relationships',
        'The Nuts and Bolts of Machine Learning',
        'Google Advanced Data Analytics Capstone'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#FF7F00',  # Gradasi untuk 2 course
        '3 Course': '#FFFF00',  # Gradasi untuk 3 course
        '4 Course': '#00FF00',  # Gradasi untuk 4 course
        '5 Course': '#00FFFF',  # Gradasi untuk 5 course
        '6 Course': '#00BFFF',  # Gradasi untuk 6 course
        '7 Course': '#1E90FF'   # Kebiruan untuk 7 course
    }
elif selected_spesialisasi == 'Google Business Intelligence Professional Certificate':
    new_keys = [
        'Foundations of Business Intelligence',
        'The Path to Insights: Data Models and Pipeline',
        'Decisions, Decisions: Dashboards and Reports'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#00BFFF',  # Gradasi untuk 2 course
        '3 Course': '#1E90FF'   # Kebiruan untuk 3 course
    }
elif selected_spesialisasi == 'Google Cybersecurity Professional Certificate':
    new_keys = [
        'Foundations of Cybersecurity',
        'Play It Safe: Manage Security Risks',
        'Connect and Protect: Networks and Network Security',
        'Tools of the Trade: Linux and SQL',
        'Assets, Threats, and Vulnerabilities',
        'Sound the Alarm: Detection and Response',
        'Automate Cybersecurity Tasks with Python',
        'Put It to Work: Prepare for Cybersecurity Jobs'
    ]
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
elif selected_spesialisasi == 'Google Digital Marketing & E-Commerce Professional Certificate':
    new_keys = [
        'Foundations of Digital Marketing and E-commerce',
        'Attract and Engage Customers with Digital Marketing',
        'From Likes to Leads: Interact with Customers Online',
        'Think Outside the Inbox: Email Marketing',
        'Assess for Success: Marketing Analytics and Measurement',
        'Make the Sale: Build, Launch, and Manage E-commerce Stores',
        'Satisfaction Guaranteed: Develop Customer Loyalty Online'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#FF7F00',  # Gradasi untuk 2 course
        '3 Course': '#FFFF00',  # Gradasi untuk 3 course
        '4 Course': '#00FF00',  # Gradasi untuk 4 course
        '5 Course': '#00FFFF',  # Gradasi untuk 5 course
        '6 Course': '#00BFFF',  # Gradasi untuk 6 course
        '7 Course': '#1E90FF'   # Kebiruan untuk 7 course
    }
else:
    new_keys = [
        'Crash Course on Python',
        'Using Python to Interact with the Operating System',
        'Introduction to Git and GitHub',
        'Troubleshooting and Debugging Techniques',
        'Configuration Management and the Cloud',
        'Automating Real-World Tasks with Python'
    ]
    # Define color map to match each label
    color_mapping = {
        '0 Course': '#FF0000',  # Merah untuk 0 course
        '1 Course': '#FF4500',  # Gradasi untuk 1 course
        '2 Course': '#FF7F00',  # Gradasi untuk 2 course
        '3 Course': '#00FF00',  # Gradasi untuk 3 course
        '4 Course': '#00FFFF',  # Gradasi untuk 4 course
        '5 Course': '#00BFFF',  # Gradasi untuk 5 course
        '6 Course': '#1E90FF'   # Kebiruan untuk 6 course
    }

# Membuat dictionary baru dengan kunci yang diubah
courses_data_item = enumerate(courses_data.items())
courses_data_updated = {new_keys[i]: value for i, (key, value) in enumerate(courses_data.items())}

fig_bar = px.bar(
    x=list(courses_data_updated.keys()),
    y=list(courses_data_updated.values()),
    labels={'x': 'Course', 'y': 'Jumlah Peserta Lulus'},
    title='Tingkat Kelulusan per Course'
)
st.plotly_chart(fig_bar)

# Tingkat penyelesaian peserta (Pie chart)
st.header('2. Tingkat Penyelesaian Peserta')

# Calculate completion rates for participants based on the number of completed courses
completion_counts = data['Jumlah Course yang Telah Diselesaikan'].value_counts().sort_index()

completion_labels = [f'{int(i)} Course' for i in completion_counts.index]

# Define color map to match each label
#color_mapping = {
#    '0 Course': '#FF0000',  # Merah untuk 0 course
#    '1 Course': '#FF4500',  # Gradasi untuk 1 course
#    '2 Course': '#FF7F00',  # Gradasi untuk 2 course
#    '3 Course': '#FFFF00',  # Gradasi untuk 3 course
#    '4 Course': '#7FFF00',  # Gradasi untuk 4 course
#    '5 Course': '#00FF00',  # Gradasi untuk 5 course
#    '6 Course': '#00FFFF',  # Gradasi untuk 6 course
#    '7 Course': '#00BFFF',  # Gradasi untuk 7 course
#    '8 Course': '#1E90FF'   # Kebiruan untuk 8 course
#}




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




# Distribusi status progress peserta (Pie chart)
st.header('3. Status Progress Peserta')

# Calculate distribution of progress status
progress_counts = data['Remark Progress Belajar'].value_counts()
progress_labels = [f'{i}' for i in progress_counts.index]

# Define color map to match each label
color_mapping = {
    'Belum Enroll': '#FF0000', 
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
completion_table = data[['Nama', 'Jumlah Course yang Telah Diselesaikan']].sort_values(by='Jumlah Course yang Telah Diselesaikan', ascending=False)
completion_table = completion_table.rename(columns={'Nama': 'Nama Peserta', 'Jumlah Course yang Telah Diselesaikan': 'Jumlah Course yang Diselesaikan'})
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

######################################
# PENAMBAHAN VISUALISASI BUSINESS UNIT
######################################

# Load the dataset
#df_bu = pd.read_csv('data.csv', delimiter=';')

## Filter the dataset
#lulus_spesialisasi = df_bu[df_bu['Remark Progress Belajar'] == 'Sudah Lulus Spesialisasi']

# Calculate the percentage
#total_participants = df_bu['Unit Divisi/Nama AP/Yayasan '].value_counts()
#lulus_participants = lulus_spesialisasi['Unit Divisi/Nama AP/Yayasan '].value_counts()
#percentage_lulus = (lulus_participants / total_participants) * 100
#percentage_lulus = percentage_lulus.fillna(0)  # Replace NaN with 0

# Create a DataFrame for the table
#percentage_table = pd.DataFrame({
#    'Unit Divisi/Nama AP/Yayasan': percentage_lulus.index,
#    'Percentage Lulus (%)': percentage_lulus.values
#})

## Display the table in Streamlit
#st.write("Percentage of Participants Who Have Completed Specialization by Unit Divisi/Nama AP/Yayasan")
#st.table(percentage_table)

## Visualize the table using a bar chart
#st.write("Visualization of Percentage of Participants Who Have Completed Specialization by Unit Divisi/Nama AP/Yayasan")
#plt.figure(figsize=(10, 6))
#plt.bar(percentage_table['Unit Divisi/Nama AP/Yayasan'], percentage_table['Percentage Lulus (%)'], color='skyblue')
#plt.xlabel('Unit Divisi/Nama AP/Yayasan')
#plt.ylabel('Percentage Lulus (%)')
#plt.title('Percentage of Participants Who Have Completed Specialization by Unit Divisi/Nama AP/Yayasan')
#plt.xticks(rotation=45, ha='right')
#st.pyplot(plt)


######################################

# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)
