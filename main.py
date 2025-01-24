import streamlit as st
import pandas as pd
from langchain_helper import analyze_sentiment, ask_question, analyze_data
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Daisy: Data Insight System")

# Upload file
uploaded_file = st.file_uploader("Unggah file CSV atau Excel", type=["csv", "xlsx"])

# Inisialisasi global variable untuk hasil sentimen
results = None

if uploaded_file:
    # Membaca file yang diunggah
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Menampilkan data yang diunggah
    st.write("Data yang diunggah:")
    st.dataframe(data)

    # Pilih Kolom untuk Analisis Sentimen
    st.header("Analisis Sentimen")
    column_options = data.columns.tolist()
    selected_column = st.selectbox("Pilih kolom teks untuk analisis sentimen", column_options)

    if selected_column:
        st.write(f"Menampilkan data dari kolom: {selected_column}")
        st.write(data[selected_column].head())

        # Analisis Sentimen
        if st.button("Analisis Sentimen"):
            st.write("Melakukan analisis sentimen...")
            sentiments = data[selected_column].dropna().apply(analyze_sentiment)

            # Menampilkan hasil analisis
            results = pd.DataFrame({
                "Teks": data[selected_column].dropna(),
                "Sentimen": sentiments
            })
            st.write("Hasil Sentimen:")
            st.dataframe(results)

            # Visualisasi Sentimen
            st.write("Visualisasi Sentimen:")
            sentiment_counts = results["Sentimen"].value_counts()
            plt.figure(figsize=(8, 4))
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis")
            plt.title("Distribusi Sentimen")
            plt.xlabel("Sentimen")
            plt.ylabel("Jumlah")
            for index, value in enumerate(sentiment_counts.values):
                plt.text(index, value, str(value), ha='center', va='bottom')
            st.pyplot(plt)

            # Unduh hasil analisis
            csv = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Unduh Hasil Analisis",
                data=csv,
                file_name="hasil_sentimen.csv",
                mime="text/csv"
            )

    # Fitur Tanya Jawab Tentang Data atau Hasil Analisis
    st.header("Tanya Jawab Tentang Data atau Hasil Analisis")
    question = st.text_input("Tanyakan sesuatu tentang data atau hasil analisis:")

    if question:
        st.write("Mencari jawaban untuk pertanyaan Anda...")
        try:
            if "harga" in data.columns and ("rata-rata harga" in question or "harga tertinggi" in question):
                # Jika pertanyaan berkaitan dengan data mentah, gunakan fungsi analyze_data
                answer = analyze_data(question, data)
                st.write(f"Jawaban: {answer}")
            elif results is not None:
                # Jika hasil analisis sentimen sudah ada, gunakan fungsi ask_question untuk pertanyaan terkait hasil analisis
                answer = ask_question(question, results)
                st.write(f"Jawaban: {answer}")
            else:
                st.error("Lakukan analisis sentimen terlebih dahulu untuk tanya jawab terkait hasil analisis.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menjawab pertanyaan: {e}")
