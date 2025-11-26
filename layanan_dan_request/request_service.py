from typing import List, Optional
# Pastikan import path model & database benar
from .request import Request 
from .layanan import Layanan
from database.db_manager import DatabaseManager
from .layanan_service import LayananService 

class RequestService:

    def __init__(self, db: DatabaseManager, layanan_service: LayananService):
        self.db = db
        self.layanan_service = layanan_service

    def create_request(self, user_id: int, nama_layanan: str, catatan: str = "") -> dict:
        """
        Membuat request layanan baru.
        Mencari layanan_id berdasarkan nama, lalu insert ke tabel request.
        """
        # 1. Cari ID Layanan berdasarkan Nama
        layanan = self.layanan_service.get_layanan_by_nama(nama_layanan)
        
        if not layanan:
            return {"status": "error", "message": f"Layanan '{nama_layanan}' tidak ditemukan di sistem."}

        # 2. Query Insert (Sesuai Skema Database + kolom catatan jika ada)
        # Asumsi: Tabel request punya kolom: request_id, user_id, layanan_id, tanggal_request, status_bayar, status_request
        # Kita gunakan CURDATE() untuk tanggal_request
        
        query = """
            INSERT INTO request (user_id, layanan_id, tanggal_request, status_bayar, status_request, catatan)
            VALUES (%s, %s, CURDATE(), 'Belum Dibayar', 'Pending', %s)
        """
        
        # Catatan: Jika tabel Anda belum ada kolom 'catatan', hapus bagian ', catatan' dan parameter terakhir.
        params = (user_id, layanan.id, catatan)

        try:
            last_id = self.db.execute_update(query, params)
            if last_id:
                return {"status": "success", "message": "Request berhasil dibuat!", "id": last_id}
            else:
                return {"status": "error", "message": "Gagal menyimpan request ke database."}
        except Exception as e:
            print(f"Error create_request: {e}")
            return {"status": "error", "message": str(e)}

    # ... (Sisa method get/update biarkan seperti sebelumnya atau sesuaikan jika perlu)