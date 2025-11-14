# APM Automation Helper

Aplikasi ini membantu operator APM untuk mengotomasi proses login dan input nomor BPJS pada aplikasi Frista dan After di lingkungan Windows.

## Persyaratan Sistem

- Windows 10/11 dengan akses ke aplikasi Frista dan After.
- Python 3.10 atau lebih baru terpasang di mesin APM.
- Kredensial login Frista dan After yang valid.

## Instalasi Dependensi

Langkah-langkah di bawah ini menggantikan konsep `npm install` pada proyek JavaScript.

1. Buka Command Prompt atau PowerShell di folder proyek.
2. (Opsional tetapi direkomendasikan) Buat lingkungan virtual Python:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   Jika menggunakan Command Prompt:

   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

3. Instal dependensi Python yang dibutuhkan oleh automasi:

   ```powershell
   pip install -r requirements.txt
   ```

   Perintah ini akan memasang `pyautogui` dan `pygetwindow` yang digunakan untuk mengontrol UI Frista dan After.

## Konfigurasi

Semua konfigurasi dasar berada di `config.conf`. Anda dapat mengubah lokasi executable, kredensial, dan pengaturan lain langsung di file tersebut atau menggunakan environment variable berikut:

- `FRISTA_PASSWORD`
- `AFTER_PASSWORD`

Pastikan jalur executable (`path`) sesuai dengan lokasi instalasi Frista dan After di mesin Anda. Contoh konfigurasi dapat dilihat di bagian `[Frista]` dan `[After]` pada berkas.

## Menjalankan Aplikasi

Setelah dependensi terpasang dan konfigurasi diatur, jalankan aplikasi dengan:

```powershell
python main.py
```

Antarmuka Tkinter akan memandu Anda menjalankan automasi Frista terlebih dahulu, kemudian After, dan akhirnya memasukkan nomor BPJS sesuai urutan yang disarankan.

## Catatan Tambahan

- Automasi bergantung pada judul jendela dan tata letak aplikasi bawaan. Jika Frista atau After diperbarui, Anda mungkin perlu menyesuaikan pengaturan `window_title` atau alur login.
- `pyautogui` memerlukan akses ke layar utama. Jangan meminimalkan aplikasi saat automasi berjalan agar fokus jendela tetap terjaga.
