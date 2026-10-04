from verification.verification_service import VerificationService

if __name__ == "__main__":
    print("--- MULAI TEST UC06 (VERIFIKASI PEMILIK) ---")
    
    service = VerificationService()
    
    # 1. PEMILIK MELIHAT DAFTAR PENDING
    print("\n[SYSTEM] Mengambil data pembayaran 'Belum diverifikasi'...")
    pending_list = service.get_pending_payments()
    
    if not pending_list:
        print("[INFO] Tidak ada pembayaran yang perlu diverifikasi.")
        exit()
        
    print(f"[INFO] Ditemukan {len(pending_list)} pembayaran pending:")
    
    # Tampilkan data layaknya di tabel GUI
    current_payment = None
    for idx, p in enumerate(pending_list):
        print(f"   {idx+1}. ID:{p['pembayaran_id']} | Penghuni: {p['nama_penghuni']} | Rp {p['nominal_pembayaran']:,} | Bulan: {p['bulan_tagihan']}")
        current_payment = p # Kita ambil yang terakhir untuk dites
        
    # 2. SIMULASI PEMILIK MEMILIH TINDAKAN
    # Kita ambil ID pembayaran terakhir yang baru saja masuk dari tes UC05 Anda
    target_id = current_payment['pembayaran_id']
    
    print(f"\n[UI] Pemilik memilih pembayaran ID {target_id}...")
    
    # nanti ini disesuain lagi sama UI
    keputusan_terima = True 
    
    print(f"[SYSTEM] Memproses verifikasi (Keputusan: {'TERIMA' if keputusan_terima else 'TOLAK'})...")
    
    if keputusan_terima:
        result = service.process_verification(target_id, is_accepted=True)
    else:
        result = service.process_verification(target_id, is_accepted=False, rejection_reason="Foto buram")
        
    #HASIL
    if result['status'] == 'success':
        print(f"[SUKSES] {result['message']}")
        print(f"[DB CHECK] Status di database kini berubah menjadi: '{result['new_status']}'")
        print("[INFO] Saat Penghuni login nanti, NotificationService (UC04) akan melihat status ini dan berhenti menagih.")
    else:
        print(f"[GAGAL] {result['message']}")