from datetime import datetime
from database.db_manager import DatabaseManager

class Dashboard:
    def __init__(self):
        self.db = DatabaseManager()

    def get_penghuni_dashboard_info(self, user_id: int):
        """
        UC08: Melihat Dashboard Informasi Akun Penghuni.
        Mengambil gabungan data:
        1. Profil Penghuni (Kamar, Harga, Jatuh Tempo)
        2. Status Tagihan Bulan Ini (Apakah sudah lunas?)
        """
        # 1. Ambil Data Profil & Kamar (Join User & Penghuni)
        query_profil = """
            SELECT 
                u.nama,
                u.username,
                p.nomor_kamar,
                p.harga_kamar,
                p.tanggal_jatuh_tempo,
                p.nomor_telepon
            FROM user u
            JOIN penghuni p ON u.user_id = p.user_id
            WHERE u.user_id = %s
        """
        profil_data = self.db.execute_query(query_profil, (user_id,))

        if not profil_data:
            return {"status": "error", "message": "User tidak ditemukan"}

        profil = profil_data[0]
        
        # Parsing tanggal jatuh tempo (misal: mengambil tanggalnya saja: '10')
        # Asumsi di DB disimpan sebagai Date, kita ambil hari-nya saja untuk display "Setiap tanggal X"
        tgl_tempo_db = profil['tanggal_jatuh_tempo']
        tgl_display = tgl_tempo_db.day if isinstance(tgl_tempo_db, datetime) else tgl_tempo_db

        # 2. Cek Status Pembayaran Bulan Ini
        today = datetime.now()
        query_bayar = """
            SELECT status_pembayaran 
            FROM pembayaran 
            WHERE user_id = %s 
              AND bulan_tagihan = %s 
              AND tahun_tagihan = %s 
              AND jenis_pembayaran = 'TAGIHAN'
        """
        bayar_data = self.db.execute_query(query_bayar, (user_id, today.month, today.year))

        # Tentukan status visual dashboard
        if bayar_data:
            status_tagihan = bayar_data[0]['status_pembayaran'] # "Sudah diverifikasi" / "Belum diverifikasi"
            is_lunas = (status_tagihan == "Sudah diverifikasi")
        else:
            status_tagihan = "Belum Bayar"
            is_lunas = False

        return {
            "status": "success",
            "data": {
                "welcome_msg": f"Halo, {profil['nama']}!",
                "info_kamar": {
                    "nomor": profil['nomor_kamar'],
                    "harga": profil['harga_kamar'],
                    "jadwal_bayar": f"Setiap tanggal {tgl_display}"
                },
                "info_akun": {
                    "username": profil['username'],
                    "kontak": profil['nomor_telepon']
                },
                "status_bulan_ini": {
                    "status_text": status_tagihan,
                    "is_lunas": is_lunas, # Boolean untuk mengatur warna (Hijau/Merah) di Frontend
                    "periode": f"{today.strftime('%B %Y')}"
                }
            }
        }