from database.db_manager import DatabaseManager
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.db = DatabaseManager()

    def get_monthly_bill_notification(self, user_id):
        """
        Mengecek apakah user perlu mendapat notifikasi tagihan bulan ini.
        Mengembalikan Dictionary berisi pesan dan nominal, atau None jika aman.
        """
        today = datetime.now()
        current_month = today.month
        current_year = today.year

        # Ambil Data Penghuni (Harga Kamar & Tanggal Jatuh Tempo)
        query_penghuni = """
        SELECT harga_kamar, tanggal_jatuh_tempo, nama 
        FROM penghuni 
        JOIN user ON penghuni.user_id = user.user_id
        WHERE penghuni.user_id = %s
        """
        penghuni = self.db.execute_query(query_penghuni, (user_id,))

        if not penghuni:
            return {"status": "error", "message": "Data penghuni tidak ditemukan."}
        
        penghuni_data = penghuni[0] # Ambil row pertama
        harga_kamar = penghuni_data['harga_kamar']
        
        # Mengambil tnggal saja (misal tgl 10), mengabaikan bulan/tahun dari data master
        tgl_jatuh_tempo = penghuni_data['tanggal_jatuh_tempo'].day 
        
        # Tentukan Tanggal Jatuh Tempo BULAN INI
        # Handle edge case: jika Februari tidak punya tgl 30, gunakan tgl terakhir bulan itu
        try:
            due_date_this_month = datetime(current_year, current_month, tgl_jatuh_tempo)
        except ValueError:
            # Jika error (misal tgl 31 di bulan yg cuma 30 hari), set ke hari terakhir bulan berjalan
            import calendar
            last_day = calendar.monthrange(current_year, current_month)[1]
            due_date_this_month = datetime(current_year, current_month, last_day)

        # apakah sudah bayar bulan ini?
        #  tabel pembayaran dengan filter bulan & tahun
        query_cek_bayar = """
        SELECT status_pembayaran, is_bukti_valid 
        FROM pembayaran 
        WHERE user_id = %s 
          AND jenis_pembayaran = 'TAGIHAN' 
          AND bulan_tagihan = %s 
          AND tahun_tagihan = %s
        LIMIT 1
        """
        payment = self.db.execute_query(query_cek_bayar, (user_id, current_month, current_year))

        # --- LOGIKA NOTIFIKASI ---
        
        # Skenario A: Sudah bayar dan Valid (Lunas)
        if payment and payment[0]['status_pembayaran'] == 'Sudah diverifikasi':
            return {
                "type": "info",
                "message": "Tagihan bulan ini LUNAS.",
                "nominal": 0,
                "is_due": False
            }
        
        # Skenario B: Sedang menunggu verifikasi
        if payment and payment[0]['status_pembayaran'] == 'Belum diverifikasi':
             return {
                "type": "warning",
                "message": "Pembayaran sedang diverifikasi pemilik.",
                "nominal": harga_kamar,
                "is_due": False
            }

        # Skenario C: Belum bayar atau Ditolak (Perlu Bayar)
        # Hitung selisih hari
        days_diff = (due_date_this_month - today).days

        # Tampilkan notifikasi jika H-7 atau sudah lewat (negatif)
        if days_diff <= 7:
            if days_diff < 0:
                pesan = f"TERLAMBAT {abs(days_diff)} hari! Segera bayar tagihan."
                tipe = "danger"
            elif days_diff == 0:
                pesan = "HARI INI adalah batas pembayaran kos."
                tipe = "warning"
            else:
                pesan = f"Tagihan jatuh tempo dalam {days_diff} hari."
                tipe = "info"

            return {
                "type": tipe,
                "message": pesan,
                "nominal": harga_kamar,
                "detail_tanggal": due_date_this_month.strftime("%d-%m-%Y"),
                "is_due": True # Flag untuk mengaktifkan tombol "Bayar" di UI
            }
        
        # Skenario D: Belum waktunya bayar (masih lama)
        return None