# src/algorithm.py

def greedy_sjf(customers):
    """
    Mengoptimalkan urutan antrian pelanggan menggunakan algoritma Greedy
    berdasarkan strategi Shortest Job First (SJF) atau Shortest Processing Time (SPT).

    Args:
        customers (list of tuple): Daftar pelanggan, di mana setiap tuple berisi
                                   (id_pelanggan, waktu_proses).
                                   Contoh: [(1, 15), (2, 8), (3, 3)]

    Returns:
        tuple: Berisi beberapa hasil analisis:
            - sorted_customers (list of tuple): Urutan pelanggan setelah dioptimalkan.
            - waiting_times (dict): Waktu tunggu untuk setiap ID pelanggan.
            - average_waiting_time (float): Rata-rata waktu tunggu semua pelanggan.
            - total_waiting_time (int): Total waktu tunggu.
            - comparison_count (int): Jumlah operasi perbandingan yang dilakukan
                                      selama proses sorting (menggunakan insertion sort
                                      untuk tujuan demonstrasi perhitungan).
    """
    if not customers:
        return [], {}, 0, 0, 0

    # --- Analisis Kompleksitas: Menghitung operasi perbandingan ---
    # Untuk tujuan demonstrasi, kita akan menggunakan insertion sort
    # agar dapat menghitung operasi perbandingan secara eksplisit.
    # Dalam implementasi nyata, Python `sorted()` (Timsort) jauh lebih efisien
    # tetapi lebih kompleks untuk diinstrumentasi.
    
    n = len(customers)
    comparison_count = 0
    # Buat salinan agar tidak mengubah list asli
    sorted_customers = list(customers)

    # Implementasi Insertion Sort untuk menghitung perbandingan
    for i in range(1, n):
        key_item = sorted_customers[i]
        j = i - 1
        # Pindahkan elemen yang lebih besar dari key_item ke kanan
        while j >= 0:
            comparison_count += 1  # Setiap kali perbandingan di dalam while terjadi
            if sorted_customers[j][1] > key_item[1]:
                sorted_customers[j + 1] = sorted_customers[j]
                j -= 1
            else:
                break
        sorted_customers[j + 1] = key_item

    # --- Menghitung Waktu Tunggu ---
    waiting_times = {}
    total_waiting_time = 0
    current_time = 0

    for customer_id, processing_time in sorted_customers:
        # Waktu tunggu untuk pelanggan saat ini adalah total waktu dari pelanggan sebelumnya
        waiting_times[customer_id] = current_time
        total_waiting_time += current_time
        
        # Tambahkan waktu proses pelanggan ini ke total waktu untuk pelanggan berikutnya
        current_time += processing_time

    # --- Menghitung Rata-rata Waktu Tunggu ---
    average_waiting_time = total_waiting_time / n if n > 0 else 0

    return sorted_customers, waiting_times, average_waiting_time, total_waiting_time, comparison_count
