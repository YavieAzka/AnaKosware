# db_manager.py
import json

class DatabaseManager:

    def __init__(self):
        # tabel dalam memori
        self.layanan = []      # list of dict
        self.request = []      # list of dict

        # auto-increment
        self.layanan_id = 1
        self.request_id = 1

    # ===============================
    # SELECT QUERY HANDLER
    # ===============================
    def execute_query(self, query, params=None):
        q = query.strip().upper()

        # === SELECT MAX(id) FROM layanan ===
        if "SELECT COALESCE(MAX(ID)" in q and "FROM LAYANAN" in q:
            if len(self.layanan) == 0:
                return [(1,)]
            else:
                max_id = max(item["id"] for item in self.layanan) + 1
                return [(max_id,)]

        # === SELECT * FROM layanan WHERE id = %s ===
        if "FROM LAYANAN WHERE ID =" in q:
            id_val = params[0]
            result = [
                tuple(self._layanan_to_row(x))
                for x in self.layanan
                if x["id"] == id_val
            ]
            return result

        # === SELECT * FROM layanan WHERE LOWER(nama) ===
        if "FROM LAYANAN WHERE LOWER(NAMA)" in q:
            nama = params[0].lower()
            result = [
                tuple(self._layanan_to_row(x))
                for x in self.layanan
                if x["nama"].lower() == nama
            ]
            return result

        # === SELECT * FROM layanan ORDER BY id ===
        if "FROM LAYANAN ORDER BY ID" in q:
            return [
                tuple(self._layanan_to_row(x))
                for x in sorted(self.layanan, key=lambda d: d["id"])
            ]

        # === SELECT * FROM request WHERE id ===
        if "FROM REQUEST WHERE ID =" in q:
            id_val = params[0]
            return [
                tuple(self._request_to_row(x))
                for x in self.request
                if x["id"] == id_val
            ]

        # === SELECT * FROM request WHERE LOWER(nama) ===
        if "FROM REQUEST" in q and "LOWER(NAMA)" in q:
            nama = params[0].lower()
            return [
                tuple(self._request_to_row(x))
                for x in self.request
                if x["nama"].lower() == nama
            ]

        # === SELECT * FROM request WHERE LOWER(nama_layanan) ===
        if "FROM REQUEST" in q and "LOWER(NAMA_LAYANAN)" in q:
            nama = params[0].lower()
            return [
                tuple(self._request_to_row(x))
                for x in self.request
                if x["nama_layanan"].lower() == nama
            ]

        # RETURNING id (insert request)
        if "RETURNING ID" in q.replace(";", "").replace("\n", " "):
            new_id = self.request_id
            self.request_id += 1

            self.request.append({
                "id": new_id,
                "nama": params[0],
                "nama_layanan": params[1],
                "status_bayar_kebutuhan": False,
                "status_request": False,
                "bukti_bayar": None
            })

            return [(new_id,)]
        
        # === SELECT * FROM request ORDER BY id ===
        if "FROM REQUEST" in q and "ORDER BY ID" in q:
            return [
                tuple(self._request_to_row(x))
                for x in sorted(self.request, key=lambda d: d["id"])
            ]

        return []

    # ===============================
    # UPDATE / INSERT / DELETE
    # ===============================
    def execute_update(self, query, params=None):
        q = query.strip().upper()

        # INSERT layanan
        if "INSERT INTO LAYANAN" in q:
            (id_val, nama, deskripsi, harga, kebutuhan) = params
            self.layanan.append({
                "id": id_val,
                "nama": nama,
                "deskripsi": deskripsi,
                "harga": harga,
                "kebutuhan": json.loads(kebutuhan) if isinstance(kebutuhan, str) else kebutuhan
            })
            return True

        # UPDATE layanan
        if "UPDATE LAYANAN" in q:
            (nama, deskripsi, harga, kebutuhan, id_val) = params
            for item in self.layanan:
                if item["id"] == id_val:
                    item["nama"] = nama
                    item["deskripsi"] = deskripsi
                    item["harga"] = harga
                    item["kebutuhan"] = json.loads(kebutuhan) if isinstance(kebutuhan, str) else kebutuhan
                    return True
            return False

        # DELETE layanan
        if "DELETE FROM LAYANAN" in q:
            id_val = params[0]
            before = len(self.layanan)
            self.layanan = [x for x in self.layanan if x["id"] != id_val]
            return len(self.layanan) < before

        # UPDATE request: bayar
        if "STATUS_BAYAR_KEBUTUHAN" in q:
            (status, id_val) = params
            for r in self.request:
                if r["id"] == id_val:
                    r["status_bayar_kebutuhan"] = status
                    return True
            return False

        # UPDATE request: status
        if "STATUS_REQUEST" in q:
            (status, id_val) = params
            for r in self.request:
                if r["id"] == id_val:
                    r["status_request"] = status
                    return True
            return False

        # UPDATE request: bukti bayar
        if "BUKTI_BAYAR" in q:
            (path, id_val) = params
            for r in self.request:
                if r["id"] == id_val:
                    r["bukti_bayar"] = path
                    return True
            return False

        # DELETE request
        if "DELETE FROM REQUEST" in q:
            id_val = params[0]
            before = len(self.request)
            self.request = [x for x in self.request if x["id"] != id_val]
            return len(self.request) < before

        return True

    # ===============================
    # Helper Row Conversion
    # ===============================
    def _layanan_to_row(self, x):
        return [
            x["id"],
            x["nama"],
            x["deskripsi"],
            x["harga"],
            json.dumps(x["kebutuhan"])
        ]

    def _request_to_row(self, x):
        return [
            x["id"],
            x["nama"],
            x["nama_layanan"],
            x["status_bayar_kebutuhan"],
            x["status_request"],
            x["bukti_bayar"]
        ]
