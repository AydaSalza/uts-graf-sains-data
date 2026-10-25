# UTS Graf Sains Data — RetailRocket

## Deskripsi
Repository ini berisi pengerjaan Ujian Tengah Semester (UTS) mata kuliah Graf Sains Data menggunakan dataset RetailRocket.

## Tujuan
- Melakukan data wrangling dan Exploratory Data Analysis (EDA).
- Membentuk representasi interaksi pengguna dan item sebagai graf.
- Menghitung kemiripan antar-item menggunakan cosine similarity.
- Menerapkan K-Nearest Neighbors (KNN) untuk rekomendasi item.
- Mengevaluasi rekomendasi menggunakan Hit@5 dan NDCG@5.

## Dataset
Dataset yang digunakan adalah RetailRocket, yang berisi data aktivitas pengguna terhadap item.

## Pembagian Analisis
- **Bagian 2.1 — Wrangling dan EDA:** pembersihan data, analisis eksploratif, pembentukan matriks interaksi, dan analisis kemiripan item.
- **Bagian 2.2 — Analytics:** pemilihan user target, rekomendasi menggunakan KNN dengan k = 5, serta evaluasi hasil rekomendasi.

## Teknologi
- Python
- Pandas dan NumPy
- SciPy
- Scikit-learn
- NetworkX
- Matplotlib
- Neo4j

## Cara Menjalankan
1. Siapkan dataset RetailRocket di folder `data/`.
2. Instal library yang dibutuhkan menggunakan `requirements.txt`.
3. Buka notebook `UTS_2_1.ipynb` untuk Bagian 2.1.
4. Buka notebook `UTS_2_2.ipynb` untuk Bagian 2.2.
5. Jalankan cell notebook secara berurutan.

## Catatan
Jangan mengunggah password Neo4j atau informasi rahasia lainnya ke repository GitHub.