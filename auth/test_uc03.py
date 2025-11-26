from auth.auth_service import AuthService

if __name__ == "__main__":
    service = AuthService()

    username = input("Username penghuni yang akan dinonaktifkan: ")

    result = service.nonaktifkan_akun_penghuni(username)
    print(result["status"].upper(), "-", result["message"])