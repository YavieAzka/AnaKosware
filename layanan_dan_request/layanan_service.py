import json
from typing import List
# FIX: Import dari folder 'models' dan 'database' dengan benar
from .layanan import Layanan
from database.db_manager import DatabaseManager

class LayananService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create_layanan(self, nama: str, deskripsi: str, harga: float, kebutuhan: list[str]) -> Layanan | None:
        # Cek duplikat nama
        if self.get_layanan_by_nama(nama) is not None:
            return None

        # Query ID baru
        query_id = "SELECT COALESCE(MAX(layanan_id), 0) + 1 FROM layanan"
        res_id = self.db.execute_query(query_id)
        new_id = res_id[0]['COALESCE(MAX(layanan_id), 0) + 1'] if res_id else 1
        # Catatan: Sesuaikan key dictionary result dengan driver DB Anda (mysql-connector biasanya return dict)
        # Jika driver return tuple, gunakan res_id[0][0]
        # Untuk keamanan, kita pakai auto_increment database saja biasanya, tapi mengikuti logika Anda:
        
        query = """
            INSERT INTO layanan (nama_layanan, deskripsi_layanan, harga_layanan, kebutuhan_layanan, tanggal_layanan)
            VALUES (%s, %s, %s, %s, CURDATE())
        """
        # Catatan: Skema DB Anda sebelumnya pakai 'nama_layanan', 'harga_layanan', dll.
        # Saya sesuaikan query dengan CREATE TABLE di awal chat.
        
        params = (
            nama,
            deskripsi,
            harga,
            json.dumps(kebutuhan)
        )

        rowcount = self.db.execute_update(query, params)
        if not rowcount:
            return None
        
        return Layanan(new_id, nama, deskripsi, harga, kebutuhan)

    def get_all_layanan(self) -> list[Layanan]:
        # Sesuaikan query dengan nama kolom di Database (lihat skema awal)
        query = "SELECT * FROM layanan ORDER BY layanan_id"
        rows = self.db.execute_query(query)

        hasil = []
        if not rows:
            return []

        for row in rows:
            # Handle jika row adalah Dictionary (MySQL Connector default)
            # Pastikan nama kolom sesuai tabel DB: 
            # layanan_id, nama_layanan, deskripsi_layanan, harga_layanan, kebutuhan_layanan
            try:
                keb = json.loads(row['kebutuhan_layanan']) if row['kebutuhan_layanan'] else []
            except:
                keb = []

            hasil.append(Layanan(
                id=row['layanan_id'],
                nama=row['nama_layanan'],
                deskripsi=row['deskripsi_layanan'],
                harga=float(row['harga_layanan']),
                kebutuhan=keb
            ))
        return hasil

    def get_layanan_by_nama(self, nama: str) -> Layanan | None:
        query = "SELECT * FROM layanan WHERE LOWER(nama_layanan) = LOWER(%s)"
        rows = self.db.execute_query(query, (nama.strip(),))

        if not rows:
            return None
        
        row = rows[0]
        try:
            keb = json.loads(row['kebutuhan_layanan']) if row['kebutuhan_layanan'] else []
        except:
            keb = []

        return Layanan(
            id=row['layanan_id'],
            nama=row['nama_layanan'],
            deskripsi=row['deskripsi_layanan'],
            harga=float(row['harga_layanan']),
            kebutuhan=keb
        )

    def update_layanan(self, id: int, nama: str, deskripsi: str, harga: float, kebutuhan: list[str]) -> bool:
        query = """
            UPDATE layanan
            SET nama_layanan = %s, deskripsi_layanan = %s, harga_layanan = %s, kebutuhan_layanan = %s
            WHERE layanan_id = %s
        """
        params = (nama, deskripsi, harga, json.dumps(kebutuhan), id)
        return self.db.execute_update(query, params) > 0

    def delete_layanan(self, id: int) -> bool:
        query = "DELETE FROM layanan WHERE layanan_id = %s"
        return self.db.execute_update(query, (id,)) > 0