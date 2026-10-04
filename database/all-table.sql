CREATE DATABASE IF NOT EXISTS anakosware_db;
USE anakosware_db;


CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE, -- Untuk Login 
    nama VARCHAR(100) NOT NULL, -- UNTUK DISPLAY
    password VARCHAR(255) NOT NULL, 
    jenisAkun CHAR(1) NOT NULL,
    statusAkun BOOLEAN NOT NULL DEFAULT TRUE,
    
    INDEX(username) 
);


CREATE TABLE IF NOT EXISTS penghuni (
    user_id INT PRIMARY KEY,
    nomor_kamar VARCHAR(10),
    tanggal_masuk DATE,
    harga_kamar INT,
    tanggal_jatuh_tempo DATE,
    
    
    nomor_telepon VARCHAR(20),
    alamat_asal TEXT,
    
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pemilik (
    user_id INT PRIMARY KEY,
    nomor_telepon VARCHAR(20),
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS penjaga (
    user_id INT PRIMARY KEY,
    nomor_telepon VARCHAR(20),
    gaji INT,
    tanggal_masuk_kerja DATE,
    tempat_tanggal_lahir VARCHAR(100),
    alamat TEXT,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS layanan (
    layanan_id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal_layanan DATE,
    nama_layanan VARCHAR(100) NOT NULL,
    deskripsi_layanan TEXT,
    kebutuhan_layanan TEXT
    
);

CREATE TABLE IF NOT EXISTS request (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- ID Penghuni yang me-request
    layanan_id INT NOT NULL,
    tanggal_request DATE NOT NULL,
    status_bayar VARCHAR(50), -- Misal: 'Belum Dibayar', 'Sudah Dibayar'
    status_request VARCHAR(50), -- Misal: 'Pending', 'In Progress', 'Done'
    
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (layanan_id) REFERENCES layanan(layanan_id)
);


CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- ID Penghuni yang memberi feedback
    tanggal_feedback DATE NOT NULL,
    isi TEXT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS pembayaran (
    pembayaran_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- ID Penghuni yang membayar
    
    jenis_pembayaran ENUM('TAGIHAN', 'LAYANAN') NOT NULL,
    
    -- Jika 'LAYANAN', link ke request_id. Jika 'TAGIHAN', ini NULL.
    request_id INT NULL, 
    
    status_pembayaran VARCHAR(50) NOT NULL DEFAULT 'Belum diverifikasi', -- 'Belum diverifikasi', 'Sudah diverifikasi', 'Tidak valid'
    tanggal_bayar DATE NOT NULL,
    nominal_pembayaran DOUBLE NOT NULL,
    
    -- Bukti pembayaran: Menyimpan file path bukti pembayaran
    bukti_pembayaran VARCHAR(255) NOT NULL, -- Simpan path ke file: 'uploads/bukti/payment_123.jpg'
    
    is_bukti_valid BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (request_id) REFERENCES request(request_id),
    
    INDEX(status_pembayaran) -- Index untuk UC06
);