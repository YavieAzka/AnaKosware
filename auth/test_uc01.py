from auth.auth_service import AuthService

if __name__ == "__main__":
    service = AuthService()

    username = input("Masukkan username baru: ")
    nama = input("Masukkan nama penghuni: ")
    password = input("Masukkan password: ")

    result = service.register_penghuni(username, nama, password)
    print(result["status"].upper(), "-", result["message"])
