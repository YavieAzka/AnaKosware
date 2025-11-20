from typing import List, Optional
from request import Request
from layanan_service import LayananService
from db_manager import DatabaseManager

class RequestService:

    def __init__(self, db: DatabaseManager, layanan_service: LayananService):
        self.db = db
        self.layanan_service = layanan_service

    # Membuat request baru
    def create_request(self, nama: str, namaLayanan: str) -> Optional[int]:

        # cek apakah layanan valid
        if self.layanan_service.get_layanan_by_nama(namaLayanan) is None:
            return None

        query = """
            INSERT INTO request (nama, nama_layanan, status_bayar_kebutuhan,
                                 status_request, bukti_bayar)
            VALUES (%s, %s, FALSE, FALSE, NULL)
            RETURNING id;
        """

        result = self.db.execute_query(query, (nama, namaLayanan))
        if result:
            return result[0][0]
        return None

    def get_request_by_id(self, id: int) -> Optional[Request]:
        query = """
            SELECT id, nama, nama_layanan, status_bayar_kebutuhan,
                   status_request, bukti_bayar
            FROM request
            WHERE id = %s
        """
        result = self.db.execute_query(query, (id,))
        return None if not result else Request(*result[0])

    def get_request_by_nama(self, nama: str) -> List[Request]:
        query = """
            SELECT id, nama, nama_layanan, status_bayar_kebutuhan,
                   status_request, bukti_bayar
            FROM request
            WHERE LOWER(nama) = LOWER(%s)
        """
        rows = self.db.execute_query(query, (nama,))
        return [Request(*r) for r in rows]

    def get_request_by_layanan(self, nama_layanan: str) -> List[Request]:
        query = """
            SELECT id, nama, nama_layanan, status_bayar_kebutuhan,
                   status_request, bukti_bayar
            FROM request
            WHERE LOWER(nama_layanan) = LOWER(%s)
        """
        rows = self.db.execute_query(query, (nama_layanan,))
        return [Request(*r) for r in rows]

    def update_status_bayar_kebutuhan(self, id: int, status: bool) -> bool:
        query = "UPDATE request SET status_bayar_kebutuhan = %s WHERE id = %s"
        return self.db.execute_update(query, (status, id))

    def update_status_request(self, id: int, status: bool) -> bool:
        query = "UPDATE request SET status_request = %s WHERE id = %s"
        return self.db.execute_update(query, (status, id))

    def update_bukti_bayar(self, id: int, path: str) -> bool:
        query = "UPDATE request SET bukti_bayar = %s WHERE id = %s"
        return self.db.execute_update(query, (path, id))

    def delete_request(self, id: int) -> bool:
        query = "DELETE FROM request WHERE id = %s"
        return self.db.execute_update(query, (id,))

    def get_info_request(self, id: int):
        req = self.get_request_by_id(id)
        if req is None:
            return None

        layanan = self.layanan_service.get_layanan_by_nama(req.namaLayanan)
        if layanan is None:
            return None

        return (layanan.deskripsi, layanan.harga, layanan.kebutuhan)
