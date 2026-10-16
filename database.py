import sqlite3
import os

VT_YOLU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")


def veritabanina_baglan():
    """
    SQLite veritabanına bağlanır ve bağlantı nesnesini döndürür.
    row_factory sayesinde sütun adıyla erişebiliyoruz (satir["ad"] gibi).
    """
    baglanti = sqlite3.connect(VT_YOLU)
    baglanti.row_factory = sqlite3.Row
    baglanti.execute("PRAGMA foreign_keys = ON")
    return baglanti


def veritabanini_baslat():
    """
    schema.sql dosyasını okur ve tabloları oluşturur.
    Uygulama ilk açıldığında çağrılıyor.
    """
    sema_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    try:
        baglanti = veritabanina_baglan()
        with open(sema_yolu, "r", encoding="utf-8") as f:
            sql = f.read()
        baglanti.executescript(sql)
        baglanti.commit()
        print("Veritabanı başarıyla oluşturuldu.")
    except Exception as hata:
        print(f"Veritabanı başlatma hatası: {hata}")
    finally:
        baglanti.close()


def kategori_listele():
    """
    Veritabanındaki tüm kategorileri çekip liste olarak döndürür.
    fetchall() bize liste döndürüyor.
    """
    baglanti = veritabanina_baglan()
    try:
        sonuc = baglanti.execute("SELECT * FROM kategori ORDER BY ad").fetchall()
        return sonuc
    except Exception as hata:
        print(f"Kategori listeleme hatası: {hata}")
        return []
    finally:
        baglanti.close()


