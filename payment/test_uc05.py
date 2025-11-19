import os
from payment.payment_service import PaymentService

def create_dummy_image():
    """Membuat file dummy untuk simulasi upload"""
    filename = "test_struk_atm.txt" # Kita pakai txt dulu, nanti direname jadi .jpg oleh sistem
    with open(filename, "w") as f:
        f.write("Ini adalah pura-pura gambar struk ATM")
    return os.path.abspath(filename)

if __name__ == "__main__":
    print("--- MULAI TEST UC05 (PEMBAYARAN) ---")
    
    service = PaymentService()
    
    # 1. Persiapan Data
    user_id = 1
    nominal_bayar = 1500000
    
    # 2. Buat file dummy (Simulasi user memilih file dari komputer mereka)
    dummy_file_path = create_dummy_image()
    print(f"[UI] User memilih file dari: {dummy_file_path}")
    
    # 3. Eksekusi Pembayaran
    print("[SYSTEM] Memproses pembayaran...")
    result = service.process_monthly_payment(user_id, nominal_bayar, dummy_file_path)
    
    # 4. Tampilkan Hasil
    if result['status'] == 'success':
        print(f"\n[SUKSES] {result['message']}")
        print(f"[DEBUG] File tersimpan di: {result['file_saved_at']}")
        print("[INFO] Silakan cek folder 'uploads/bukti_bayar' di proyek Anda.")
        print("[INFO] Silakan cek tabel 'pembayaran' di database Anda.")
    else:
        print(f"\n[GAGAL] {result['message']}")

    # Cleanup: Hapus file dummy asal
    if os.path.exists(dummy_file_path):
        os.remove(dummy_file_path)