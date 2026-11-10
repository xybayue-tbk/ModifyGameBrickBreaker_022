# Cyber Brick Breaker

Cyber Brick Breaker adalah game Brick Breaker 2D berbasis Python dan Pygame.
Pemain menggerakkan paddle di bagian bawah layar untuk memantulkan bola dan
menghancurkan blok. Game ini menggunakan struktur berorientasi objek dan tema
warna cyberpunk.

## Daftar isi

- [Fitur](#fitur)
- [Persyaratan](#persyaratan)
- [Instalasi dan menjalankan](#instalasi-dan-menjalankan)
- [Kontrol](#kontrol)
- [Aturan permainan](#aturan-permainan)
- [Jenis blok dan skor](#jenis-blok-dan-skor)
- [Struktur program](#struktur-program)
- [Dokumentasi screenshot kode](#dokumentasi-screenshot-kode)
- [Pengaturan utama](#pengaturan-utama)
- [Pemecahan masalah](#pemecahan-masalah)

## Fitur

- Layar permainan berukuran 800 × 600 piksel dengan latar gelap.
- Paddle cyan dan bola putih.
- Empat jenis blok dengan warna, ketahanan, dan nilai skor yang berbeda.
- Susunan blok diacak setiap kali level dimulai.
- Tiga nyawa, skor, dan nomor level ditampilkan selama bermain.
- Kecepatan bola meningkat satu unit setiap kali level berhasil diselesaikan.
- Kecepatan paddle dijaga dua kali kecepatan bola.
- Game over menyediakan pilihan untuk memulai ulang atau keluar.

## Persyaratan

- Python yang kompatibel dengan `pygame-ce`.
- Dependensi proyek pada [requirements.txt](./requirements.txt).

Game ini menggunakan `pygame-ce`, distribusi Pygame Community Edition yang
tetap diimpor di dalam program dengan nama modul `pygame`.

## Instalasi dan menjalankan

Buka PowerShell di folder proyek, kemudian jalankan:

```powershell
python -m pip install -r requirements.txt
python coba.py
```

Jika menggunakan virtual environment `.venv` yang tersedia di Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\coba.py
```

Perintah pertama memasang dependensi. Perintah kedua menjalankan game. Jendela
game akan terbuka; tutup jendela tersebut untuk keluar.

## Kontrol

| Tombol | Fungsi |
| --- | --- |
| Panah kiri | Menggerakkan paddle ke kiri |
| Panah kanan | Menggerakkan paddle ke kanan |
| Spasi pada layar Game Over | Memulai permainan baru |
| `Esc` pada layar Game Over | Keluar dari permainan |
| Tombol tutup jendela | Keluar dari permainan |

Paddle tidak dapat bergerak melewati sisi kiri atau kanan layar. Tombol panah
yang ditekan akan menggerakkan paddle ke arah tersebut; gerakan berhenti saat
tombol dilepas.

## Aturan permainan

1. Bola mulai bergerak dari area bawah layar.
2. Pantulkan bola menggunakan paddle untuk mengenai blok.
3. Blok yang dapat dihancurkan mengurangi ketahanannya ketika terkena bola.
4. Hancurkan semua blok yang masih dapat dihancurkan untuk menyelesaikan level.
   Blok indestructible tidak perlu dihancurkan.
5. Setiap level baru menambah kecepatan bola satu unit dan menghasilkan susunan
   blok acak yang baru.
6. Bola yang melewati bagian bawah layar mengurangi satu nyawa dan bola
   dikembalikan ke posisi awal. Arah horizontal awal bola dipilih secara acak.
7. Permainan menampilkan layar Game Over ketika nyawa habis. Pilih Spasi untuk
   memulai ulang atau `Esc` untuk keluar.

Paddle bergerak dua kali kecepatan bola. Kecepatan tersebut dihitung dalam
pergerakan per frame; game membatasi pembaruan hingga 60 frame per detik.

## Jenis blok dan skor

| Jenis | Warna | Ketahanan awal | Nilai skor | Keterangan |
| --- | --- | ---: | ---: | --- |
| Normal | Hijau | 100 | 5 | Hancur setelah satu serangan |
| Hard | Ungu | 200 | 15 | Membutuhkan dua serangan; berubah hijau setelah serangan pertama |
| Bonus | Emas | 100 | 50 | Hancur setelah satu serangan dan memberi skor lebih tinggi |
| Indestructible | Merah | Tidak dapat dihancurkan | 0 | Tidak mengurangi ketahanan dan tidak memberi skor |

Setiap serangan mengurangi ketahanan sebesar 100. Jenis blok dipilih secara
acak dengan bobot relatif: normal 60, hard 25, indestructible 5, dan bonus 10.
Jumlah seluruh bobot adalah 100.

## Struktur program

Implementasi game berada di [coba.py](./coba.py).

### Konstanta dan objek tampilan

- `WIDTH` dan `HEIGHT` mengatur ukuran jendela.
- Konstanta warna (`BG_COLOR`, `CYAN`, `GREEN`, `PURPLE`, `RED`, `GOLD`, dan
  `WHITE`) mengatur tema dan warna objek.
- `screen`, `font`, dan `clock` adalah objek Pygame untuk menggambar, menulis
  teks, dan membatasi frame rate.
- `FPS` menetapkan batas pembaruan game menjadi 60 frame per detik.

### Fungsi

- `collisionChecker(rect, ball_rect)` memeriksa tumpang tindih dua persegi
  panjang Pygame dan mengembalikan nilai boolean.

### Kelas

#### `Block`

Mewakili satu blok. Konstruktor menerima posisi, ukuran, dan jenis blok, lalu
menentukan warna, ketahanan, dan nilai skornya. `display()` menggambar blok,
`hit()` mengurangi ketahanan jika blok dapat dihancurkan, `getRect()` memberikan
area tabrakan, dan `getHealth()` memberikan nilai ketahanan.

#### `Striker`

Mewakili paddle. `update(xFac)` menggerakkan paddle berdasarkan arah dan
kecepatannya, lalu membatasi posisinya agar tetap di dalam layar. `display()`
menggambar paddle dan `getRect()` memberikan area tabrakannya.

#### `Ball`

Mewakili bola. `update()` menggerakkan bola dan mengurus pantulan dari dinding
kiri, kanan, dan atas; metode ini mengembalikan `True` ketika bola mencapai
bagian bawah layar. `reset()` mengembalikan bola ke posisi awal, `hit()`
membalik arah vertikal bola, `display()` menggambar bola, dan `getRect()`
memberikan area tabrakannya.

#### `GameManager`

Mengelola keadaan dan alur permainan:

- `__init__()` menginisialisasi skor, nyawa, level, bola, paddle, dan blok.
- `populateBlocks()` membuat susunan blok baru dengan jenis yang diacak.
- `gameOverScreen()` menampilkan skor akhir serta pilihan mulai ulang atau
  keluar.
- `run()` menjalankan loop utama: memperbarui antarmuka, membaca input,
  memeriksa tabrakan, memperbarui keadaan permainan, menggambar objek, dan
  mengatur frame rate.

Program membuat objek `GameManager` dan memanggil `run()` hanya saat
`coba.py` dijalankan langsung. Setelah loop selesai, Pygame ditutup dengan
`pygame.quit()`.

## Dokumentasi screenshot kode

Screenshot berikut memperlihatkan bagian-bagian implementasi di `coba.py`.
Urutannya mengikuti alur dari pengaturan awal, pembuatan blok, sampai
pengelolaan permainan.

### 1. Pengaturan layar dan warna

Bagian ini menunjukkan ukuran jendela 800 × 600, palet warna tema cyberpunk,
inisialisasi tampilan Pygame, penggunaan font bawaan, dan batas permainan 60
FPS yang menjadi pengaturan awal game.

![Pengaturan layar, palet warna, font, dan FPS](<sekerengsot/Screenshot 2026-11-10 105450.png>)

### 2. Jenis dan tampilan blok

Screenshot ini memperlihatkan konstruktor `Block` menentukan warna,
ketahanan, dan nilai skor berdasarkan jenis. Cuplikan yang terlihat mencakup
inisialisasi blok normal dan hard serta awal pengaturan untuk blok bonus.

![Inisialisasi atribut kelas Block](<sekerengsot/Screenshot 2026-11-10 105627.png>)

### 3. Respons blok saat terkena bola dan kelas paddle

Screenshot ini melanjutkan konstruktor dengan pengaturan blok indestructible
(`health = -1`) dan metode `display()` yang menggambar blok aktif dengan garis
tepi. Metode `hit()` mengurangi ketahanan sebesar 100 dan mengubah blok hard
menjadi hijau setelah serangan pertama. Di bagian bawah terlihat metode akses
area tabrakan serta awal kelas `Striker`, yaitu paddle yang dikendalikan pemain.

![Metode hit pada Block dan awal kelas Striker](<sekerengsot/Screenshot 2026-11-10 105655.png>)

### 4. Inisialisasi permainan dan susunan blok acak

Kelas `GameManager` memulai permainan dengan tiga nyawa, skor nol, level
pertama, bola, dan paddle. Metode `populateBlocks()` menyusun blok pada area
atas layar; jenis blok dipilih secara acak dengan bobot normal 60, hard 25,
indestructible 5, dan bonus 10.

![Inisialisasi GameManager dan pembuatan blok acak](<sekerengsot/Screenshot 2026-11-10 105721.png>)

## Pengaturan utama

Nilai-nilai dasar permainan dapat diubah di `coba.py`:

| Pengaturan | Nilai awal | Lokasi |
| --- | ---: | --- |
| Ukuran layar | 800 × 600 | `WIDTH`, `HEIGHT` |
| Batas frame rate | 60 FPS | `FPS` |
| Nyawa awal | 3 | `GameManager.__init__()` |
| Kecepatan bola awal | 6 | Inisialisasi `Ball` |
| Kecepatan paddle | 2 × kecepatan bola | Inisialisasi dan loop `GameManager.run()` |
| Ukuran blok | 60 × 20 | `blockWidth`, `blockHeight` |
| Jarak antarblok | 15 piksel | `horizontalGap`, `verticalGap` |

Setiap kali level naik, kecepatan bola bertambah satu. Kecepatan paddle
diperbarui dari kecepatan bola pada setiap frame, sehingga perbandingan dua kali
tetap berlaku pada level berikutnya.

## Pemecahan masalah

### `ModuleNotFoundError: No module named 'pygame'`

Pastikan interpreter yang digunakan sama untuk memasang dependensi dan
menjalankan program. Pada Windows dengan `.venv`, gunakan:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\coba.py
```

### Perintah `python` tidak ditemukan

Pasang Python dan pastikan perintah `python` tersedia di PowerShell, atau
gunakan path interpreter lengkap seperti contoh `.venv` di atas.