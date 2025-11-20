import json
from typing import List
from db_manager import DatabaseManager
from layanan import Layanan


class LayananService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    # Membuat layanan baru
    def create_layanan(self, nama: str, deskripsi: str,
                       harga: float, kebutuhan: list[str]) -> Layanan | None:
        
        # Cek apakah nama layanan sudah dipakai
        if self.get_layanan_by_nama(nama) is not None:
            return None

        # Buat ID baru berdasarkan MAX(id)
        query = "SELECT COALESCE(MAX(id), 0) + 1 FROM layanan"
        new_id = self.db.execute_query(query)[0][0]

        # Insert ke database
        query = """
            INSERT INTO layanan (id, nama, deskripsi, harga, kebutuhan)
            VALUES (%s, %s, %s, %s, %s)
        """

        params = (
            new_id,
            nama,
            deskripsi,
            harga,
            json.dumps(kebutuhan)   # Simpan sebagai JSON string
        )

        result = self.db.execute_update(query, params)
        if not result:
            return None
        
        return Layanan(new_id, nama, deskripsi, harga, kebutuhan)

    # Membaca berdasarkan ID
    def get_layanan_by_id(self, id: int) -> Layanan | None:
        query = "SELECT * FROM layanan WHERE id = %s"
        data = self.db.execute_query(query, (id,))

        if not data:
            return None

        row = data[0]
        return Layanan(
            id = row[0],
            nama = row[1],
            deskripsi = row[2],
            harga = row[3],
            kebutuhan = json.loads(row[4])
        )

    # Membaca berdasarkan nama
    def get_layanan_by_nama(self, nama: str) -> Layanan | None:
        query = "SELECT * FROM layanan WHERE LOWER(nama) = LOWER(%s)"
        data = self.db.execute_query(query, (nama.strip(),))

        # Cek kalau query gagal (False), None, atau kosong
        if data is False or data is None:
            return None

        if not isinstance(data, list) or len(data) == 0:
            return None

        row = data[0]
        return Layanan(
            id=row[0],
            nama=row[1],
            deskripsi=row[2],
            harga=row[3],
            kebutuhan=json.loads(row[4]) if row[4] else []
        )

    # Update layanan
    def update_layanan(self, id: int, nama: str | None = None, 
                       deskripsi: str | None = None,
                       harga: float | None = None,
                       kebutuhan: list[str] | None = None) -> bool:

        layanan = self.get_layanan_by_id(id)
        if layanan is None:
            return False

        # Ganti field yang diisi user saja
        new_nama = nama if nama is not None else layanan.nama
        new_desc = deskripsi if deskripsi is not None else layanan.deskripsi
        new_harga = harga if harga is not None else layanan.harga
        new_kebutuhan = kebutuhan if kebutuhan is not None else layanan.kebutuhan

        query = """
            UPDATE layanan
            SET nama = %s, deskripsi = %s, harga = %s, kebutuhan = %s
            WHERE id = %s
        """

        params = (
            new_nama,
            new_desc,
            new_harga,
            json.dumps(new_kebutuhan),
            id
        )

        return self.db.execute_update(query, params)

    # Delete layanan
    def delete_layanan(self, id: int) -> bool:
        query = "DELETE FROM layanan WHERE id = %s"
        return self.db.execute_update(query, (id,))

    # Mendapatkan semua layanan
    def get_all_layanan(self) -> list[Layanan]:
        query = "SELECT * FROM layanan ORDER BY id"
        rows = self.db.execute_query(query)

        hasil = []
        for row in rows:
            hasil.append(Layanan(
                id=row[0],
                nama=row[1],
                deskripsi=row[2],
                harga=row[3],
                kebutuhan=json.loads(row[4])
            ))
        return hasil

    # Validasi ID
    def is_id_valid(self, id: int) -> bool:
        return self.get_layanan_by_id(id) is None
