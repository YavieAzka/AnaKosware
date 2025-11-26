from database.db_manager import DatabaseManager

class VerificationService:
    def __init__(self):
        self.db = DatabaseManager()

    def get_pending_payments(self):
        """
        Mengambil daftar pembayaran yang menunggu verifikasi untuk ditampilkan di Dashboard Pemilik.
        Join dengan tabel user untuk mendapatkan nama pembayar.
        """
        query = """
        SELECT 
            p.pembayaran_id,
            u.nama AS nama_penghuni,
            p.bulan_tagihan,
            p.nominal_pembayaran,
            p.tanggal_bayar,
            p.bukti_pembayaran
        FROM pembayaran p
        JOIN user u ON p.user_id = u.user_id
        WHERE p.status_pembayaran = 'Belum diverifikasi'
        ORDER BY p.tanggal_bayar ASC
        """
        return self.db.execute_query(query)

    def process_verification(self, pembayaran_id, is_accepted, rejection_reason=None):
        """
        Memproses keputusan pemilik: Terima (Accept) atau Tolak (Decline).
        sekaligus menjadi mekanisme 'Notifikasi' ke user (User akan melihat status baru).
        """
        if is_accepted:
            new_status = 'Sudah diverifikasi'
            is_valid = True
            pesan_log = "Pembayaran DITERIMA."
        else:
            new_status = 'Tidak valid'
            is_valid = False
            pesan_log = f"Pembayaran DITOLAK. Alasan: {rejection_reason}"

        # Query Update
        query = """
        UPDATE pembayaran 
        SET status_pembayaran = %s,
            is_bukti_valid = %s
        WHERE pembayaran_id = %s
        """
        
        # Konversi True/False python ke 1/0 untuk MySQL
        params = (new_status, 1 if is_valid else 0, pembayaran_id)
        
        result = self.db.execute_update(query, params)

        if result:
            return {"status": "success", "message": pesan_log, "new_status": new_status}
        else:
            return {"status": "error", "message": "Gagal mengupdate database."}