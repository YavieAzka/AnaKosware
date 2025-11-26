from database.db_manager import DatabaseManager

class AuthService:
    def __init__(self):
        self.db = DatabaseManager()

    def _username_exists(self, username: str) -> bool:
        """
        Mengecek apakah username sudah ada di tabel user.
        """
        query = "SELECT COUNT(*) AS jumlah FROM user WHERE username = %s"
        rows = self.db.execute_query(query, (username,))
        if not rows:
            return False
        # Handle jika return dict atau tuple
        if isinstance(rows[0], dict):
            return rows[0]["jumlah"] > 0
        return rows[0][0] > 0

    def register_penghuni(self, username: str, nama: str, password: str, 
                          nomor_kamar: str, harga_kamar: int, 
                          tanggal_masuk, tanggal_jatuh_tempo, 
                          nomor_telepon: str, alamat_asal: str) -> dict:
        """
        Mendaftarkan akun penghuni baru ke tabel 'user' DAN 'penghuni'.
        """

        if not username or not password:
            return {"status": "error", "message": "Username dan password tidak boleh kosong."}

        if self._username_exists(username):
            return {"status": "error", "message": "Username sudah digunakan, pilih username lain."}

        # 1. INSERT KE TABEL USER
        query_user = """
            INSERT INTO user (username, nama, password, jenisAkun, statusAkun)
            VALUES (%s, %s, %s, %s, %s)
        """
        params_user = (username, nama, password, "P", 1)

        # execute_update di db_manager Anda mengembalikan last_row_id jika INSERT
        user_id = self.db.execute_update(query_user, params_user)

        if not user_id:
            return {"status": "error", "message": "Gagal membuat User ID."}

        # 2. INSERT KE TABEL PENGHUNI (Menggunakan user_id yang baru didapat)
        query_penghuni = """
            INSERT INTO penghuni (
                user_id, nomor_kamar, tanggal_masuk, harga_kamar, 
                tanggal_jatuh_tempo, nomor_telepon, alamat_asal
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        params_penghuni = (
            user_id, 
            nomor_kamar, 
            tanggal_masuk, 
            harga_kamar, 
            tanggal_jatuh_tempo, 
            nomor_telepon, 
            alamat_asal
        )

        try:
            result_penghuni = self.db.execute_update(query_penghuni, params_penghuni)
            
            if result_penghuni:
                return {"status": "success", "message": "Registrasi penghuni berhasil."}
            else:
                # Opsional: Hapus user yang sudah terlanjur dibuat jika insert penghuni gagal
                # self.db.execute_update("DELETE FROM user WHERE user_id = %s", (user_id,))
                return {"status": "error", "message": "User dibuat, tapi gagal menyimpan detail penghuni."}
                
        except Exception as e:
            print(f"Error Register Penghuni: {e}")
            return {"status": "error", "message": str(e)}

    def login(self, jenisAkun: str, username: str, password: str) -> dict:
        """
        Memvalidasi login user.
        """
        if not username or not password:
            return {"status": "error", "message": "Username/password tidak boleh kosong."}

        query = """
            SELECT user_id, username, nama, jenisAkun, statusAkun
            FROM user
            WHERE username = %s
              AND password = %s
              AND jenisAkun = %s
              AND statusAkun = 1
            LIMIT 1
        """
        params = (username, password, jenisAkun)

        rows = self.db.execute_query(query, params)

        if not rows:
            return {"status": "error", "message": "Login gagal. Cek username, password, atau role."}

        user = rows[0]
        return {
            "status": "success",
            "message": "Login berhasil.",
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "nama": user["nama"],
                "jenisAkun": user["jenisAkun"],
            },
        }

    def nonaktifkan_akun_penghuni(self, username: str) -> dict:
        """
        Menonaktifkan akun penghuni (Update statusAkun = 0).
        """
        if not username:
            return {"status": "error", "message": "Username tidak boleh kosong."}

        query = "UPDATE user SET statusAkun = 0 WHERE username = %s"
        params = (username,)

        rowcount = self.db.execute_update(query, params)

        if rowcount:
            return {"status": "success", "message": f"Akun penghuni '{username}' berhasil dinonaktifkan."}
        else:
            return {"status": "error", "message": f"Gagal menonaktifkan akun '{username}'."}

    def get_all_penghuni(self) -> list:
        """
        Mengambil daftar semua penghuni (Join user & penghuni).
        """
        query = """
            SELECT 
                u.user_id, 
                u.username, 
                u.nama, 
                u.statusAkun, 
                p.nomor_kamar,
                p.nomor_telepon,
                p.harga_kamar
            FROM user u
            LEFT JOIN penghuni p ON u.user_id = p.user_id
            WHERE u.jenisAkun IN ('P', 'PENGHUNI')
            ORDER BY u.nama ASC
        """
        return self.db.execute_query(query)