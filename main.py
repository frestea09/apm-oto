import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import os
import threading

# Fungsi untuk membuka aplikasi Frista dan melakukan login
def login_frista():
    if os.path.exists("D:\\BPJS\\Frista\\Frista.exe"):
        os.startfile("D:\\BPJS\\Frista\\Frista.exe")
    else:
        print("Error: File Frista.exe tidak ditemukan")

    # Tunggu 5 detik setelah Frista terbuka sebelum mengisi username dan password
    time.sleep(5)  # Tunggu 5 detik setelah Frista terbuka

    # Mengisi username dan password di Frista
    pyautogui.write("1002r006th")  # Mengisi username
    pyautogui.press('tab')  # Pindah ke field password
    pyautogui.write("#Bandung28")  # Mengisi password

    # Pindah ke tombol Login dan menekan tombol Login dengan Space
    pyautogui.press('tab')  # Pindah ke tombol Login
    pyautogui.press('space')  # Tekan Space untuk menekan tombol Login

    # Tunggu sebentar untuk memastikan aplikasi merespons
    time.sleep(1)

# Fungsi untuk membuka aplikasi After dan melakukan login
def login_after():
    if os.path.exists("C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"):
        os.startfile("C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe")
    else:
        print("Error: File After.exe tidak ditemukan")

    # Tunggu 7 detik setelah After terbuka sebelum mengisi username dan password
    time.sleep(7)  # Tunggu 7 detik setelah After terbuka

    # Mengisi username dan password di After
    pyautogui.write("1002r006th")  # Mengisi username
    pyautogui.press('tab')  # Pindah ke field password
    pyautogui.write("#Bandung28")  # Mengisi password lengkap (#Bandung28)

    # Pindah ke tombol Login dan menekan tombol Login dengan Enter
    pyautogui.press('tab')  # Pindah ke tombol Login
    pyautogui.press('enter')  # Tekan Enter untuk login di aplikasi After

    # Tunggu sebentar untuk memastikan aplikasi merespons
    time.sleep(1)

# Fungsi untuk input nomor BPJS ke kedua aplikasi setelah login
def input_nomor_bpjs():
    # Mengambil input nomor BPJS dari entry widget
    nomor_bpjs = entry_nomor_bpjs.get()

    if not nomor_bpjs:
        messagebox.showerror("Error", "Nomor BPJS tidak boleh kosong!")
        return

    # Input nomor BPJS ke aplikasi Frista
    pyautogui.write(nomor_bpjs)  # Mengisi nomor BPJS
    pyautogui.press('enter')  # Menekan Enter setelah input

    # Tunggu sebentar untuk memastikan aplikasi merespons
    time.sleep(1)

    # Input nomor BPJS ke aplikasi After
    pyautogui.write(nomor_bpjs)  # Mengisi nomor BPJS
    pyautogui.press('enter')  # Menekan Enter setelah input

    # Tunggu sebentar untuk memastikan aplikasi merespons
    time.sleep(1)

    messagebox.showinfo("Sukses", "Nomor BPJS berhasil dimasukkan ke kedua aplikasi!")

# Fungsi untuk memulai proses login dan input nomor BPJS
def start_process():
    # Menambahkan feedback bahwa aplikasi sedang diproses
    progress_label.config(text="Sedang membuka aplikasi Frista dan After...")
    button_start.config(state="disabled")  # Menonaktifkan tombol selama proses berlangsung

    # Mulai thread untuk login ke aplikasi Frista dan After
    thread_frista = threading.Thread(target=login_frista)
    thread_after = threading.Thread(target=login_after)

    # Mulai kedua thread secara bersamaan
    thread_frista.start()
    thread_after.start()

    # Tunggu kedua thread selesai
    thread_frista.join()
    thread_after.join()

    # Setelah login selesai, input nomor BPJS
    input_nomor_bpjs()

    # Memberi feedback ke pengguna bahwa proses telah selesai
    progress_label.config(text="Proses selesai, masukkan nomor BPJS.")
    button_start.config(state="normal")  # Menyalakan kembali tombol

# Membuat jendela aplikasi Tkinter
root = tk.Tk()
root.title("Aplikasi Login BPJS")

# Ukuran jendela
root.geometry("400x250")

# Label untuk Nomor BPJS
label_nomor_bpjs = tk.Label(root, text="Masukkan Nomor BPJS:")
label_nomor_bpjs.pack(pady=10)

# Entry untuk input nomor BPJS
entry_nomor_bpjs = tk.Entry(root, width=30)
entry_nomor_bpjs.pack(pady=5)

# Label untuk memberi informasi status
progress_label = tk.Label(root, text="Silakan masukkan nomor BPJS dan tekan 'Mulai Proses Login'.", wraplength=300)
progress_label.pack(pady=10)

# Tombol untuk memulai proses login
button_start = tk.Button(root, text="Mulai Proses Login", command=start_process)
button_start.pack(pady=20)

# Menjalankan aplikasi
root.mainloop()
