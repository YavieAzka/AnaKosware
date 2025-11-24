from typing import List, Dict, Any, Optional
from database.db_manager import DatabaseManager
from datetime import datetime

class ServiceHistory:
    def __init__(self):
        self.db = DatabaseManager()

    def get_riwayat_layanan(self, 
                            user_id: Optional[int] = None, 
                            sort_by: str = 'newest', 
                            filter_status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Mengambil data riwayat request layanan.
        Aktor: Penjaga (user_id=None) & Penghuni (user_id=int)
        """
        
        # Query dengan JOIN (Request -> User -> Penghuni -> Layanan)
        query = """
            SELECT 
                r.id AS request_id,
                r.tanggal_request,
                u.username,
                u.nama AS nama_penghuni,
                p.nomor_kamar,
                r.nama_layanan,
                l.harga AS total_harga,
                l.deskripsi,
                l.kebutuhan,
                r.status_request,
                r.status_bayar_kebutuhan,
                r.bukti_bayar
            FROM request r
            LEFT JOIN user u ON r.nama = u.nama 
            LEFT JOIN penghuni p ON u.user_id = p.user_id
            LEFT JOIN layanan l ON LOWER(r.nama_layanan) = LOWER(l.nama)
            WHERE 1=1
        """
        
        params = []

        # 1. Filter User (POV Penghuni)
        if user_id is not None:
            query += " AND u.user_id = %s"
            params.append(user_id)

        # 2. Filter Status (Proses/Selesai)
        if filter_status:
            if filter_status.lower() == 'selesai':
                query += " AND r.status_request = 1"
            elif filter_status.lower() == 'proses':
                query += " AND r.status_request = 0"

        # 3. Sorting
        if sort_by == 'username':
            query += " ORDER BY u.username ASC"
        elif sort_by == 'nama':
            query += " ORDER BY u.nama ASC"
        elif sort_by == 'kamar':
            query += " ORDER BY p.nomor_kamar ASC"
        elif sort_by == 'oldest':
            query += " ORDER BY r.tanggal_request ASC"
        elif sort_by == 'status': # Status pengerjaan
            query += " ORDER BY r.status_request ASC"
        elif sort_by == 'harga_tertinggi':
            query += " ORDER BY l.harga DESC"
        elif sort_by == 'harga_terendah':
            query += " ORDER BY l.harga ASC"
        else:
            # Default: Terbaru
            query += " ORDER BY r.tanggal_request DESC"

        rows = self.db.execute_query(query, tuple(params))
        return self._format_result(rows)

    def _format_result(self, rows) -> List[Dict[str, Any]]:
        history = []
        if not rows: return history

        for row in rows:
            # Format Tanggal DD/MM/YYYY
            tgl_mentah = row['tanggal_request']
            tgl_formatted = "-"
            if tgl_mentah:
                if isinstance(tgl_mentah, str):
                    try:
                        tgl_obj = datetime.strptime(tgl_mentah, "%Y-%m-%d")
                        tgl_formatted = tgl_obj.strftime("%d/%m/%Y")
                    except ValueError: tgl_formatted = tgl_mentah
                elif hasattr(tgl_mentah, 'strftime'):
                     tgl_formatted = tgl_mentah.strftime("%d/%m/%Y")

            status_text = "Selesai" if row['status_request'] else "Sedang dikerjakan"
            items = row['kebutuhan'] if row['kebutuhan'] else "Tidak ada rincian"

            history.append({
                "id": row['request_id'],
                "username": row['username'],
                "nama_penghuni": row['nama_penghuni'],
                "nomor_kamar": row['nomor_kamar'],
                "tanggal": tgl_formatted,
                "layanan": row['nama_layanan'],
                "rincian_barang": items, 
                "status": status_text,
                "total_harga": row['total_harga'],
                "bukti_upload": row['bukti_bayar']
            })
        return history