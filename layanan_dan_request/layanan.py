from dataclasses import dataclass
from typing import List

@dataclass
class Layanan:
    id: int
    nama: str
    deskripsi: str
    harga: float
    kebutuhan: List[str]