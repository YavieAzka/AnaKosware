from auth.auth_service import AuthService

if __name__ == "__main__":
    service = AuthService()

    jenisAkun = input("Role (misal: PENGHUNI / PEMILIK / PENJAGA): ")
    username = input("Username: ")
    password = input("Password: ")

    result = service.login(jenisAkun, username, password)
    print(result["status"].upper(), "-", result["message"])

    if result["status"] == "success":
        print("Data user:", result["user"])
