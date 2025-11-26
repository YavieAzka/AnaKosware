from dataclasses import dataclass
from typing import List

# Set Tipe Data Layanan
@dataclass
class Layanan:
    id          : int
    nama        : str
    deskripsi   : str
    harga       : float
    kebutuhan   : List[str]