CREATE TABLE IF NOT EXISTS kategori (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    ust_kategori_no INTEGER,
    FOREIGN KEY (ust_kategori_no) REFERENCES kategori(no) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tedarikci (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    telefon TEXT,
    eposta TEXT UNIQUE,
    adres TEXT
);

CREATE TABLE IF NOT EXISTS parca (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    parca_kodu TEXT NOT NULL UNIQUE,
    kategori_no INTEGER NOT NULL,
    tedarikci_no INTEGER NOT NULL,
    fiyat REAL NOT NULL DEFAULT 0.0,
    stok_miktari INTEGER NOT NULL DEFAULT 0,
    aciklama TEXT,
    kayit_tarihi TEXT NOT NULL DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (kategori_no) REFERENCES kategori(no) ON DELETE RESTRICT,
    FOREIGN KEY (tedarikci_no) REFERENCES tedarikci(no) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS stok_hareketi (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    parca_no INTEGER NOT NULL,
    miktar INTEGER NOT NULL,
    hareket_tipi TEXT NOT NULL CHECK(hareket_tipi IN ('giris', 'cikis')),
    tarih TEXT NOT NULL DEFAULT (datetime('now','localtime')),
    aciklama TEXT,
    FOREIGN KEY (parca_no) REFERENCES parca(no) ON DELETE CASCADE
);

INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Motor Parçaları', NULL);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Elektrik & Elektronik', NULL);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Hidrolik Sistem', NULL);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Rulman & Mil', NULL);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Bağlantı Elemanları', NULL);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Pistonlar', 1);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Valfler', 1);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Sensörler', 2);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Kablolama', 2);
INSERT INTO kategori (ad, ust_kategori_no) VALUES ('Pompalar', 3);

INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES ('Bosch Türkiye', '0212-555-0001', 'info@bosch.com.tr', 'İstanbul, Türkiye');
INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES ('SKF Rulman', '0216-555-0002', 'satis@skf.com.tr', 'Kocaeli, Türkiye');
INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES ('Siemens Endüstri', '0312-555-0003', 'siparis@siemens.com.tr', 'Ankara, Türkiye');
INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES ('Parker Hannifin', '0232-555-0004', 'info@parker.com.tr', 'İzmir, Türkiye');
INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES ('Festo Türkiye', '0216-555-0005', 'bilgi@festo.com.tr', 'İstanbul, Türkiye');
INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES ('Schneider Electric', '0212-555-0006', 'destek@schneider.com.tr', 'İstanbul, Türkiye');

INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Endüstriyel Piston V12', 'MTR-PST-001', 6, 1, 2450.00, 35, '12 cm çaplı endüstriyel piston, yüksek basınca dayanıklı');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Bilyalı Rulman 6205', 'RUL-BIL-001', 4, 2, 185.50, 150, 'SKF 6205-2RS bilyalı rulman, 25x52x15 mm');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Proximity Sensör M18', 'ELK-SNS-001', 8, 3, 320.00, 75, 'Endüktif proximity sensör, 8mm algılama mesafesi');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Hidrolik Pompa 20L', 'HDR-PMP-001', 10, 4, 8750.00, 12, '20 litre/dakika kapasiteli dişli pompa');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Pnömatik Valf 5/2', 'MTR-VLF-001', 7, 5, 540.00, 45, '5/2 yönlü pnömatik selenoid valf');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('M10 Cıvata Seti', 'BAG-CIV-001', 5, 1, 12.50, 500, 'Paslanmaz çelik M10x40 cıvata, 50li paket');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Kontaktör 3P 40A', 'ELK-KNT-001', 2, 6, 475.00, 28, '3 kutuplu 40 Amper AC kontaktör');
INSERT INTO parca (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama) VALUES ('Kayış Kasnağı D200', 'MTR-KSK-001', 1, 2, 680.00, 18, '200mm çaplı döküm kasnak, B tipi kayış uyumlu');

INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (1, 50, 'giris', '2026-01-15 09:30:00', 'İlk stok girişi — Bosch siparişi');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (1, 15, 'cikis', '2026-02-20 14:00:00', 'Üretim hattına sevk');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (2, 200, 'giris', '2026-01-10 10:00:00', 'SKF toplu alım');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (2, 50, 'cikis', '2026-03-05 11:30:00', 'Bakım departmanı talebi');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (3, 100, 'giris', '2026-02-01 08:45:00', 'Siemens siparişi teslim alındı');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (3, 25, 'cikis', '2026-03-18 16:15:00', 'Hat-3 sensör değişimi');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (4, 15, 'giris', '2026-01-20 13:00:00', 'Parker Hannifin teslimat');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (4, 3, 'cikis', '2026-04-01 09:00:00', 'Hidrolik sistem revizyonu');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (5, 60, 'giris', '2026-02-10 10:30:00', 'Festo kampanya alımı');
INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, tarih, aciklama) VALUES (5, 15, 'cikis', '2026-03-25 15:45:00', 'Pnömatik hat bakımı');
