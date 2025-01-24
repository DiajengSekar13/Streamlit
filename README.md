# Daisy - Data Insight System

**Daisy** adalah platform analisis data berbasis **Streamlit** yang dirancang untuk menganalisis sentimen dari ulasan produk. Platform ini memanfaatkan kekuatan model **GroqAI LLM** yang diintegrasikan dengan **LangChain** untuk memberikan hasil analisis yang akurat dan mendalam. 

## Fitur Utama
1. **Analisis Sentimen Otomatis**  
   Daisy mampu mengidentifikasi pola sentimen (positif, netral, atau negatif) dari ulasan produk dengan tingkat akurasi tinggi.

2. **Integrasi Model LLM GroqAI**  
   Menggunakan teknologi **GroqAI LLM** yang diintegrasikan melalui **LangChain** untuk pemrosesan bahasa alami (NLP) yang canggih.

3. **Antarmuka Interaktif**  
   Dibangun dengan **Streamlit**, Daisy menyediakan antarmuka yang sederhana dan mudah digunakan untuk eksplorasi data.

4. **Visualisasi Data**  
   Platform ini dilengkapi dengan visualisasi grafis yang membantu pengguna memahami pola sentimen secara lebih intuitif.

5. **Pemrosesan Data Real-Time**  
   Memungkinkan analisis data yang cepat dan efisien, mendukung berbagai format data ulasan.

## Teknologi yang Digunakan
- **Python**  
  Bahasa pemrograman utama untuk membangun platform ini.
- **GroqAI LLM**  
  Model pembelajaran mesin untuk pemrosesan data ulasan.
- **LangChain**  
  Framework untuk mengintegrasikan model AI dengan pipeline data.
- **Streamlit**  
  Alat untuk membangun antarmuka web yang interaktif dan cepat.

## Cara Menggunakan
1. Clone repositori ini:  
   ```bash
   git clone https://github.com/username/daisy.git
2. Masuk ke direktori proyek:
   ```bash
   cd daisy
3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
4. Jalankan aplikasi:
   ```bash
   streamlit run app.py
5. Unggah dataset ulasan Anda dan analisis hasilnya secara langsung! (Gunakan Data yang sudah dibersihkan karena Mengingat Limit groqai hanya 3000)


Tujuan Pengembangan
Daisy bertujuan untuk membantu bisnis dan peneliti menganalisis sentimen pelanggan dengan cara yang efisien, sehingga dapat mendukung pengambilan keputusan yang lebih baik berbasis data.


### Penyesuaian:
1. Pastikan mengganti `username` dengan nama pengguna GitHub Anda di URL repositori.
2. Sesuaikan nama file seperti `Main.py` atau `langchain_helper.py` jika ada perbedaan nama file di proyek Anda. 

Setelah menambahkan file ini ke repositori Anda, pengguna lain akan lebih mudah memahami struktur dan fungsi proyek Anda. 😊
