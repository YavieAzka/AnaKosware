# logic_controller.py
# Modul ini berisi semua logika bisnis dan kueri database untuk AnaKosware.

# Impor manajer database yang sudah kita buat
try:
    from .db_manager import DatabaseManager
except ImportError:
    from db_manager import DatabaseManager

class LogicController:
    """
    Kelas ini menangani semua operasi logika bisnis, 
    bertindak sebagai perantara antara UI dan DatabaseManager.
    """
    
    def __init__(self):
        # Dapatkan instance singleton dari DatabaseManager
        self.db = DatabaseManager()

    def get_dashboard_penghuni(self, search_keyword=None, status_filter=None):
        """
        Mengambil data penghuni untuk Dashboard (UC08).
        Ini menangani 'loadDatabasePenghuni', 'searchData', dan 'sortByStatus'.
        
        :param search_keyword: String untuk pencarian (opsional)
        :param status_filter: Boolean (True/False) untuk filter status (opsional)
        :return: List dictionary data penghuni, atau None jika gagal.
        """
        
        # Kueri SQL dasar (sesuai I-02 dan skema yang direvisi)
        # Kita JOIN 'user' dan 'penghuni'
        base_query = """
        SELECT 
            u.user_id,
            u.username,
            u.nama AS nama_lengkap,
            u.statusAkun,
            p.nomor_kamar,
            p.tanggal_masuk,
            p.harga_kamar
        FROM 
            user u
        JOIN 
            penghuni p ON u.user_id = p.user_id
        WHERE 
            u.jenisAkun = 'H' 
        """
        
        params = []
        
        # Menangani filter pencarian (UC08 - searchData)
        if search_keyword:
            # Mencari di username, nama, atau nomor kamar
            base_query += " AND (u.username LIKE %s OR u.nama LIKE %s OR p.nomor_kamar LIKE %s)"
            search_pattern = f"%{search_keyword}%"
            params.extend([search_pattern, search_pattern, search_pattern])

        # Menangani filter status (UC08 - sortByStatus)
        if status_filter is not None: # Memeriksa "is not None" agar bisa memfilter "False"
            base_query += " AND u.statusAkun = %s"
            params.append(status_filter)
            
        base_query += " ORDER BY p.nomor_kamar ASC;"
        
        # Eksekusi kueri
        data = self.db.execute_query(base_query, tuple(params))
        
        # Debug
        if data is None:
            print("Error: Gagal mengambil data dashboard.")
            return []
        
        # Ubah data boolean 'statusAkun' menjadi teks yang mudah dibaca
        for row in data:
            row['status_teks'] = "Aktif" if row['statusAkun'] else "Nonaktif"
            
        return data

