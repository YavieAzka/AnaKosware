from layanan_service import LayananService
from request_service import RequestService
from db_manager import DatabaseManager


def create_dummy_data(ls: LayananService):
    """
    Pastikan layanan sudah ada sebelum membuat request.
    """
    print("=== DUMMY DATA UC11 ===")

    if ls.get_layanan_by_nama("Laundry") is None:
        ls.create_layanan(
            "Laundry",
            "Cuci pakaian lengkap",
            15000,
            ["Detergen", "Pewangi"]
        )

    if ls.get_layanan_by_nama("Bersih Kamar") is None:
        ls.create_layanan(
            "Bersih Kamar",
            "Pembersihan kamar harian",
            20000,
            ["Sapu", "Pel"]
        )

def test_request(rs: RequestService):
    print("\n=== TEST CREATE REQUEST ===")

    req1 = rs.create_request("Andi", "Laundry")
    print("Request Andi:", req1)

    req2 = rs.create_request("Budi", "Bersih Kamar")
    print("Request Budi:", req2)

    req3 = rs.create_request("Cindy", "TidakAdaLayanan")
    print("Request tidak valid (harus None):", req3)
    tampilkan_request(rs)


def test_uc11_payment(rs: RequestService, request_id: int):
    print("\n=== TEST UC11: Membayar Request Layanan ===")

    # Update status bayar kebutuhan
    bayar_ok = rs.update_status_bayar_kebutuhan(request_id, True)
    print("Status bayar kebutuhan updated?", bayar_ok)

    # Update bukti bayar
    bukti_ok = rs.update_bukti_bayar(request_id, "bukti_transfer.jpg")
    print("Bukti bayar updated?", bukti_ok)


def tampilkan_request(rs: RequestService):
    print("\n=== SEMUA REQUEST ===")
    query = "SELECT * FROM request ORDER BY id"
    data = rs.db.execute_query(query)
    for row in data:
        print(row)

def tampilkan_request_by_nama(rs: RequestService, nama: str):
    print(f"\n=== REQUEST OLEH {nama} ===")
    for r in rs.get_request_by_nama(nama):
        print(r)


def tampilkan_request_by_layanan(rs: RequestService, layanan: str):
    print(f"\n=== REQUEST UNTUK LAYANAN: {layanan} ===")
    for r in rs.get_request_by_layanan(layanan):
        print(r)

if __name__ == "__main__":
    db = DatabaseManager()
    layanan_service = LayananService(db)
    request_service = RequestService(db, layanan_service)
    create_dummy_data(layanan_service)

    test_request(request_service)
    tampilkan_request_by_nama(request_service, "Andi")
    request_id = request_service.get_request_by_nama("Andi")

    tampilkan_request(request_service)

    test_uc11_payment(request_service, request_id[0].id)

    tampilkan_request(request_service)

    print("\n=== SELESAI UC11 ===")