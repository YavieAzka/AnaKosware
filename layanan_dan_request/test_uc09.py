from db_manager import DatabaseManager
from layanan_service import LayananService


def create_dummy_data(service: LayananService):
    """
    Mengisi database dengan layanan awal untuk keperluan testing.
    Hanya dijalankan sekali saja.
    """
    print("DEBUG:", service.db.execute_query("SELECT name FROM sqlite_master WHERE type='table';"))
    print("=== MENGISI DUMMY DATA UC09 ===")

    # Tambah layanan pertama
    layanan1 = service.create_layanan(
        nama="Laundry",
        deskripsi="Cuci pakaian lengkap",
        harga=15000,
        kebutuhan=["Detergen", "Pewangi"]
    )
    print("Tambah layanan 1:", layanan1)
    print("\n")

    # Tambah layanan kedua
    layanan2 = service.create_layanan(
        nama="Bersih Kamar",
        deskripsi="Pembersihan kamar harian",
        harga=20000,
        kebutuhan=["Sapu", "Pel", "Pembersih lantai"]
    )
    print("Tambah layanan 2:", layanan2)
    print("\n")

def test_update(service: LayananService):
    print("\n=== TEST UPDATE LAYANAN ===")

    layanan = service.get_layanan_by_nama("Laundry")
    if layanan:
        print("Sebelum update:", layanan)

        service.update_layanan(
            id=layanan.id,
            harga=18000,
            kebutuhan=["Detergen", "Pewangi", "Softener"]
        )

        layanan_baru = service.get_layanan_by_id(layanan.id)
        print("Setelah update:", layanan_baru)


def test_duplicate_name(service: LayananService):
    print("\n=== TEST DUPLICATE NAME ===")

    result = service.create_layanan(
        nama="Laundry",  # duplikat
        deskripsi="Test",
        harga=10000,
        kebutuhan=[]
    )
    print("Hasil membuat layanan duplikat:", result)


def tampilkan_semua(service: LayananService):
    print("\n=== SEMUA LAYANAN ===")
    for l in service.get_all_layanan():
        print(l)


if __name__ == "__main__":
    db = DatabaseManager()
    service = LayananService(db)

    create_dummy_data(service)
    test_update(service)
    test_duplicate_name(service)
    tampilkan_semua(service)
    print("\n=== SELESAI UC09 ===")