def kategori_getir(kategori_no):
    """
    Verilen no'ya ait kategoriyi döndürür.
    SQL parametresi tuple olarak geçiriliyor (SQL injection önlemi).
    """
    baglanti = veritabanina_baglan()
    try:
        sonuc = baglanti.execute(
            "SELECT * FROM kategori WHERE no = ?", (kategori_no,)
        ).fetchone()
        return sonuc
    except Exception as hata:
        print(f"Kategori getirme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def kategori_ekle(ad, ust_kategori_no=None):
    """
    Yeni kategori ekler ve eklenen kaydın no'sunu döndürür.
    Üst kategori yoksa NULL bırakılıyor.
    """
    baglanti = veritabanina_baglan()
    try:
        imlec = baglanti.execute(
            "INSERT INTO kategori (ad, ust_kategori_no) VALUES (?, ?)",
            (ad, ust_kategori_no)
        )
        baglanti.commit()
        return imlec.lastrowid
    except Exception as hata:
        print(f"Kategori ekleme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def kategori_guncelle(kategori_no, ad, ust_kategori_no=None):
    """Mevcut kategoriyi günceller, başarılı olursa True döner."""
    baglanti = veritabanina_baglan()
    try:
        baglanti.execute(
            "UPDATE kategori SET ad = ?, ust_kategori_no = ? WHERE no = ?",
            (ad, ust_kategori_no, kategori_no)
        )
        baglanti.commit()
        return True
    except Exception as hata:
        print(f"Kategori güncelleme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def kategori_sil(kategori_no):
    """Kategoriyi siler. Bu kategoriye bağlı parça varsa FK hatası verir."""
    baglanti = veritabanina_baglan()
    try:
        baglanti.execute("DELETE FROM kategori WHERE no = ?", (kategori_no,))
        baglanti.commit()
        return True
    except Exception as hata:
        print(f"Kategori silme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def kategori_agaci(ust_no=None, seviye=0):
    """
    Özyinelemeli (recursive) fonksiyon - kategori ağacını oluşturur.
    Kendini tekrar çağırarak alt kategorileri buluyor.
    Sınırsız derinlikte kategori yapısını destekler.
    """
    baglanti = veritabanina_baglan()
    try:
        if ust_no is None:
            kategoriler = baglanti.execute(
                "SELECT * FROM kategori WHERE ust_kategori_no IS NULL ORDER BY ad"
            ).fetchall()
        else:
            kategoriler = baglanti.execute(
                "SELECT * FROM kategori WHERE ust_kategori_no = ? ORDER BY ad",
                (ust_no,)
            ).fetchall()

        agac = []
        for kat in kategoriler:
            dugum = {
                "no": kat["no"],
                "ad": kat["ad"],
                "seviye": seviye,
                "alt_kategoriler": []
            }
            baglanti.close()
            dugum["alt_kategoriler"] = kategori_agaci(kat["no"], seviye + 1)
            baglanti = veritabanina_baglan()
            agac.append(dugum)

        return agac
    except Exception as hata:
        print(f"Kategori ağacı hatası: {hata}")
        return []
    finally:
        baglanti.close()


def kategori_agaci_duz(ust_no=None, seviye=0):
    """
    Kategori ağacını düz liste olarak döndürür.
    Dropdown menülerde kullanmak için tasarlandı.
    Bu da recursive çalışıyor, her seviyeye girinti ekliyor.
    """
    baglanti = veritabanina_baglan()
    try:
        if ust_no is None:
            kategoriler = baglanti.execute(
                "SELECT * FROM kategori WHERE ust_kategori_no IS NULL ORDER BY ad"
            ).fetchall()
        else:
            kategoriler = baglanti.execute(
                "SELECT * FROM kategori WHERE ust_kategori_no = ? ORDER BY ad",
                (ust_no,)
            ).fetchall()

        sonuc = []
        for kat in kategoriler:
            girinti = "—" * seviye
            sonuc.append({
                "no": kat["no"],
                "ad": f"{girinti} {kat['ad']}" if seviye > 0 else kat["ad"],
                "ad_sade": kat["ad"],
                "seviye": seviye
            })
            baglanti.close()
            sonuc.extend(kategori_agaci_duz(kat["no"], seviye + 1))
            baglanti = veritabanina_baglan()

        return sonuc
    except Exception as hata:
        print(f"Düz kategori ağacı hatası: {hata}")
        return []
    finally:
        baglanti.close()


def tedarikci_listele():
    """Tüm tedarikçileri A-Z sıralı getirir."""
    baglanti = veritabanina_baglan()
    try:
        sonuc = baglanti.execute("SELECT * FROM tedarikci ORDER BY ad").fetchall()
        return sonuc
    except Exception as hata:
        print(f"Tedarikçi listeleme hatası: {hata}")
        return []
    finally:
        baglanti.close()


def tedarikci_getir(tedarikci_no):
    """No'ya göre tek tedarikçi getirir."""
    baglanti = veritabanina_baglan()
    try:
        sonuc = baglanti.execute(
            "SELECT * FROM tedarikci WHERE no = ?", (tedarikci_no,)
        ).fetchone()
        return sonuc
    except Exception as hata:
        print(f"Tedarikçi getirme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def tedarikci_ekle(ad, telefon, eposta, adres):
    """
    Yeni tedarikçi ekler.
    E-posta alanı UNIQUE olduğu için aynı mail tekrar girilirse hata verir.
    """
    baglanti = veritabanina_baglan()
    try:
        imlec = baglanti.execute(
            "INSERT INTO tedarikci (ad, telefon, eposta, adres) VALUES (?, ?, ?, ?)",
            (ad, telefon, eposta, adres)
        )
        baglanti.commit()
        return imlec.lastrowid
    except sqlite3.IntegrityError:
        print(f"Bu e-posta zaten kayıtlı: {eposta}")
        return None
    except Exception as hata:
        print(f"Tedarikçi ekleme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def tedarikci_guncelle(tedarikci_no, ad, telefon, eposta, adres):
    """Tedarikçi bilgilerini günceller."""
    baglanti = veritabanina_baglan()
    try:
        baglanti.execute(
            "UPDATE tedarikci SET ad=?, telefon=?, eposta=?, adres=? WHERE no=?",
            (ad, telefon, eposta, adres, tedarikci_no)
        )
        baglanti.commit()
        return True
    except sqlite3.IntegrityError:
        print("E-posta zaten kullanımda.")
        return False
    except Exception as hata:
        print(f"Tedarikçi güncelleme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def tedarikci_sil(tedarikci_no):
    """
    Tedarikçiyi siler.
    Bu tedarikçiye bağlı parça varsa silme işlemi başarısız olur (FK kuralı).
    """
    baglanti = veritabanina_baglan()
    try:
        baglanti.execute("DELETE FROM tedarikci WHERE no = ?", (tedarikci_no,))
        baglanti.commit()
        return True
    except Exception as hata:
        print(f"Tedarikçi silme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def parca_listele(arama=None, kategori_no=None):
    """
    Parçaları listeler. Arama metni ve kategori filtresi destekliyor.
    Filtreler dinamik olarak WHERE koşuluna ekleniyor.
    LOWER() ile büyük/küçük harf duyarsız arama yapıyoruz.
    """
    baglanti = veritabanina_baglan()
    try:
        sorgu = """
            SELECT p.*, k.ad AS kategori_adi, t.ad AS tedarikci_adi
            FROM parca p
            LEFT JOIN kategori k ON p.kategori_no = k.no
            LEFT JOIN tedarikci t ON p.tedarikci_no = t.no
        """
        kosullar = []
        parametreler = []

        if arama:
            kosullar.append("(LOWER(p.ad) LIKE ? OR LOWER(p.parca_kodu) LIKE ?)")
            arama_lower = f"%{arama.lower()}%"
            parametreler.extend([arama_lower, arama_lower])

        if kategori_no:
            kosullar.append("p.kategori_no = ?")
            parametreler.append(kategori_no)

        if kosullar:
            sorgu += " WHERE " + " AND ".join(kosullar)

        sorgu += " ORDER BY p.ad"

        parcalar = baglanti.execute(sorgu, tuple(parametreler)).fetchall()
        return parcalar
    except Exception as hata:
        print(f"Parça listeleme hatası: {hata}")
        return []
    finally:
        baglanti.close()


def parca_getir(parca_no):
    """
    No'ya göre tek parça getirir.
    JOIN ile kategori ve tedarikçi adlarını da çekiyoruz.
    """
    baglanti = veritabanina_baglan()
    try:
        sonuc = baglanti.execute("""
            SELECT p.*, k.ad AS kategori_adi, t.ad AS tedarikci_adi
            FROM parca p
            LEFT JOIN kategori k ON p.kategori_no = k.no
            LEFT JOIN tedarikci t ON p.tedarikci_no = t.no
            WHERE p.no = ?
        """, (parca_no,)).fetchone()
        return sonuc
    except Exception as hata:
        print(f"Parça getirme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def parca_ekle(ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama):
    """
    Yeni parça ekler.
    Parça kodu UNIQUE olduğu için aynı kod tekrar girilemez.
    """
    baglanti = veritabanina_baglan()
    try:
        imlec = baglanti.execute(
            """INSERT INTO parca
               (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama)
        )
        baglanti.commit()
        return imlec.lastrowid
    except sqlite3.IntegrityError:
        print(f"Parça kodu zaten mevcut: {parca_kodu}")
        return None
    except Exception as hata:
        print(f"Parça ekleme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def parca_guncelle(parca_no, ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama):
    """Mevcut parçanın bilgilerini günceller."""
    baglanti = veritabanina_baglan()
    try:
        baglanti.execute(
            """UPDATE parca
               SET ad=?, parca_kodu=?, kategori_no=?, tedarikci_no=?,
                   fiyat=?, stok_miktari=?, aciklama=?
               WHERE no=?""",
            (ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok_miktari, aciklama, parca_no)
        )
        baglanti.commit()
        return True
    except sqlite3.IntegrityError:
        print("Parça kodu çakışması.")
        return False
    except Exception as hata:
        print(f"Parça güncelleme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def parca_sil(parca_no):
    """
    Parçayı siler.
    Bağlı stok hareketleri CASCADE ile otomatik silinir (schema.sql'de tanımlı).
    """
    baglanti = veritabanina_baglan()
    try:
        baglanti.execute("DELETE FROM parca WHERE no = ?", (parca_no,))
        baglanti.commit()
        return True
    except Exception as hata:
        print(f"Parça silme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def stok_hareketi_listele(parca_no=None):
    """
    Stok hareketlerini listeler, en yeniden eskiye sıralar.
    parca_no verilirse sadece o parçanın hareketlerini getirir.
    """
    baglanti = veritabanina_baglan()
    try:
        if parca_no:
            sonuc = baglanti.execute("""
                SELECT sh.*, p.ad AS parca_adi, p.parca_kodu
                FROM stok_hareketi sh
                LEFT JOIN parca p ON sh.parca_no = p.no
                WHERE sh.parca_no = ?
                ORDER BY sh.tarih DESC
            """, (parca_no,)).fetchall()
        else:
            sonuc = baglanti.execute("""
                SELECT sh.*, p.ad AS parca_adi, p.parca_kodu
                FROM stok_hareketi sh
                LEFT JOIN parca p ON sh.parca_no = p.no
                ORDER BY sh.tarih DESC
            """).fetchall()
        return sonuc
    except Exception as hata:
        print(f"Stok hareketi listeleme hatası: {hata}")
        return []
    finally:
        baglanti.close()


def stok_hareketi_ekle(parca_no, miktar, hareket_tipi, aciklama=""):
    """
    Yeni stok hareketi ekler ve parçanın stok miktarını günceller.
    Çıkış yapılacaksa önce yeterli stok var mı kontrol ediyoruz.
    """
    baglanti = veritabanina_baglan()
    try:
        if hareket_tipi == "cikis":
            parca = baglanti.execute(
                "SELECT stok_miktari FROM parca WHERE no = ?", (parca_no,)
            ).fetchone()
            if parca is None:
                return None
            if parca["stok_miktari"] < miktar:
                print(f"Yetersiz stok. Mevcut: {parca['stok_miktari']}, İstenen: {miktar}")
                return None

        imlec = baglanti.execute(
            "INSERT INTO stok_hareketi (parca_no, miktar, hareket_tipi, aciklama) VALUES (?, ?, ?, ?)",
            (parca_no, miktar, hareket_tipi, aciklama)
        )

        if hareket_tipi == "giris":
            baglanti.execute(
                "UPDATE parca SET stok_miktari = stok_miktari + ? WHERE no = ?",
                (miktar, parca_no)
            )
        else:
            baglanti.execute(
                "UPDATE parca SET stok_miktari = stok_miktari - ? WHERE no = ?",
                (miktar, parca_no)
            )

        baglanti.commit()
        return imlec.lastrowid
    except Exception as hata:
        baglanti.rollback()
        print(f"Stok hareketi ekleme hatası: {hata}")
        return None
    finally:
        baglanti.close()


def stok_hareketi_sil(hareket_no):
    """
    Stok hareketini siler ve stok miktarını geri alır.
    Giriş silindiyse stok düşer, çıkış silindiyse stok artar.
    """
    baglanti = veritabanina_baglan()
    try:
        hareket = baglanti.execute(
            "SELECT * FROM stok_hareketi WHERE no = ?", (hareket_no,)
        ).fetchone()

        if hareket is None:
            return False

        if hareket["hareket_tipi"] == "giris":
            baglanti.execute(
                "UPDATE parca SET stok_miktari = stok_miktari - ? WHERE no = ?",
                (hareket["miktar"], hareket["parca_no"])
            )
        else:
            baglanti.execute(
                "UPDATE parca SET stok_miktari = stok_miktari + ? WHERE no = ?",
                (hareket["miktar"], hareket["parca_no"])
            )

        baglanti.execute("DELETE FROM stok_hareketi WHERE no = ?", (hareket_no,))
        baglanti.commit()
        return True
    except Exception as hata:
        baglanti.rollback()
        print(f"Stok hareketi silme hatası: {hata}")
        return False
    finally:
        baglanti.close()


def pano_ozeti():
    """
    Ana sayfa için özet verileri toplar.
    Sonucu sözlük (dict) olarak döndürüyoruz.
    """
    baglanti = veritabanina_baglan()
    try:
        ozet = {
            "toplam_parca": baglanti.execute("SELECT COUNT(*) FROM parca").fetchone()[0],
            "toplam_kategori": baglanti.execute("SELECT COUNT(*) FROM kategori").fetchone()[0],
            "toplam_tedarikci": baglanti.execute("SELECT COUNT(*) FROM tedarikci").fetchone()[0],
            "toplam_hareket": baglanti.execute("SELECT COUNT(*) FROM stok_hareketi").fetchone()[0],
            "toplam_stok_degeri": baglanti.execute(
                "SELECT COALESCE(SUM(fiyat * stok_miktari), 0) FROM parca"
            ).fetchone()[0],
            "dusuk_stoklu": baglanti.execute(
                "SELECT COUNT(*) FROM parca WHERE stok_miktari < 20"
            ).fetchone()[0],
            "son_hareketler": baglanti.execute("""
                SELECT sh.*, p.ad AS parca_adi, p.parca_kodu
                FROM stok_hareketi sh
                LEFT JOIN parca p ON sh.parca_no = p.no
                ORDER BY sh.tarih DESC LIMIT 5
            """).fetchall()
        }
        return ozet
    except Exception as hata:
        print(f"Pano özeti hatası: {hata}")
        return {}
    finally:
        baglanti.close()
