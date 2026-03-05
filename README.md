# Optimalisasi Antrian Pelayanan Menggunakan Algoritma Greedy

Proyek ini adalah sebuah program simulasi untuk mengoptimalkan urutan antrian pelayanan (seperti kasir, loket, atau customer service) dengan tujuan meminimalkan rata-rata waktu tunggu pelanggan.

Pendekatan yang digunakan adalah **Algoritma Greedy** dengan strategi **Shortest Processing Time (SPT)** atau **Shortest Job First (SJF) non-preemptive**, di mana pelanggan dengan estimasi waktu pelayanan tercepat akan dilayani terlebih dahulu.

## Fitur

-   **Algoritma Greedy (SPT/SJF)**: Mengurutkan antrian untuk efisiensi maksimal.
-   **Antarmuka Grafis (GUI)**: Dibangun menggunakan `Tkinter` untuk kemudahan penggunaan.
-   **Input Fleksibel**: Data pelanggan dapat diinput langsung melalui GUI atau di-load dari file teks.
-   **Analisis Kompleksitas**: Program secara otomatis mengukur waktu eksekusi, penggunaan memori, dan jumlah operasi dasar (perbandingan) lalu menyimpannya ke file.
-   **Visualisasi Data**: Menampilkan grafik perbandingan total waktu tunggu sebelum dan sesudah optimasi menggunakan `matplotlib`.
-   **Unit Testing**: Kebenaran algoritma dijamin oleh serangkaian test case (best, worst, average, dan edge case).

## Struktur Direktori

```
OptimalisasiAntrianGreedy/
│
├── src/
│   ├── main.py          # GUI Tkinter & entry point program
│   ├── algorithm.py     # Implementasi algoritma greedy
│   └── utils.py         # Fungsi pendukung (I/O, validasi, analisis)
│
├── data/
│   ├── input/
│   │   └── sample_input.txt
│   └── output/
│
├── tests/
│   └── test_algorithm.py
│
├── docs/
│   └── analysis_results.txt
│
├── README.md
└── requirements.txt
```

## Cara Instalasi

1.  Pastikan Anda memiliki Python 3.6 atau yang lebih baru.
2.  Clone repositori ini atau unduh dalam bentuk ZIP.
3.  Buka terminal atau command prompt, navigasi ke direktori `OptimalisasiAntrianGreedy`.
4.  Instal semua dependensi yang dibutuhkan dengan menjalankan perintah:
    ```bash
    pip install -r requirements.txt
    ```

## Cara Menjalankan Program

Program dapat dijalankan melalui mode GUI. Pastikan Anda berada di direktori root `OptimalisasiAntrianGreedy/`.

Jalankan perintah berikut di terminal:

```bash
python src/main.py
```

Sebuah jendela GUI akan muncul.

### Menggunakan GUI

1.  **Input Waktu Pelayanan**: Masukkan estimasi waktu pelayanan untuk setiap pelanggan, dipisahkan oleh koma. Contoh: `20, 5, 10`.
2.  **Tombol "Proses Antrian"**: Klik untuk menjalankan simulasi. Hasilnya (urutan pelayanan, waktu tunggu, dan rata-rata) akan muncul di area output. Grafik perbandingan juga akan ditampilkan di jendela terpisah.
3.  **Tombol "Load dari File"**: Klik untuk memilih file `.txt` yang berisi data waktu pelayanan. Program akan otomatis memuatnya ke kolom input.
4.  **Tombol "Reset"**: Klik untuk membersihkan semua input dan output.

## Contoh Penggunaan

**Input di GUI**:

```
15, 8, 3, 10
```

**Output yang Dihasilkan**:

