from .db_manager import DatabaseManager
from pymysql.constants import ER 
import pymysql.cursors

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

    def register_penghuni_complete(self, data: dict) -> dict:
        """
        Menyimpan data ke tabel 'user' DAN 'penghuni' dalam satu transaksi.
        """
        username = data['username']
        
        # 1. Cek Username
        if self._username_exists(username):
            return {"status": "error", "message": "Username sudah digunakan!"}

        conn = self.db.get_connection()
        if not conn:
            return {"status": "error", "message": "Gagal terhubung ke database."}

        try:
            # Mulai Transaksi
            conn.begin() 
            
            with conn.cursor() as cursor:
                # A. Insert ke tabel USER
                query_user = """
                    INSERT INTO user (username, nama, password, jenisAkun, statusAkun)
                    VALUES (%s, %s, %s, 'P', 1)
                """
                cursor.execute(query_user, (data['username'], data['nama'], data['password']))
                
                # Ambil ID user yang baru saja dibuat
                user_id = cursor.lastrowid

                # B. Insert ke tabel PENGHUNI
                query_penghuni = """
                    INSERT INTO penghuni (user_id, nomor_kamar, tanggal_masuk, 
                                          harga_kamar, nomor_telepon, alamat_asal)
                    VALUES (%s, %s, %s, %s, %s, '')
                """
                # Pastikan urutan parameter sesuai dengan %s di query
                cursor.execute(query_penghuni, (
                    user_id, 
                    data['nomor_kamar'], 
                    data['tanggal_masuk'], 
                    data['harga'],
                    data['telepon']
                ))

            # Jika kedua insert berhasil, simpan permanen
            conn.commit()
            return {"status": "success", "message": f"Penghuni {data['nama']} berhasil didaftarkan."}

        except pymysql.Error as err:
            conn.rollback() # Batalkan jika ada error
            return {"status": "error", "message": f"Database Error: {err}"}
        finally:
            cursor.close()
            conn.close()

    def login(self, jenis_akun: chr, username: str, password: str) -> dict:
        """
        Memvalidasi login user.
        SELECT * FROM user
        WHERE username = ? AND password = ?
          AND jenis_akun = ? AND status_akun = 1;
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
        params = (username, password, jenis_akun)

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
                "jenis_akun": user["jenisAkun"],
            },
        }

    def nonaktifkan_akun_penghuni(self, username: str) -> dict:
        raise NotImplementedError(
            "UC03 (nonaktif akun) belum diimplementasikan."
        )