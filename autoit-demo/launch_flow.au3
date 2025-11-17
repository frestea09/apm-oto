; Demo alur: buka Frista, tutup, lalu buka aplikasi utama
; Sesuaikan path dan judul jendela agar cocok dengan instalasi Anda

#include <MsgBoxConstants.au3>

; ---- Konfigurasi pengguna ----
Global $gFristaPath   = "C:\\Program Files\\Frista\\frista.exe"
Global $gMainAppPath  = "C:\\Program Files\\AplikasiUtama\\aplikasi_utama.exe"
Global $gFristaWindow = "Frista"          ; Judul jendela Frista
Global $gMainWindow   = "Aplikasi Utama"  ; Judul jendela aplikasi utama

; ---- Langkah 1: buka aplikasi pertama ----
If Not FileExists($gFristaPath) Then
    MsgBox($MB_ICONERROR, "File tidak ditemukan", "Tidak bisa menemukan Frista di " & $gFristaPath)
    Exit
EndIf

Run($gFristaPath)
WinWaitActive($gFristaWindow, "", 10) ; timeout 10 detik

; Tambahkan jeda jika aplikasi butuh waktu inisialisasi
Sleep(1000)

; ---- Langkah 2: tutup aplikasi pertama setelah selesai ----
WinClose($gFristaWindow)

; Pastikan jendela benar-benar tertutup sebelum lanjut
WinWaitClose($gFristaWindow, "", 10)

; ---- Langkah 3: buka aplikasi utama ----
If Not FileExists($gMainAppPath) Then
    MsgBox($MB_ICONERROR, "File tidak ditemukan", "Tidak bisa menemukan aplikasi utama di " & $gMainAppPath)
    Exit
EndIf

Run($gMainAppPath)
WinWaitActive($gMainWindow, "", 10)

; ---- Langkah 4: beri tahu pengguna ----
MsgBox($MB_ICONINFORMATION, "Siap", "Aplikasi utama siap digunakan. Klik OK untuk mulai.")
