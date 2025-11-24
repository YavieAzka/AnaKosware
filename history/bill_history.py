from typing import List, Dict, Any, Optional
from database.db_manager import DatabaseManager
from datetime import datetime

class BillHistory:
    def __init__(self):
        self.db = DatabaseManager()

    def get_riwayat_tagihan(self, 
                            user_id: Optional[int] = None, 
                            sort_by: str = 'newest', 
                            filter_status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Mengambil data riwayat tagihan bulanan.
        Aktor: Pemilik (user_id=None) & Penghuni (user_id=int)
        """

        # Query Dasar
        query = """
            SELECT 
                p.pembayaran_id,
                p.bulan_tagihan,
                p.tahun_tagihan,
                p.tanggal_bayar,
                p.nominal_pembayaran,
                p.status_pembayaran,
                p.is_bukti_valid,
                u.username,
                u.nama AS nama_penghuni,
                pg.nomor_kamar
            FROM pembayaran p
            JOIN user u ON p.user_id = u.user_id
            LEFT JOIN penghuni pg ON u.user_id = pg.user_id
            WHERE p.jenis_pembayaran = 'TAGIHAN'
        """
        
        params = []

        # 1. Filter User (POV Penghuni vs Pemilik)
        if user_id is not None:
            query += " AND p.user_id = %s"
            params.append(user_id)

        # 2. Filter Status
        if filter_status:
            if filter_status.lower() == 'diterima':
                query += " AND p.status_pembayaran = 'Sudah diverifikasi' AND p.is_bukti_valid = 1"
            elif filter_status.lower() == 'menunggu':
                query += " AND p.status_pembayaran = 'Belum diverifikasi'"
            elif filter_status.lower() == 'ditolak':
                query += " AND p.status_pembayaran = 'Sudah diverifikasi' AND p.is_bukti_valid = 0"

        # 3. Sorting / Filter Urutan
        if sort_by == 'username':
            query += " ORDER BY u.username ASC"
        elif sort_by == 'bulan_asc':
            query += " ORDER BY p.tahun_tagihan ASC, p.bulan_tagihan ASC"
        elif sort_by == 'bulan_desc':
            query += " ORDER BY p.tahun_tagihan DESC, p.bulan_tagihan DESC"
        elif sort_by == 'nominal_high':
            query += " ORDER BY p.nominal_pembayaran DESC"
        elif sort_by == 'nominal_low':
            query += " ORDER BY p.nominal_pembayaran ASC"
        elif sort_by == 'oldest': 
            query += " ORDER BY p.tanggal_bayar ASC"
        elif sort_by == 'status':
            query += " ORDER BY p.status_pembayaran ASC"
        else:
            # Default: Terbaru
            query += " ORDER BY p.tanggal_bayar DESC"

        rows = self.db.execute_query(query, tuple(params))
        return self._format_result(rows)

    def _format_result(self, rows) -> List[Dict[str, Any]]:
        history = []
        if not rows: return history

        for row in rows:
            # Format Tanggal DD/MM/YYYY
            tgl_raw = row['tanggal_bayar']
            tgl_fix = "-"
            if tgl_raw:
                if isinstance(tgl_raw, str):
                    try:
                        tgl_obj = datetime.strptime(tgl_raw, "%Y-%m-%d")
                        tgl_fix = tgl_obj.strftime("%d/%m/%Y")
                    except: tgl_fix = tgl_raw
                else:
                    tgl_fix = tgl_raw.strftime("%d/%m/%Y")

            # Logic Status Teks
            status_db = row['status_pembayaran']
            valid = row['is_bukti_valid']
            
            display_status = status_db
            if status_db == 'Sudah diverifikasi':
                display_status = "Diterima" if valid else "Ditolak"
            elif status_db == 'Belum diverifikasi':
                display_status = "Menunggu Konfirmasi"

            history.append({
                "id": row['pembayaran_id'],
                "username": row['username'],
                "nama_penghuni": row['nama_penghuni'],
                "kamar": row['nomor_kamar'],
                "periode": f"{row['bulan_tagihan']}/{row['tahun_tagihan']}",
                "tanggal": tgl_fix,
                "nominal": row['nominal_pembayaran'],
                "status": display_status
            })
            
        return history