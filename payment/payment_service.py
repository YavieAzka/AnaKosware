import os
import shutil
from datetime import datetime
from database.db_manager import DatabaseManager

class PaymentService:
    def __init__(self):
        self.db = DatabaseManager()
        # Tentukan lokasi penyimpanan bukti bayar
        self.upload_dir = os.path.join(os.getcwd(), "uploads", "bukti_bayar")
        
        # Buat folder jika belum ada (Penting agar tidak error saat pertama kali run)
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def process_monthly_payment(self, user_id, nominal, file_path_asal):
        """
        Menangani pembayaran tagihan bulanan:
        1. Rename & Copy file gambar ke folder lokal sistem.
        2. Insert data ke database.
        """
        # Validasi File
        if not os.path.exists(file_path_asal):
            return {"status": "error", "message": "File gambar tidak ditemukan."}

        try:
            # File Handling
            # Buat nama file unik: bukti_USERID_TIMESTAMP.jpg
            file_ext = os.path.splitext(file_path_asal)[1] # Ambil ekstensi (.jpg/.png)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"bukti_{user_id}_{timestamp}{file_ext}"
            destination_path = os.path.join(self.upload_dir, new_filename)

            # Copy file dari sumber ke folder uploads proyek
            shutil.copy2(file_path_asal, destination_path)
            
            # Simpan path relatif untuk database (agar portable)
            db_file_path = f"uploads/bukti_bayar/{new_filename}"

            # Persiapan Data Waktu
            today = datetime.now()
            
            # Insert ke Database
            
            query = """
                INSERT INTO pembayaran (
                    user_id, 
                    jenis_pembayaran, 
                    request_id, 
                    bulan_tagihan, 
                    tahun_tagihan,
                    status_pembayaran, 
                    tanggal_bayar, 
                    nominal_pembayaran, 
                    bukti_pembayaran,
                    is_bukti_valid
                ) VALUES (%s, 'TAGIHAN', NULL, %s, %s, 'Belum diverifikasi', %s, %s, %s, FALSE)
            """
            
            params = (
                user_id, 
                today.month, 
                today.year, 
                today.date(), 
                nominal, 
                db_file_path
            )
            
            result = self.db.execute_update(query, params)

            if result:
                return {
                    "status": "success", 
                    "message": "Pembayaran berhasil dikirim. Menunggu verifikasi.",
                    "file_saved_at": destination_path
                }
            else:
                return {"status": "error", "message": "Gagal menyimpan data ke database."}

        except Exception as e:
            return {"status": "error", "message": f"Terjadi kesalahan sistem: {str(e)}"}