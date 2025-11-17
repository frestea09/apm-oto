# Demo Alur Aplikasi dengan AutoIt

Folder ini berisi contoh sederhana bagaimana memanfaatkan AutoIt untuk
mengarahkan alur aplikasi: membuka aplikasi pertama (misal "Frista"),
menutupnya setelah selesai, lalu melanjutkan ke aplikasi utama.

## Kenapa AutoIt?
- **Otomatisasi GUI Windows**: AutoIt unggul untuk mengendalikan jendela,
  klik, dan input keyboard secara langsung di aplikasi Windows.
- **Ringan & portabel**: Script dapat dikompilasi menjadi `.exe` kecil
  yang mudah dijalankan pengguna, termasuk orang tua yang kurang familiar
  dengan terminal atau perintah khusus.
- **Sintaks sederhana**: Struktur mirip BASIC sehingga mudah dibaca dan
  dipelajari.

## Perbandingan singkat
- **Dibanding Python + pywinauto/win32**: AutoIt lebih siap pakai untuk
  kontrol GUI dasar tanpa perlu pemasangan pustaka tambahan, meski Python
  lebih fleksibel untuk logika kompleks dan integrasi web/API.
- **Dibanding PowerShell**: PowerShell kuat untuk administrasi sistem,
  namun AutoIt biasanya lebih nyaman untuk interaksi GUI granular
  (koordinat klik, kontrol dialog).

## Gambaran alur
1. Menjalankan aplikasi pertama (placeholder: "Frista").
2. Menunggu jendela aplikasinya aktif.
3. Menutup aplikasi pertama saat tugas selesai.
4. Membuka aplikasi utama.
5. Menampilkan pesan sederhana agar pengguna mengetahui aplikasi siap
   digunakan.

## Cara memakai contoh ini
1. Ubah path aplikasi di `launch_flow.au3` agar sesuai dengan lokasi
   executable Anda.
2. Pastikan judul jendela (`WinWaitActive`/`WinClose`) cocok dengan judul
   sebenarnya di layar.
3. Kompilasi script menjadi `.exe` melalui AutoIt SciTE (Compile Script)
   agar mudah dibuka pengguna lanjut usia.
4. Letakkan `.exe` di folder bersama shortcut/ikon besar agar mudah
   diklik.

## Tips aksesibilitas untuk pengguna lanjut usia
- Buat shortcut di desktop dengan ikon besar dan nama jelas, misalnya
  "Buka Frista lalu Aplikasi Utama".
- Tambahkan pesan dialog sederhana seperti di contoh script agar mereka
  tahu langkah berikutnya.
- Pastikan urutan otomatis berhenti dengan aman jika aplikasi tidak
  ditemukan; Anda bisa menambah `If Not FileExists(...) Then MsgBox(...)`
  untuk memberi tahu pengguna.
- Jika butuh jeda lebih lama, naikkan nilai `Sleep` atau tambahkan
  `WinWaitActive` tambahan pada dialog tertentu.

## File dalam folder ini
- `launch_flow.au3`: Script AutoIt contoh alur aplikasi.

