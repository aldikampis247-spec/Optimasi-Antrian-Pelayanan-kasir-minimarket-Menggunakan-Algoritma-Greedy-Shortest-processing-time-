# src/utils.py

import os
import re
import time
import psutil
import matplotlib.pyplot as plt
from datetime import datetime

def validate_input(text_input):
    """
    Memvalidasi input dari pengguna. Input yang valid adalah angka yang dipisahkan
    koma, dengan opsional spasi.

    Args:
        text_input (str): String input dari kolom entri.

    Returns:
        list of int or None: Mengembalikan list integer jika valid, None jika tidak.
    """
    # Hapus spasi dan split berdasarkan koma
    cleaned_input = [part.strip() for part in text_input.split(',')]
    
    # Cek jika ada string kosong setelah split (misal: "10,,20")
    if any(part == '' for part in cleaned_input):
        return None

    try:
        # Konversi semua bagian menjadi integer
        numbers = [int(part) for part in cleaned_input]
        # Cek apakah ada angka negatif
        if any(num < 0 for num in numbers):
            return None
        return numbers
    except ValueError:
        # Gagal konversi ke integer
        return None

def read_from_file(filepath):
    """
    Membaca data waktu pelayanan dari sebuah file teks.

    Args:
        filepath (str): Path ke file input.

    Returns:
        str or None: Konten file sebagai string jika berhasil, None jika gagal.
    """
    try:
        with open(filepath, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def analyze_and_save(execution_time, memory_usage, operations_count, num_customers):
    """
    Menyimpan hasil analisis performa ke dalam file teks.

    Args:
        execution_time (float): Waktu eksekusi algoritma dalam detik.
        memory_usage (int): Penggunaan memori dalam bytes.
        operations_count (int): Jumlah operasi perbandingan.
        num_customers (int): Jumlah pelanggan yang diproses.
    """
    filepath = os.path.join('docs', 'analysis_results.txt')
    
    # Membuat direktori jika belum ada
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result_str = (
        f"--- Analysis @ {timestamp} ---\n"
        f"Jumlah Pelanggan     : {num_customers}\n"
        f"Operasi Perbandingan : {operations_count} (Insertion Sort)\n"
        f"Waktu Eksekusi (CPU) : {execution_time:.6f} detik\n"
        f"Penggunaan Memori    : {memory_usage / 1024:.2f} KB\n"
        f"---------------------------------------\n\n"
    )
    
    with open(filepath, 'a') as f:
        f.write(result_str)

def visualize_performance(original_order, optimized_order, original_waits, optimized_waits):
    """
    Membuat visualisasi perbandingan waktu tunggu menggunakan matplotlib.

    Args:
        original_order (list): Urutan ID pelanggan sebelum optimasi.
        optimized_order (list): Urutan ID pelanggan setelah optimasi.
        original_waits (list): Waktu tunggu untuk setiap pelanggan sebelum optimasi.
        optimized_waits (list): Waktu tunggu untuk setiap pelanggan setelah optimasi.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # --- Grafik 1: Waktu Tunggu Individual ---
    customer_ids_str_optimized = [f"Cust {cid}" for cid in optimized_order]
    ax1.bar(customer_ids_str_optimized, optimized_waits, color='skyblue')
    ax1.set_title('Waktu Tunggu Individual (Setelah Optimasi SPT)')
    ax1.set_xlabel('Pelanggan (diurutkan berdasarkan pelayanan)')
    ax1.set_ylabel('Waktu Tunggu')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # --- Grafik 2: Perbandingan Total Waktu Tunggu ---
    total_wait_original = sum(original_waits)
    total_wait_optimized = sum(optimized_waits)
    
    categories = ['Sebelum Optimasi', 'Setelah Optimasi (SPT)']
    totals = [total_wait_original, total_wait_optimized]
    
    bars = ax2.bar(categories, totals, color=['salmon', 'lightgreen'])
    ax2.set_title('Perbandingan Total Waktu Tunggu')
    ax2.set_ylabel('Total Waktu Tunggu')
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval}', va='bottom', ha='center')

    fig.tight_layout()
    plt.show()

def calculate_original_wait_times(customers):
    """
    Menghitung waktu tunggu jika antrian diproses sesuai urutan kedatangan (asli).
    """
    if not customers:
        return [], [], 0
    
    wait_times = []
    order = []
    current_time = 0
    for customer_id, processing_time in customers:
        order.append(customer_id)
        wait_times.append(current_time)
        current_time += processing_time
        
    return order, wait_times, sum(wait_times)
