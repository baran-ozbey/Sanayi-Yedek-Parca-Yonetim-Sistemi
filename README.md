# Sanayi Yedek Parça Yönetim Sistemi

## Proje Açıklaması
Flask + SQLite + HTML/CSS/JS ile geliştirilmiş, sanayi yedek parçalarının stok, kategori ve tedarikçi yönetimini sağlayan tam işlevsel bir web uygulamasıdır.

**Ders:** YZM102 / MYAZ104 — Programlamaya Giriş II  
**Konu:** Sanayi Yedek Parça Yönetim Sistemi  

---

## Kurulum ve Çalıştırma

### 1. Gereksinimler
- Python 3.10+
- pip

### 2. Sanal Ortam Oluşturma
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Çalıştırma
```bash
python app.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışır.  
İlk çalıştırmada veritabanı otomatik olarak oluşturulur ve örnek verilerle doldurulur.

---

## Veritabanı Tabloları

| Tablo | Açıklama | İlişki |
|-------|----------|--------|
| `kategori` | Parça kategorileri (özyinelemeli) | Kendi kendine FK (üst kategori) |
| `tedarikci` | Tedarikçi firmalar | — |
| `parca` | Yedek parçalar | FK → kategori, tedarikci |
| `stok_hareketi` | Stok giriş/çıkış kayıtları | FK → parca |

---

## Kullanılan Python Konuları

| # | Konu | Kullanım Yeri |
|---|------|--------------|
| 1 | Değişkenler & Veri Tipleri | Model sınıfları, veritabanı dönüşümleri |
| 2 | print() & input() | Debug/log çıktıları |
| 3 | Koşul İfadeleri & Döngüler | Filtreleme, form doğrulama, stok kontrolü |
| 4 | String Modülü | Arama (lower/upper), parça kodu formatlama |
| 5 | Fonksiyonlar | CRUD fonksiyonları, yardımcı araçlar |
| 6 | Listeler | Veritabanı sorgu sonuçları |
| 7 | Demetler (Tuple) | SQL parametre geçişi |
| 8 | Modüller | flask, sqlite3, os, json, csv, datetime, io |
| 9 | Dosya İşlemleri | CSV dışa aktarma, log dosyası yazma |
| 10 | Sözlükler | JSON yanıt yapıları, dashboard özet |
| 11 | Özyinelemeli Fonksiyonlar | Kategori ağacı (hiyerarşik listeleme) |
| 12 | İstisna Yönetimi | try/except/finally, HTTP 404/500 |
| 13 | Nesne Yönelimli Programlama | Model sınıfları: Kategori, Parca, Tedarikci, StokHareketi |
| 14 | Numpy / Pandas / Matplotlib | İstatistik sayfası, grafikler, veri analizi |

---

## Proje Yapısı

```
sanayi_yedek_parca/
├── app.py                  # Ana Flask uygulaması
├── database.py             # Veritabanı bağlantı ve CRUD fonksiyonları
├── models.py               # OOP model sınıfları
├── schema.sql              # Veritabanı şeması ve örnek veriler
├── data.db                 # SQLite veritabanı (otomatik oluşur)
├── requirements.txt        # Python bağımlılıkları
├── static/
│   ├── css/style.css       # Ana stil dosyası (koyu tema)
│   └── js/main.js          # JavaScript (modal, sidebar)
├── templates/
│   ├── base.html           # Temel şablon (layout)
│   ├── index.html          # Dashboard
│   ├── parcalar.html       # Parça yönetimi
│   ├── kategoriler.html    # Kategori yönetimi
│   ├── tedarikciler.html   # Tedarikçi yönetimi
│   ├── stok.html           # Stok hareketleri
│   ├── istatistik.html     # İstatistik & grafikler
│   └── hata.html           # Hata sayfası
└── README.md               # Bu dosya
```

---

## Kullanılan Teknolojiler ve Kaynaklar

| Teknoloji | Sürüm | Kaynak |
|-----------|-------|--------|
| Python | 3.10+ | python.org |
| Flask | 3.x | flask.palletsprojects.com |
| SQLite3 | Built-in | docs.python.org |
| Numpy | 1.26+ | numpy.org |
| Pandas | 2.1+ | pandas.pydata.org |
| Matplotlib | 3.8+ | matplotlib.org |
| Font Awesome | 6.5 | fontawesome.com |
| Google Fonts (Inter) | — | fonts.google.com |

