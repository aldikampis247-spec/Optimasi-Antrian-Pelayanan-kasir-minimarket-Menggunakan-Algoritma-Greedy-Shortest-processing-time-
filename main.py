# src/main.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os
import psutil

# Import dari file lokal
import utils
import algorithm

class QueueOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Optimalisasi Antrian Pelayanan (Greedy SPT)")
        self.geometry("650x550")
        
        # Simpan state data pelanggan
        self.original_customers = []

        # Konfigurasi grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Membuat frame utama
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)

        # --- Bagian Input ---
        ttk.Label(main_frame, text="Waktu Pelayanan (pisahkan dengan koma):").grid(row=0, column=0, sticky="w", pady=5)
        self.times_entry = ttk.Entry(main_frame, width=60)
        self.times_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # --- Frame untuk Tombol ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2), weight=1)

        self.process_button = ttk.Button(button_frame, text="Proses Antrian", command=self.process_queue)
        self.process_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.load_button = ttk.Button(button_frame, text="Load dari File", command=self.load_from_file)
        self.load_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_all)
        self.reset_button.grid(row=0, column=2, padx=5, sticky="ew")

        # --- Bagian Output ---
        output_frame = ttk.LabelFrame(self, text="Hasil Optimasi", padding="10")
        output_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap="word", state="disabled", height=15)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        # Menambahkan scrollbar
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def process_queue(self):
        """
        Handler utama untuk memproses data input, menjalankan algoritma,
        dan menampilkan hasilnya.
        """
        input_str = self.times_entry.get()
        processing_times = utils.validate_input(input_str)

        if processing_times is None:
            messagebox.showerror("Input Tidak Valid", "Masukkan angka positif yang dipisahkan koma (contoh: 10, 5, 8).")
            return
            
        # Membuat daftar pelanggan dengan ID unik (berdasarkan urutan input)
        self.original_customers = list(enumerate(processing_times, 1)) # ID mulai dari 1

        # --- Analisis Performa ---
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        time_start = time.perf_counter()

        # Panggil algoritma greedy
        (sorted_customers, 
         waiting_times, 
         avg_wait, 
         total_wait, 
         comps) = algorithm.greedy_sjf(self.original_customers)

        time_end = time.perf_counter()
        mem_after = process.memory_info().rss

        exec_time = time_end - time_start
        mem_used = mem_after - mem_before
        
        # Simpan hasil analisis ke file
        utils.analyze_and_save(exec_time, mem_used, comps, len(self.original_customers))
        
        # Tampilkan hasil di GUI
        self.display_results(sorted_customers, waiting_times, avg_wait, total_wait)

        # Tampilkan visualisasi (bonus)
        self.show_visualization(sorted_customers, waiting_times)

    def display_results(self, sorted_customers, waiting_times, avg_wait, total_wait):
        """Format dan tampilkan hasil di Text widget."""
        order_str = " -> ".join([str(cid) for cid, _ in sorted_customers])

        wait_details_list = []
        for cid, p_time in sorted_customers:
            wait = waiting_times[cid]
            wait_details_list.append(f"- Pelanggan {cid} (Waktu Proses: {p_time}): Waktu Tunggu = {wait}")
        
        wait_details_str = "\n".join(wait_details_list)

        result_str = f"""--- HASIL OPTIMASI ANTRIAN ---

Strategi: Shortest Processing Time (SPT)

Urutan Pelayanan Optimal (ID Pelanggan):
{order_str}

Waktu Tunggu Individual:
{wait_details_str}

Total Waktu Tunggu: {total_wait}
Rata-rata Waktu Tunggu: {avg_wait:.2f}
"""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result_str)
        self.output_text.config(state="disabled")

    def show_visualization(self, sorted_customers, waiting_times):
        """Menyiapkan data dan memanggil fungsi visualisasi."""
        # Data sebelum optimasi
        orig_order, orig_waits, _ = utils.calculate_original_wait_times(self.original_customers)
        
        # Data setelah optimasi
        opt_order = [cid for cid, _ in sorted_customers]
        opt_waits = [waiting_times[cid] for cid in opt_order]

        try:
            utils.visualize_performance(orig_order, opt_order, orig_waits, opt_waits)
        except Exception as e:
            messagebox.showwarning("Visualisasi Gagal", f"Tidak dapat menampilkan grafik: {e}")

    def load_from_file(self):
        """Membuka dialog file dan memuat data."""
        filepath = filedialog.askopenfilename(
            title="Pilih File Input",
            filetypes=[("Text Files", "*.txt")],
            initialdir="./data/input"  # Mulai dari direktori data/input
        )
        if not filepath:
            return

        content = utils.read_from_file(filepath)
        if content is not None:
            self.times_entry.delete(0, tk.END)
            self.times_entry.insert(0, content)
        else:
            messagebox.showerror("Gagal Membaca File", f"Tidak dapat membuka atau membaca file di:\n{filepath}")
            
    def reset_all(self):
        """Membersihkan semua input dan output."""
        self.times_entry.delete(0, tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
        self.original_customers = []

if __name__ == "__main__":
    # Pastikan direktori `docs` ada saat program dijalankan
    os.makedirs('docs', exist_ok=True)
    app = QueueOptimizerApp()
    app.mainloop()
