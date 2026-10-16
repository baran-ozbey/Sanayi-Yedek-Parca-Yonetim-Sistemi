class Kategori:
    """Kategori tablosunu temsil eden sınıf."""

    def __init__(self, no=None, ad="", ust_kategori_no=None):
        self.no = no
        self.ad = ad
        self.ust_kategori_no = ust_kategori_no

    def sozluge_cevir(self):
        """Nesneyi sözlüğe (dict) çevirir. JSON için gerekli."""
        return {
            "no": self.no,
            "ad": self.ad,
            "ust_kategori_no": self.ust_kategori_no
        }

    def __repr__(self):
        """Print ile basınca anlamlı bir çıktı verir."""
        return f"Kategori(no={self.no}, ad='{self.ad}')"

    @staticmethod
    def satirdan_oku(satir):
        """Veritabanı satırını alıp Kategori nesnesine çevirir."""
        if satir is None:
            return None
        return Kategori(
            no=satir["no"],
            ad=satir["ad"],
            ust_kategori_no=satir["ust_kategori_no"]
        )


class Tedarikci:
    """Tedarikçi tablosunu temsil eden sınıf."""

    def __init__(self, no=None, ad="", telefon="", eposta="", adres=""):
        self.no = no
        self.ad = ad
        self.telefon = telefon
        self.eposta = eposta
        self.adres = adres

    def sozluge_cevir(self):
        """Sözlüğe çevirir."""
        return {
            "no": self.no,
            "ad": self.ad,
            "telefon": self.telefon,
            "eposta": self.eposta,
            "adres": self.adres
        }

    def __repr__(self):
        return f"Tedarikci(no={self.no}, ad='{self.ad}', eposta='{self.eposta}')"

    @staticmethod
    def satirdan_oku(satir):
        """Veritabanı satırından Tedarikci nesnesi oluşturur."""
        if satir is None:
            return None
        return Tedarikci(
            no=satir["no"],
            ad=satir["ad"],
            telefon=satir["telefon"],
            eposta=satir["eposta"],
            adres=satir["adres"]
        )


class Parca:
    """Parça tablosunu temsil eden sınıf. Sistemin ana modeli."""

    def __init__(self, no=None, ad="", parca_kodu="", kategori_no=None,
                 tedarikci_no=None, fiyat=0.0, stok_miktari=0,
                 aciklama="", kayit_tarihi=""):
        self.no = no
        self.ad = ad
        self.parca_kodu = parca_kodu
        self.kategori_no = kategori_no
        self.tedarikci_no = tedarikci_no
        self.fiyat = fiyat
        self.stok_miktari = stok_miktari
        self.aciklama = aciklama
        self.kayit_tarihi = kayit_tarihi

    def stok_degeri(self):
        """Bu parçanın toplam stok değerini hesaplar (fiyat x miktar)."""
        return self.fiyat * self.stok_miktari

    def sozluge_cevir(self):
        """JSON çıktısı için sözlüğe çevirir."""
        return {
            "no": self.no,
            "ad": self.ad,
            "parca_kodu": self.parca_kodu,
            "kategori_no": self.kategori_no,
            "tedarikci_no": self.tedarikci_no,
            "fiyat": self.fiyat,
            "stok_miktari": self.stok_miktari,
            "aciklama": self.aciklama,
            "kayit_tarihi": self.kayit_tarihi
        }

    def __repr__(self):
        return f"Parca(no={self.no}, ad='{self.ad}', kod='{self.parca_kodu}', stok={self.stok_miktari})"

    @staticmethod
    def satirdan_oku(satir):
        """Veritabanı satırından Parca nesnesi oluşturur."""
        if satir is None:
            return None
        return Parca(
            no=satir["no"],
            ad=satir["ad"],
            parca_kodu=satir["parca_kodu"],
            kategori_no=satir["kategori_no"],
            tedarikci_no=satir["tedarikci_no"],
            fiyat=satir["fiyat"],
            stok_miktari=satir["stok_miktari"],
            aciklama=satir["aciklama"],
            kayit_tarihi=satir["kayit_tarihi"]
        )


class StokHareketi:
    """Stok hareketi tablosunu temsil eden sınıf."""

    HAREKET_TIPLERI = ("giris", "cikis")

    def __init__(self, no=None, parca_no=None, miktar=0,
                 hareket_tipi="giris", tarih="", aciklama=""):
        self.no = no
        self.parca_no = parca_no
        self.miktar = miktar
        self.hareket_tipi = hareket_tipi
        self.tarih = tarih
        self.aciklama = aciklama

    def hareket_tipi_gosterim(self):
        """Ekranda daha güzel görünsün diye Türkçeleştirir."""
        if self.hareket_tipi == "giris":
            return "Giriş"
        return "Çıkış"

    def sozluge_cevir(self):
        """Sözlüğe çevirir."""
        return {
            "no": self.no,
            "parca_no": self.parca_no,
            "miktar": self.miktar,
            "hareket_tipi": self.hareket_tipi,
            "tarih": self.tarih,
            "aciklama": self.aciklama
        }

    def __repr__(self):
        return f"StokHareketi(no={self.no}, parca_no={self.parca_no}, miktar={self.miktar}, tip='{self.hareket_tipi}')"

    @staticmethod
    def satirdan_oku(satir):
        """Veritabanı satırından StokHareketi nesnesi oluşturur."""
        if satir is None:
            return None
        return StokHareketi(
            no=satir["no"],
            parca_no=satir["parca_no"],
            miktar=satir["miktar"],
            hareket_tipi=satir["hareket_tipi"],
            tarih=satir["tarih"],
            aciklama=satir["aciklama"]
        )
