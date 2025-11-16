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

   Perintah ini akan memasang `pyautogui`, `pygetwindow`, serta `opencv-python` dan `pyzbar` yang diperlukan untuk
   fitur pemindaian barcode BPJS.

## Konfigurasi

Semua konfigurasi dasar berada di `config.conf`. Anda dapat mengubah lokasi executable, kredensial, dan pengaturan lain langsung di file tersebut atau menggunakan environment variable berikut:

- `FRISTA_PASSWORD`
- `AFTER_PASSWORD`

Pastikan jalur executable (`path`) sesuai dengan lokasi instalasi Frista dan After di mesin Anda. Jika aplikasi membutuhkan direktori kerja tertentu agar dapat berjalan (misalnya Frista berada di `D:\BPJS\Frista`), atur juga nilai `working_dir`. Contoh konfigurasi dapat dilihat di bagian `[Frista]` dan `[After]` pada berkas. Untuk memanfaatkan pemindaian barcode, aktifkan bagian `[Scanner]`, sesuaikan `camera_id`, serta atur `scan_timeout` sesuai kebutuhan lapangan.

## Menjalankan Aplikasi

Setelah dependensi terpasang dan konfigurasi diatur, jalankan aplikasi dengan:

```powershell
python main.py
```

Antarmuka Tkinter akan memandu Anda menjalankan automasi Frista terlebih dahulu, kemudian After, dan akhirnya memasukkan nomor BPJS sesuai urutan yang disarankan. Setelah kedua aplikasi siap, tekan tombol "Scan Barcode" bila ingin mengisi nomor secara otomatis menggunakan kamera. Arahkan kartu BPJS ke kamera hingga terbaca atau tekan `Q` untuk membatalkan pemindaian, lalu lanjutkan input manual jika diperlukan.

Menu utama di bagian atas kini juga memiliki menu khusus "Kontrol Frista" sehingga opsi "Selesai Verifikasi", "Sembunyikan Frista", dan "Tutup Frista" dapat dijalankan dari mana saja tanpa menggulir ke langkah empat. Setelah proses verifikasi wajah di Frista selesai dan popup "Hasil Pengenalan Wajah" muncul, gunakan tombol atau menu "Selesai Verifikasi di Frista" agar popup tertutup secara otomatis, aplikasi Frista diminimalkan, dan antarmuka APM kembali ke posisi paling depan. Tombol tambahan "Sembunyikan Frista" dan "Tutup Frista" juga tersedia di langkah ini maupun di menu tersebut sehingga operator bisa langsung meminimalkan atau menutup jendela Frista dari aplikasi utama tanpa perlu berpindah layar. Pilihan sumber input nomor booking kini tersedia (manual, webcam laptop, atau scanner eksternal) sehingga petugas dapat menyesuaikan perangkat yang digunakan di lapangan.

## Catatan Tambahan

- Automasi bergantung pada judul jendela dan tata letak aplikasi bawaan. Jika Frista atau After diperbarui, Anda mungkin perlu menyesuaikan pengaturan `window_title` atau alur login.
- `pyautogui` memerlukan akses ke layar utama. Jangan meminimalkan aplikasi saat automasi berjalan agar fokus jendela tetap terjaga.
