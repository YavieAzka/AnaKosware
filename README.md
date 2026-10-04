# IF2150-2025-K02-G05-AnaKosware
The repository for IF2150 Software Engineering final project: AnaKosware

# 🏠 AnaKosware  
Sistem Manajemen Kos Berbasis Python & PyQt6  

---

## Deskripsi Singkat

AnaKosware adalah aplikasi desktop berbasis **Python dan PyQt6** yang dikembangkan untuk mendukung sistem administrasi kos secara digital.  
Aplikasi ini menyediakan fitur:

- Sistem login multi-role (Pemilik, Penghuni, Penjaga)
- Manajemen layanan (Laundry, refill galon, dll)
- Request layanan oleh penghuni
- Pembayaran tagihan dan layanan
- Feedback penghuni terkait layanan & pengalaman
- Tampilan GUI modern berbasis PyQt6

Aplikasi ini dikembangkan sebagai bagian dari tugas besar mata kuliah ** IF2150 Rekayasa Perangkat Lunak**.

---

## Prasyarat dan Instalasi

### 1. Software yang diperlukan

| Komponen     | Minimal Versi            |
|--------------|--------------------------|
| Python       | 3.11 atau lebih baru     |
| MySQL Server | 8.x                      |
| pip          | Latest                   |
| OS Support   | Windows / Linux / MacOS  |



### 2. Instalasi Dependensi

Jalankan perintah berikut pada terminal:

```bash
pip install -r requirements.txt
````

Jika file `requirements.txt` tidak terbaca, minimal install:

```bash
pip install PyQt6 pymysql
```



### 3. Instalasi Database

Jalankan script SQL yang terdapat pada folder:

```
/database/all-table.sql
```

Atau secara manual:

```sql
CREATE DATABASE anakosware_db;
USE anakosware_db;
```

Konfigurasi database dapat ditemukan pada:

```
database/db_manager.py
```

Contoh konfigurasi:

```python
host='localhost'
user='root'
password='finalbangetfiks'
database='anakosware_db'
```

---

## ▶️ Cara Menjalankan Aplikasi

1. Pastikan **MySQL Server aktif**
2. Pastikan database sudah ter-import
3. Jalankan aplikasi melalui terminal:

```bash
python -m GUI.main_view
```

Aplikasi akan berjalan dengan tampilan GUI.

---

## Modul yang Diimplementasikan dan Penanggung Jawab

| Kode Modul | Nama Modul                                           | Penanggung Jawab                                           |
| ---------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| UC01       | Mendaftarkan Akun Penghuni                           | Helena Kristela Sarhawa                                    |
| UC02       | Login Akun                                           | Helena Kristela Sarhawa                                    |
| UC03       | Menonaktifkan Akun Penghuni                          | Helena Kristela Sarhawa                                    |
| UC04       | Mendapatkan Pengingat dan Total Tagihan Bulanan      | Yavie Azka Putra                                           |
| UC05       | Membayar Tagihan Kos                                 | Yavie Azka Putra                                           |
| UC06       | Verifikasi Pembayaran Tagihan Kos                    | Yavie Azka Putra                                           |
| UC07       | Melihat Riwayat Pembayaran Tagihan dan Layanan       | Syaqina Octavia Rhizha                                     |
| UC08       | Melihat Dashboard Informasi Akun Penghuni            | Syaqina Octavia Rizha                                      |
| UC09       | Membuat dan Mengedit Layanan Kebutuhan yang Tersedia | Reynard Anderson Wijaya                                    |
| UC10       | Mengajukan Request Layanan                           | Reynard Anderson Wijaya                                    |
| UC11       | Membayar Request Layanan                             | Reynard Anderson Wijaya                                    |
| UC12       | Menerima dan Memenuhi Request                        | Reynard Anderson Wijaya                                    |
| UC13       | Memberikan Feedback                                  | Syaqina Octavia Rizha                                      |
| UC14       | Melihat Feedback                                     | Syaqina Octavia Rizha                                      |
| -          | Desain UI/UX                                         | Keisha Rizka Syofyani & Alya Nur Rahmah                    |
| -          | GUI                                                  | Keisha Rizka Syofyani & Alya Nur Rahmah & Yavie Azka Putra |
| -          | Inisialisasi Database                                | Yavie Azka Putra                                           |
| -          | Integrasi Front-End & Backend                        | Yavie Azka Putra                                           |
| -          | Testing & Debugging                                  | Helena Kristela Sarhawa                                    |
| -          | File doc                                             | Keisha Rizka Syofyani                                      |


---

## Struktur Database

Berikut daftar tabel yang digunakan dalam sistem:

| Nama Tabel     | Atribut                                                                                                                                                                                 |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **user**       | `user_id (PK)`, `username`, `nama`, `password`, `jenisAkun`, `statusAkun`                                                                                                               |
| **penghuni**   | `user_id (PK/FK)`, `nomor_kamar`, `tanggal_masuk`, `harga_kamar`, `tanggal_jatuh_tempo`, `nomor_telepon`, `alamat_asal`                                                                 |
| **pemilik**    | `user_id (PK/FK)`, `nomor_telepon`                                                                                                                                                      |
| **penjaga**    | `user_id (PK/FK)`, `nomor_telepon`, `gaji`, `tanggal_masuk_kerja`, `tempat_tanggal_lahir`, `alamat`                                                                                     |
| **layanan**    | `layanan_id (PK)`, `tanggal_layanan`, `nama_layanan`, `deskripsi_layanan`, `kebutuhan_layanan`                                                                                          |
| **request**    | `request_id (PK)`, `user_id (FK)`, `layanan_id (FK)`, `tanggal_request`, `status_bayar`, `status_request`                                                                               |
| **feedback**   | `feedback_id (PK)`, `user_id (FK)`, `tanggal_feedback`, `isi`                                                                                                                           |
| **pembayaran** | `pembayaran_id (PK)`, `user_id (FK)`, `jenis_pembayaran`, `request_id (nullable, FK)`, `status_pembayaran`, `tanggal_bayar`, `nominal_pembayaran`, `bukti_pembayaran`, `is_bukti_valid` |

---

## Struktur Folder

```
├── AnaKosware
│   ├── dashboard.py
├── GUI
│   ├── assets
│   ├── components
│   │   ├── __pycache__
│   │   ├── _init_.py
│   │   ├── custom_widgets.py
│   │   ├── pemilik
│   │   ├── penghuni
│   │   └── penjaga
│   ├── pages
│   │   ├── __pycache__
│   │   ├── _init_.py
│   │   ├── login
│   │   ├── pemilik
│   │   ├── penghuni
│   │   └── penjaga
│   └── main_view.py
├── README.md
├── assets
├── auth
│   ├── __pycache__
│   │   └── auth_service.cpython-313.pyc
│   ├── auth_service.py
│   ├── test_uc01.py
│   └── test_uc02.py
├── database
│   ├── __pycache__
│   │   ├── db_manager.cpython-313.pyc
│   │   └── logic_controller.cpython-313.pyc
│   ├── all-table.sql
│   ├── database_query.sql
│   ├── db_manager.py
│   └── logic_controller.py
├── feedback
│   ├── __pycache__
│   │   └── feedback.cpython-313.pyc
│   └── feedback.py
├── history
│   ├── __pycache__
│   │   ├── bill_history.cpython-313.pyc
│   │   └── service_history.cpython-313.pyc
│   ├── bill_history.py
│   └── service_history.py
├── uploads
├── venv_anakosware
└── verification
└── doc
└── requirements.txt

```

