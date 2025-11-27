import os
import shutil
from datetime import datetime
from database.db_manager import DatabaseManager

class PaymentService:
    def __init__(self):
        self.db = DatabaseManager()
        # Tentukan lokasi penyimpanan bukti bayar (Path Absolut)
        self.upload_dir = os.path.join(os.getcwd(), "uploads", "bukti_bayar")
        
        # Buat folder jika belum ada
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def process_monthly_payment(self, user_id, nominal, file_path_asal):
        """
        Menangani pembayaran tagihan bulanan (TAGIHAN).
        Menyimpan bulan dan tahun tagihan saat ini ke database.
        """
        # Validasi File
        if not file_path_asal or not os.path.exists(file_path_asal):
            return {"status": "error", "message": "File gambar tidak ditemukan/valid."}

        try:
            # 1. File Handling (Rename & Copy)
            file_ext = os.path.splitext(file_path_asal)[1] # Ambil ekstensi (.jpg/.png)
            if not file_ext: file_ext = ".jpg"
            
            # Nama file unik: bukti_USERID_TIMESTAMP.jpg
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"bukti_{user_id}_{timestamp}{file_ext}"
            destination_path = os.path.join(self.upload_dir, new_filename)

            # Copy file dari sumber ke folder proyek
            shutil.copy2(file_path_asal, destination_path)
            
            # Path relatif untuk disimpan di database
            db_file_path = f"uploads/bukti_bayar/{new_filename}"

            # 2. Persiapan Data Waktu
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            current_date = now.strftime("%Y-%m-%d")

            # 3. Insert ke Database (Sesuai Skema Baru)
            query = """
                INSERT INTO pembayaran (
                    user_id, 
                    jenis_pembayaran, 
                    request_id, 
                    status_pembayaran, 
                    tanggal_bayar, 
                    nominal_pembayaran, 
                    bulan_tagihan, 
                    tahun_tagihan, 
                    bukti_pembayaran, 
                    is_bukti_valid
                ) VALUES (
                    %s, 
                    'TAGIHAN', 
                    NULL, 
                    'Belum diverifikasi', 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    '0'
                )
            """
            
            params = (
                user_id, 
                current_date, 
                nominal, 
                current_month, 
                current_year, 
                db_file_path
            )
            
            result = self.db.execute_update(query, params)

            if result:
                return {
                    "status": "success", 
                    "message": "Pembayaran berhasil dikirim. Menunggu verifikasi admin.",
                    "file_saved_at": destination_path
                }
            else:
                return {"status": "error", "message": "Gagal menyimpan data ke database."}

        except Exception as e:
            print(f"Payment Error: {e}")
            return {"status": "error", "message": f"Terjadi kesalahan sistem: {str(e)}"}
    
    def process_layanan_payment(self, user_id, request_id, nominal, file_path_asal):
        """
        Menangani pembayaran LAYANAN.
        """

        if not file_path_asal or not os.path.exists(file_path_asal):
            return {"status": "error", "message": "File gambar tidak ditemukan/valid."}

        try:
            # 1. File Handling
            file_ext = os.path.splitext(file_path_asal)[1] or ".jpg"
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"bukti_layanan_{user_id}_{timestamp}{file_ext}"
            destination_path = os.path.join(self.upload_dir, new_filename)
            shutil.copy2(file_path_asal, destination_path)

            db_file_path = f"uploads/bukti_bayar/{new_filename}"
            current_date = datetime.now().strftime("%Y-%m-%d")

            # 2. INSERT KE PEMBAYARAN → BEDA UTAMA ADA DI SINI
            query = """
                INSERT INTO pembayaran (
                    user_id,
                    jenis_pembayaran,
                    request_id,
                    status_pembayaran,
                    tanggal_bayar,
                    nominal_pembayaran,
                    bukti_pembayaran,
                    is_bukti_valid
                )
                VALUES (
                    %s,
                    'LAYANAN',
                    %s,
                    'Belum diverifikasi',
                    %s,
                    %s,
                    %s,
                    0
                )
            """

            params = (
                user_id,
                request_id,
                current_date,
                nominal,
                db_file_path
            )

            result = self.db.execute_update(query, params)

            if result:
                return {
                    "status": "success",
                    "message": "Pembayaran layanan berhasil dikirim.",
                    "file_saved_at": destination_path
                }
            else:
                return {"status": "error", "message": "Gagal menyimpan pembayaran layanan."}

        except Exception as e:
            print(f"Layanan Payment Error: {e}")
            return {"status": "error", "message": str(e)}