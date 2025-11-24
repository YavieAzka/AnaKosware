from database.db_manager import DatabaseManager
from datetime import datetime

class FeedbackService:
    def __init__(self):
        # Inisialisasi koneksi database
        self.db = DatabaseManager()

    def submit_feedback(self, user_id, isi_feedback):
        """
        UC13: Memberikan Feedback
        Fungsi ini dipanggil ketika Penghuni mengirimkan feedback/laporan.
        """
        # 1. Validasi Input
        if not isi_feedback or not isi_feedback.strip():
            return {
                "status": "error", 
                "message": "Isi feedback tidak boleh kosong."
            }

        try:
            timestamp = datetime.now()

            # Query Insert,  Kolom: user_id, tanggal_feedback, isi
            query = """
                INSERT INTO feedback (user_id, tanggal_feedback, isi)
                VALUES (%s, %s, %s)
            """

            params = (user_id, timestamp, isi_feedback)

            # Eksekusi ke Database
            result = self.db.execute_update(query, params)

            if result:
                return {
                    "status": "success", 
                    "message": "Feedback berhasil dikirim. Terima kasih atas masukan Anda.",
                    "created_at": timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                return {"status": "error", "message": "Gagal menyimpan feedback ke database."}

        except Exception as e:
            return {"status": "error", "message": f"Terjadi kesalahan sistem: {str(e)}"}

    def get_all_feedbacks(self):
        """
        UC14: Melihat Feedback (Untuk Pemilik Kos)
        Mengambil semua data feedback digabung dengan data user (nama penghuni).
        """
        try:
            # PERBAIKAN: Saya menghapus 'u.nomor_kamar' dari query di bawah ini
            # karena kolom tersebut tidak ada di tabel user Anda.
            query = """
                SELECT 
                    f.feedback_id, 
                    f.tanggal_feedback, 
                    f.isi, 
                    u.nama AS nama_penghuni
                FROM feedback f
                JOIN user u ON f.user_id = u.user_id
                ORDER BY f.tanggal_feedback DESC
            """
            
            feedbacks = self.db.execute_query(query)
            
            if feedbacks:
                formatted_data = []
                for item in feedbacks:
                    # Formatting data tanggal agar aman (handle date object atau string)
                    tgl = item['tanggal_feedback']
                    str_tgl = str(tgl) # Fallback default
                    
                    if hasattr(tgl, 'strftime'):
                        str_tgl = tgl.strftime("%d-%m-%Y")
                    elif isinstance(tgl, str):
                        # Coba parsing jika string formatnya YYYY-MM-DD
                        try:
                            # Sesuaikan format ini dengan output database Anda jika perlu
                            tgl_obj = datetime.strptime(str(tgl), "%Y-%m-%d") 
                            str_tgl = tgl_obj.strftime("%d-%m-%Y")
                        except:
                            pass # Gunakan string aslinya jika parsing gagal

                    formatted_data.append({
                        "id": item['feedback_id'],
                        "penghuni": item['nama_penghuni'],
                        "tanggal": str_tgl,
                        "isi": item['isi']
                    })
                
                return {
                    "status": "success",
                    "data": formatted_data
                }
            else:
                return {
                    "status": "success", 
                    "data": [], 
                    "message": "Belum ada feedback masuk."
                }

        except Exception as e:
            # Print error ke terminal agar mudah debugging
            print(f"DEBUG ERROR FEEDBACK: {str(e)}")
            return {"status": "error", "message": f"Gagal memuat data: {str(e)}"}

    def get_my_feedback_history(self, user_id):
        """
        (Fitur Tambahan) Melihat Riwayat Feedback Sendiri
        Untuk ditampilkan di sisi Penghuni agar tahu feedback apa saja yang pernah dikirim.
        """
        try:
            query = """
                SELECT feedback_id, tanggal_feedback, isi 
                FROM feedback 
                WHERE user_id = %s 
                ORDER BY tanggal_feedback DESC
            """
            feedbacks = self.db.execute_query(query, (user_id,))
            
            return {"status": "success", "data": feedbacks if feedbacks else []}
        
        except Exception as e:
            return {"status": "error", "message": f"Error: {str(e)}"}