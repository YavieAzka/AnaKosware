

import pymysql 
import pymysql.cursors 
from pymysql.constants import ER 

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', user='root', password='kulintang8', database='anakosware_db'):
        if not hasattr(self, 'connection') or self.connection is None:
            self.db_config = {
                'host': host,
                'user': user,
                'password': password,       
                'database': database,
                'cursorclass': pymysql.cursors.DictCursor # AGAR HASILNYA SEPERTI OBJECT
            }
            self.connection = None
            self.connect()

    def connect(self):

        try:
            print("DB_MANAGER (PyMySQL): Memeriksa status koneksi...")

            if not self.connection or not self.connection.open:
                print(f"DB_MANAGER (PyMySQL): Koneksi tidak ada/tertutup. Mencoba koneksi baru ke {self.db_config['database']}...")
                self.connection = pymysql.connect(**self.db_config)
                print("DB_MANAGER (PyMySQL): Koneksi database berhasil dibuat.")
            else:
                print("DB_MANAGER (PyMySQL): Koneksi sudah ada dan aktif.")
                
        except pymysql.Error as err:
            # Menggunakan error codes dari PyMySQL
            err_code = err.args[0]
            
            if err_code == ER.ER_ACCESS_DENIED_ERROR:
                print("DB_MANAGER ERROR (PyMySQL): Username atau password database salah.")
            elif err_code == ER.ER_BAD_DB_ERROR:

                print(f"DB_MANAGER ERROR (PyMySQL): Database '{self.db_config['database']}' tidak ditemukan.")
            else:
                print(f"DB_MANAGER ERROR (PyMySQL): {err}")
            self.connection = None
            
        except Exception as e:
            print(f"DB_MANAGER ERROR (UMUM): Terjadi error tak terduga saat koneksi: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        """
        Mengeksekusi query SELECT dan mengembalikan hasilnya (fetchAll).
        """
        self.connect() # Memastikan koneksi selalu ada
        if not self.connection:
            print("Query gagal: Tidak ada koneksi database.")
            return None
            
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
            except pymysql.Error as err:
                print(f"Error saat eksekusi query: {err}")
                return None

    def execute_update(self, query, params=None):
        self.connect() # Memastikan koneksi selalu ada
        if not self.connection:
            print("Update gagal: Tidak ada koneksi database.")
            return False
            
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, params)
                self.connection.commit()
                last_row_id = cursor.lastrowid
                # Mengembalikan last_row_id jika itu INSERT, atau True jika sukses
                return last_row_id if last_row_id else True 
            except pymysql.Error as err:
                print(f"Error saat eksekusi update: {err}")
                self.connection.rollback() # Rollback jika terjadi error
                return False
    def get_connection(self):
        """
        Mengembalikan objek koneksi mentah untuk keperluan Transaksi manual.
        """
        self.connect() # Pastikan terkoneksi
        return self.connection


        