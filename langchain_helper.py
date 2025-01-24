import os
import re
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from tenacity import retry, wait_fixed, stop_after_attempt
import textwrap

# Konfigurasi API Key
os.environ["GROQ_API_KEY"] = "Masukkan GROQ API Key"
os.environ["LANGCHAIN_API_KEY"] = "Masukkan Langchain API KEY"

# Inisialisasi LLM
llm = ChatGroq(
   temperature=0.7,
   max_tokens=150,
   max_retries=2,
)

# Fungsi untuk memecah teks menjadi potongan lebih kecil
def split_text_into_chunks(text, chunk_size=1000):
   return textwrap.wrap(text, chunk_size)

# Fungsi untuk membersihkan harga
def clean_price(price):
   if isinstance(price, str):
       cleaned_price = re.sub(r'[^0-9.,]', '', price)
       if cleaned_price.count('.') > 1:
           cleaned_price = cleaned_price.replace('.', '', cleaned_price.count('.') - 1)
       cleaned_price = cleaned_price.replace(',', '.')
       try:
           return float(cleaned_price)
       except ValueError:
           return 0.0
   return 0.0

# Fungsi untuk normalisasi respons model
def normalize_response(response):
   """
   Memeriksa apakah respons model sesuai dengan ekspektasi.
   Menghapus karakter tambahan atau informasi yang tidak relevan.
   """
   response_text = response.strip().lower()
   if "positif" in response_text:
       return "Positif"
   elif "negatif" in response_text:
       return "Negatif"
   elif "netral" in response_text:
       return "Netral"
   return "Netral"

# Fungsi untuk analisis sentimen dengan retry
@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def analyze_sentiment(text):
   prompt_template = PromptTemplate(
       input_variables=["text"],
       template=(
           "Teks berikut adalah ulasan: \"{text}\". "
           "Berikan satu kata yang menggambarkan sentimen ulasan ini: "
           "Positif, Negatif, atau Netral. Jangan tambahkan informasi tambahan."
       )
   )
   chain = LLMChain(llm=llm, prompt=prompt_template)

   try:
       # Menggunakan invoke() alih-alih run() untuk menghindari peringatan deprecation
       response = chain.invoke({"text": text})
       # Mencetak model response sebelum normalisasi
       print(f"Model response: {response}")

       # Normalisasi respons
       return normalize_response(response['text'])
   except Exception as e:
       print(f"Error during sentiment analysis: {e}")
       return "Netral"

# Fungsi untuk menjawab pertanyaan terkait hasil sentimen
@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def ask_question(question, data):
   prompt_template = PromptTemplate(
       input_variables=["question", "data"],
       template=(
           "Berikut adalah hasil analisis sentimen dalam format tabel:\n"
           "{data}\n\n"
           "Jawablah pertanyaan berikut berdasarkan tabel di atas atau jika tidak terkait, jawab secara umum:\n"
           "{question}"
       )
   )
   chain = LLMChain(llm=llm, prompt=prompt_template)

   try:
       response = chain.invoke({"question": question, "data": data.to_csv(index=False)})
       # Mencetak model response untuk Q&A
       print(f"Model response: {response}")
       return response.strip()
   except Exception as e:
       print(f"Error during Q&A: {e}")
       return "Error"

# Fungsi untuk menjawab pertanyaan terkait data mentah
def analyze_data(question, data):
   if 'harga' in data.columns:
       data['cleaned_harga'] = data['harga'].apply(clean_price)

   question = question.lower()


   if "harga tertinggi" in question:
       highest_price_row = data.loc[data['cleaned_harga'].idxmax()]
       return f"Produk dengan harga tertinggi adalah {highest_price_row['namaproduk']} dengan harga {highest_price_row['harga']}."
   elif "rata-rata harga" in question:
       avg_price = data['cleaned_harga'].mean()
       return f"Rata-rata harga adalah {avg_price:.2f}."
   elif "rata-rata rating" in question:
       avg_rating = data['rating'].mean()
       return f"Rata-rata rating adalah {avg_rating:.2f}."
   else:
       return "Pertanyaan tidak dikenali."
