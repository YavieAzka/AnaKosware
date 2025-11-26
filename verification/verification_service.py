from database.db_manager import DatabaseManager

class VerificationService:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_transactions(self):
        """
        Mengambil semua transaksi (Tagihan & Layanan) dengan detail User.
        """
        query = """
            SELECT 
                p.pembayaran_id,
                p.tanggal_bayar,
                u.nama AS nama_penghuni,
                u.username,
                COALESCE(penghuni.nomor_kamar, '-') AS nomor_kamar,
                p.jenis_pembayaran,
                p.nominal_pembayaran,
                p.status_pembayaran,
                p.bukti_pembayaran,
                p.bulan_tagihan,
                p.tahun_tagihan,
                l.nama_layanan
            FROM pembayaran p
            JOIN user u ON p.user_id = u.user_id
            LEFT JOIN penghuni ON p.user_id = penghuni.user_id
            LEFT JOIN request r ON p.request_id = r.request_id
            LEFT JOIN layanan l ON r.layanan_id = l.layanan_id
            ORDER BY p.tanggal_bayar DESC
        """
        return self.db.execute_query(query)

    def verify_payment(self, payment_id, is_valid):
        """
        Update status pembayaran DAN lunasi tagihan layanan terkait jika valid.
        is_valid: True (Terima), False (Tolak)
        """
        # 1. Tentukan Status Baru untuk Tabel Pembayaran
        new_status = "Sudah diverifikasi" if is_valid else "Ditolak"
        valid_flag = 1 if is_valid else 0
        
        try:
            # 2. Update Tabel Pembayaran
            query_pay = """
                UPDATE pembayaran 
                SET status_pembayaran = %s, is_bukti_valid = %s 
                WHERE pembayaran_id = %s
            """
            update_success = self.db.execute_update(query_pay, (new_status, valid_flag, payment_id))

            # 3. LOGIKA TAMBAHAN: JIKA VALID, LUNASI SEMUA REQUEST PENGHUNI TERSEBUT
            if is_valid and update_success:
                # A. Cari tahu siapa user pemilik pembayaran ini
                q_user = "SELECT user_id FROM pembayaran WHERE pembayaran_id = %s"
                res_user = self.db.execute_query(q_user, (payment_id,))
                
                if res_user:
                    # Handle hasil dict atau tuple tergantung konfigurasi DB Manager
                    user_data = res_user[0]
                    user_id = user_data.get('user_id') if isinstance(user_data, dict) else user_data[0]

                    # B. Update semua request 'Belum Dibayar' milik user ini menjadi 'Sudah Dibayar'
                    # Karena asumsinya user membayar TOTAL tagihan (Sewa + Layanan)
                    q_lunas = """
                        UPDATE request 
                        SET status_bayar = 'Sudah Dibayar' 
                        WHERE user_id = %s AND status_bayar = 'Belum Dibayar'
                    """
                    self.db.execute_update(q_lunas, (user_id,))
            
            return True

        except Exception as e:
            print(f"Verification Error: {e}")
            return False