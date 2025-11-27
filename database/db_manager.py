import pymysql 
import pymysql.cursors 
from pymysql.constants import ER 

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', user='root', password='[sesuai masing-masing]', database='anakosware_db'):
        # Pastikan password di atas benar sesuai konfigurasi MySQL lokal Anda
        if not hasattr(self, 'connection') or self.connection is None:
            self.db_config = {
                'host': host,
                'user': user,
                'password': password,       
                'database': database,
                'cursorclass': pymysql.cursors.DictCursor, # Return data sebagai Dictionary
                'autocommit': False # Kita kontrol commit secara manual
            }
            self.connection = None
            self.connect()

    def connect(self):
        try:
            # Cek apakah koneksi ada dan masih terbuka (ping check)
            if self.connection:
                try:
                    self.connection.ping(reconnect=True)
                    return # Koneksi aktif, tidak perlu buat baru
                except pymysql.Error:
                    pass # Koneksi putus, lanjut buat baru

            print(f"DB_MANAGER: Menghubungkan ke database '{self.db_config['database']}'...")
            self.connection = pymysql.connect(**self.db_config)
            print("DB_MANAGER: Koneksi Berhasil.")
                
        except pymysql.Error as err:
            err_code = err.args[0]
            if err_code == ER.ER_ACCESS_DENIED_ERROR:
                print("DB_MANAGER ERROR: Username atau password database salah.")
            elif err_code == ER.ER_BAD_DB_ERROR:
                print(f"DB_MANAGER ERROR: Database '{self.db_config['database']}' tidak ditemukan.")
            else:
                print(f"DB_MANAGER ERROR: {err}")
            self.connection = None
            
        except Exception as e:
            print(f"DB_MANAGER ERROR (UMUM): {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        """
        Untuk SELECT. Mengembalikan list of dictionary atau list kosong [].
        """
        self.connect()
        if not self.connection:
            return [] # Return list kosong agar tidak error saat di-loop
            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result if result else []
        except pymysql.Error as err:
            print(f"SQL Error (SELECT): {err}")
            print(f"Query: {query}")
            return []

    def execute_update(self, query, params=None):
        """
        Untuk INSERT, UPDATE, DELETE.
        - INSERT: Mengembalikan ID baris baru (int).
        - UPDATE/DELETE: Mengembalikan jumlah baris yang berubah (int).
        - ERROR: Mengembalikan 0.
        """
        self.connect()
        if not self.connection:
            return 0
            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit() # PENTING: Simpan perubahan permanen
                
                # Jika INSERT, kembalikan ID baru
                if cursor.lastrowid:
                    return cursor.lastrowid
                
                # Jika UPDATE/DELETE, kembalikan jumlah baris (rowcount)
                # rowcount bisa 0 jika tidak ada data yang cocok/berubah, tapi itu bukan error.
                return cursor.rowcount if cursor.rowcount >= 0 else 1 
                
        except pymysql.Error as err:
            self.connection.rollback() # Batalkan jika error
            print(f"SQL Error (UPDATE/INSERT): {err}")
            return 0

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("DB_MANAGER: Koneksi ditutup.")