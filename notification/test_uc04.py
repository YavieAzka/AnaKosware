from notification.notification_service import NotificationService
from database.db_manager import DatabaseManager

# Setup Dummy Data (Hanya dijalankan sekali untuk testing)
def setup_dummy_data():
    db = DatabaseManager()
    
    # Pastikan user ada
    db.execute_update("INSERT IGNORE INTO user (user_id, username, nama, password, jenisAkun) VALUES (1, 'penghuni1', 'Budi Santoso', '123', 'P')")
    

    # Menggunakan format tanggal YYYY-MM-DD
    db.execute_update("""
        INSERT IGNORE INTO penghuni (user_id, nomor_kamar, harga_kamar, tanggal_jatuh_tempo) 
        VALUES (1, 'A01', 1500000, '2024-01-20') 
    """) 
    
    print("Dummy data siap.")

if __name__ == "__main__":
    setup_dummy_data() # Hapus baris ini jika data DB sudah ada
    
    service = NotificationService()
    
    # Test User ID 1
    print("\n--- TESTING NOTIFIKASI USER 1 ---")
    notif = service.get_monthly_bill_notification(user_id=1)
    
    if notif:
        print(f"[{notif['type'].upper()}] {notif['message']}")
        print(f"Tagihan: Rp {notif['nominal']:,}")
        if notif.get('is_due'):
            print("Tombol [BAYAR] Aktif")
    else:
        print("Tidak ada notifikasi tagihan saat ini.")