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
        Asumsi kolom tabel user: user_id, username, nama, password, jenis_akun, status_akun.
        jenis_akun untuk penghuni: 'PENGHUNI' (ganti kalau di SQL kalian beda).
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
            INSERT INTO user (username, nama, password, jenis_akun, status_akun)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (username, nama, password, "PENGHUNI", 1)

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
            SELECT user_id, username, nama, jenisAkun, status_akun
            FROM user
            WHERE username   = %s
              AND password   = %s
              AND jenisAkun = %s
              AND status_akun = 1
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
        raise NotImplementedError(
            "UC03 (nonaktif akun) belum diimplementasikan."
        )