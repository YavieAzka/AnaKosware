from dataclasses import dataclass

@dataclass
class Request:
    id: int
    nama: str                  # Nama Pemesan
    namaLayanan: str           # Nama layanan (string)
    statusBayarKebutuhan: bool
    statusRequest: bool
    buktiBayar: str            # Path Bukti Bayar (sementara str, nanti pakai class Pembayaran)