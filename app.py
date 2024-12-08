import re
from turtle import onclick
import streamlit as st
import numpy as np
import joblib

st.set_page_config(
    page_title="Prediksi Sleep Disorder Menggunakan Metode Naive Bayes Gaussian",
    page_icon="💤",
    layout="wide",
)

# Load the model
model = joblib.load('shl_model.pkl')

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'input'

# Function to reset session state
def reset():
    st.session_state.page = 'input'

# Function to handle prediction
def handle_prediction():
    input_data = np.array([[
        st.session_state.gender,
        st.session_state.age,
        st.session_state.sleep_duration,
        st.session_state.quality_of_sleep,
        st.session_state.physical_activity_level,
        st.session_state.stress_level,
        st.session_state.bmi_category,
        st.session_state.systolic_blood_pressure,
        st.session_state.diastolic_blood_pressure,
        st.session_state.heart_rate,
        st.session_state.daily_steps
    ]])
    # Predict and update session state
    st.session_state.prediction = model.predict(input_data)[0]
    st.session_state.page = 'result'

# Input page
if st.session_state.page == 'input':
    st.title('Prediksi Sleep Disorder Menggunakan Metode Naive Bayes Gaussian')
    st.write("**Aplikasi ini membantu mendeteksi potensi gangguan tidur berdasarkan data kesehatan Anda.**")

    # Layout with three columns inside a form
    with st.form("input_form"):
        col1, space1, col2, space2, col3 = st.columns([1, 0.05, 1, 0.05, 1])

        with col1:
            st.session_state.gender = st.selectbox('Jenis Kelamin', ['Laki-laki', 'Perempuan'], index=0)
            st.session_state.gender = 1 if st.session_state.gender == 'Laki-laki' else 0
            st.session_state.age = st.number_input('Usia', min_value=1)
            st.session_state.sleep_duration = st.number_input('Durasi Tidur (jam)', min_value=0.0, max_value=24.0)
            st.session_state.quality_of_sleep = st.number_input('Kualitas Tidur (1-10)', min_value=1, max_value=10)

        with col2:
            st.session_state.systolic_blood_pressure = st.number_input('Tekanan Darah Sistolik (mmHg)')
            st.session_state.diastolic_blood_pressure = st.number_input('Tekanan Darah Diastolik (mmHg)')
            st.session_state.stress_level = st.number_input('Tingkat Stres (1-10)', min_value=1, max_value=10)
            st.session_state.physical_activity_level = st.number_input('Aktivitas Fisik (menit)', min_value=0, max_value=200)

        with col3:
            st.session_state.bmi_category = st.selectbox('Kategori BMI', ['Normal', 'Overweight', 'Obesitas'], index=0)
            st.session_state.bmi_category = 1 if st.session_state.bmi_category == 'Normal' else 2 if st.session_state.bmi_category == 'Overweight' else 3
            st.session_state.heart_rate = st.number_input('Detak Jantung (bpm)')
            st.session_state.daily_steps = st.number_input('Langkah Harian', min_value=0)

        # Button to submit form
        submitted = st.form_submit_button("Prediksi")
        if submitted:
            handle_prediction()

# Result page
elif st.session_state.page == 'result':
    st.title('Hasil Prediksi Sleep Disorder')
    prediction = st.session_state.prediction

    if prediction == 'None':
        st.success("**Anda tidak memiliki gejala gangguan tidur.**")
        st.write("Tetaplah menjaga pola hidup sehat seperti mengonsumsi makanan sehat, rajin berolahraga, dan tidur dengan teratur.")
    elif prediction == 'Insomnia':
        st.warning("**Anda memiliki gejala gangguan tidur Insomnia.**")
        st.write("""
        Berikut adalah beberapa tips mengatasi insomnia ringan:
        - Membuat lingkungan yang nyaman untuk tidur
        - Rajin berolahraga
        - Mengonsumsi makanan sehat
        - Menghindari penggunaan ponsel atau alat elektronik lainnya sebelum tidur
        - Membuat jadwal tidur yang teratur
        """)
    elif prediction == 'Sleep Apnea':
        st.error("**Anda memiliki gejala gangguan tidur Sleep Apnea.**")
        st.write("""
        Cobalah memulai pola hidup sehat seperti mengonsumsi makanan sehat, rajin berolahraga, dan tidur dengan teratur.
        Jika kondisi tidak membaik, segeralah periksa ke dokter untuk pengecekan dan penanganan lebih lanjut.
        """)

    if st.button('Prediksi Ulang'):
        reset()
