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
        return rows[0]["jumlah"] > 0

    def register_penghuni(self, username: str, nama: str, password: str) -> dict:
        """
        Mendaftarkan akun penghuni baru.
        Asumsi kolom tabel user: user_id, username, nama, password, jenisAkun, status_akun.
        jenisAkun untuk penghuni: 'PENGHUNI' (ganti kalau di SQL kalian beda).
        status_akun: 1 = aktif, 0 = non-aktif.
        """

        if not username or not password:
            return {
                "status": "error",
                "message": "Username dan password tidak boleh kosong.",
            }

        if self._username_exists(username):
            return {
                "status": "error",
                "message": "Username sudah digunakan, pilih username lain.",
            }

        query = """
            INSERT INTO user (username, nama, password, jenisAkun, statusAkun)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (username, nama, password, "P", 1)

        rowcount = self.db.execute_update(query, params)

        if rowcount:
            return {"status": "success", "message": "Registrasi penghuni berhasil."}
        else:
            return {
                "status": "error",
                "message": "Gagal menyimpan data ke database.",
            }


    def login(self, jenisAkun: str, username: str, password: str) -> dict:
        """
        Memvalidasi login user.
        SELECT * FROM user
        WHERE username = ? AND password = ?
          AND jenisAkun = ? AND status_akun = 1;
        """

        if not username or not password:
            return {
                "status": "error",
                "message": "Username/password tidak boleh kosong.",
            }

        query = """

            SELECT user_id, username, nama, jenisAkun, statusAkun
            FROM user
            WHERE username   = %s
              AND password   = %s
              AND jenisAkun = %s
              AND statusAkun = 1

            LIMIT 1
        """
        params = (username, password, jenisAkun)

        rows = self.db.execute_query(query, params)

        if not rows:
            return {
                "status": "error",
                "message": "Login gagal. Cek username, password, atau role.",
            }

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
        Menonaktifkan akun penghuni.
        FIX: Menggunakan statusAkun = 0 (bukan status_akun)
        """
        if not username:
            return {"status": "error", "message": "Username tidak boleh kosong."}

        # Perhatikan nama kolom 'statusAkun'
        query = """
            UPDATE user
            SET statusAkun = 0
            WHERE username = %s
        """
        params = (username,)

        rowcount = self.db.execute_update(query, params)

        if rowcount:
            return {
                "status": "success",
                "message": f"Akun penghuni '{username}' berhasil dinonaktifkan.",
            }
        else:
            return {
                "status": "error",
                "message": f"Gagal menonaktifkan akun '{username}' (atau akun tidak ditemukan).",
            }
    def get_all_penghuni(self) -> list:
        """
        Mengambil daftar semua penghuni.
        PENTING: Kita menggunakan alias 'statusAkun' agar sesuai dengan kode UI.
        """
        query = """
            SELECT 
                u.user_id, 
                u.username, 
                u.nama, 
                u.statusAkun,  -- Pastikan nama kolom ini sesuai dengan tabel user Anda
                p.nomor_kamar 
            FROM user u
            LEFT JOIN penghuni p ON u.user_id = p.user_id
            WHERE u.jenisAkun IN ('P', 'PENGHUNI')
            ORDER BY u.nama ASC
        """
        return self.db.execute_query(query)