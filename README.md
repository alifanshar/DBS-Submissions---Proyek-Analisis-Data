# Proyek Analisis Data: E-Commerce Public Dataset

**Nama:** Muhammad Alif Anshar  
**Email:** alif040105@gmail.com  
**ID Dicoding:** CDCC208D6Y2146

---

## Deskripsi Proyek

Proyek ini melakukan analisis data pada **Brazilian E-Commerce Public Dataset** yang mencakup data pesanan, produk, pelanggan, pembayaran, ulasan, dan pengiriman dari tahun 2016–2018.

### Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan total pendapatan (revenue) tertinggi, dan bagaimana tren penjualannya secara bulanan sepanjang periode 2017–2018?
2. Bagaimana hubungan antara keterlambatan pengiriman (dalam hari) terhadap skor ulasan pelanggan, dan negara bagian mana yang memiliki rata-rata keterlambatan tertinggi selama periode 2017–2018?

### Analisis Lanjutan
- **RFM Analysis**: Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary.

---

## Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv       # Data gabungan untuk dashboard
│   ├── rfm_data.csv        # Data RFM untuk dashboard
│   └── dashboard.py        # Aplikasi Streamlit
├── E-Commerce Public Dataset/
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── products_dataset.csv
│   ├── customers_dataset.csv
│   ├── sellers_dataset.csv
│   ├── geolocation_dataset.csv
│   └── product_category_name_translation.csv
├── notebook.ipynb          # Notebook analisis lengkap (sudah dijalankan)
├── requirements.txt        # Daftar library yang digunakan
└── README.md               # Dokumentasi proyek ini
```

---

## Cara Menjalankan Dashboard

### 1. Clone / Download Proyek

```bash
git clone https://github.com/alifanshar/DBS-Submissions---Proyek-Analisis-Data.git
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`

---

## Fitur Dashboard

- 📊 **KPI Cards**: Total revenue, jumlah pesanan, rata-rata nilai pesanan, jumlah kategori
- 📦 **Tab Revenue & Kategori**: Top 10 kategori berdasarkan revenue + tren bulanan top 3 kategori
- 🚚 **Tab Pengiriman & Review**: Hubungan delay pengiriman dengan review score + peta delay per state
- 👥 **Tab RFM Segmentasi**: Distribusi segmen pelanggan + statistik RFM per segmen
- 🔍 **Filter Interaktif**: Filter berdasarkan tahun, kategori produk, dan state pelanggan