```
--- HASIL OPTIMASI ANTRIAN ---

Strategi: Shortest Processing Time (SPT)

Urutan Pelayanan Optimal (ID Pelanggan):
3 -> 2 -> 4 -> 1

Waktu Tunggu Individual:
- Pelanggan 3 (Waktu Proses: 3): Waktu Tunggu = 0
- Pelanggan 2 (Waktu Proses: 8): Waktu Tunggu = 3
- Pelanggan 4 (Waktu Proses: 10): Waktu Tunggu = 11
- Pelanggan 1 (Waktu Proses: 15): Waktu Tunggu = 21

Total Waktu Tunggu: 35
Rata-rata Waktu Tunggu: 8.75
```

## Studi Kasus: Optimalisasi Antrian di Minimarket

Algoritma Greedy dengan strategi *Shortest Processing Time* (SPT) dapat diterapkan secara nyata untuk meningkatkan efisiensi sistem antrian di kasir minimarket seperti Alfamidi, terutama pada jam-jam sibuk.

**Skenario:**
Bayangkan sebuah minimarket dengan satu kasir pada pukul 12:00 siang. Ada 4 pelanggan yang antri bersamaan dengan estimasi waktu pelayanan berdasarkan jumlah barang yang mereka beli:
- **Pelanggan 1**: Membeli banyak barang (estimasi 10 menit).
- **Pelanggan 2**: Membeli beberapa barang (estimasi 4 menit).
- **Pelanggan 3**: Hanya membeli satu minuman (estimasi 1 menit).
- **Pelanggan 4**: Membeli sedikit snack (estimasi 2 menit).

---

### Skenario 1: Tanpa Optimasi (First-Come, First-Served)

Kasir melayani berdasarkan urutan kedatangan (Pelanggan 1 -> 2 -> 3 -> 4).

- **Waktu Tunggu Pelanggan 1**: 0 menit.
- **Waktu Tunggu Pelanggan 2**: 10 menit (menunggu Pelanggan 1 selesai).
- **Waktu Tunggu Pelanggan 3**: 10 + 4 = 14 menit.
- **Waktu Tunggu Pelanggan 4**: 10 + 4 + 1 = 15 menit.

- **Total Waktu Tunggu**: 0 + 10 + 14 + 15 = **39 menit**.
- **Rata-rata Waktu Tunggu**: 39 / 4 = **9.75 menit**.

Dalam skenario ini, pelanggan dengan transaksi cepat harus menunggu sangat lama, yang dapat menyebabkan ketidakpuasan.

---

### Skenario 2: Dengan Optimasi (Algoritma Greedy SPT)

Kasir melayani berdasarkan estimasi waktu tercepat (Pelanggan 3 -> 4 -> 2 -> 1).

- **Urutan Pelayanan**:
  1. Pelanggan 3 (1 menit)
  2. Pelanggan 4 (2 menit)
  3. Pelanggan 2 (4 menit)
  4. Pelanggan 1 (10 menit)

- **Waktu Tunggu Pelanggan 3**: 0 menit.
- **Waktu Tunggu Pelanggan 4**: 1 menit (menunggu Pelanggan 3 selesai).
- **Waktu Tunggu Pelanggan 2**: 1 + 2 = 3 menit.
- **Waktu Tunggu Pelanggan 1**: 1 + 2 + 4 = 7 menit.

- **Total Waktu Tunggu**: 0 + 1 + 3 + 7 = **11 menit**.
- **Rata-rata Waktu Tunggu**: 11 / 4 = **2.75 menit**.

---

**Kesimpulan:**

Dengan menerapkan algoritma Greedy (SPT), rata-rata waktu tunggu **berkurang dari 9.75 menit menjadi 2.75 menit**. Ini menunjukkan bahwa mengubah urutan pelayanan untuk mendahulukan pelanggan dengan transaksi tercepat dapat secara drastis mengurangi waktu tunggu keseluruhan dan meningkatkan kepuasan pelanggan tanpa menambah sumber daya (kasir).

Implementasi praktisnya bisa berupa jalur kasir khusus "Express" untuk pelanggan dengan ≤ 5 barang, yang merupakan aplikasi sederhana dari prinsip SPT.
