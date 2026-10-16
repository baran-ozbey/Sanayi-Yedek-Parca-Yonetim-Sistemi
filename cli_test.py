import database as vt


def menu_goster():
    """Ana menüyü ekrana basar."""
    print("\n" + "=" * 40)
    print("  Sanayi Yedek Parça - Hızlı Test")
    print("=" * 40)
    print("1. Tüm Parçaları Listele")
    print("2. Kategori Ara")
    print("3. Tedarikçileri Listele")
    print("4. Çıkış")
    print("-" * 40)


def parcalari_listele():
    """Veritabanındaki parçaları ekrana döker."""
    parcalar = vt.parca_listele()
    if not parcalar:
        print("Hiç parça bulunamadı.")
        return
    print(f"\nToplam {len(parcalar)} parça bulundu:\n")
    for p in parcalar:
        print(f"  [{p['parca_kodu']}] {p['ad']}")
        print(f"       Stok: {p['stok_miktari']} adet | Fiyat: {p['fiyat']} TL")
        print(f"       Kategori: {p['kategori_adi']} | Tedarikçi: {p['tedarikci_adi']}")
        print()


def kategori_ara():
    """Kullanıcıdan kategori adı alır ve arar."""
    arama = input("Aramak istediğiniz kategori adını girin: ").strip()
    if not arama:
        print("Arama metni boş olamaz.")
        return

    kategoriler = vt.kategori_listele()
    bulunanlar = [k for k in kategoriler if arama.lower() in k["ad"].lower()]

    if bulunanlar:
        print(f"\n'{arama}' için {len(bulunanlar)} sonuç:")
        for k in bulunanlar:
            print(f"  - NO: {k['no']} | Ad: {k['ad']}")
    else:
        print(f"'{arama}' ile eşleşen kategori bulunamadı.")


def tedarikcileri_listele():
    """Tedarikçileri ekrana basar."""
    tedarikciler = vt.tedarikci_listele()
    if not tedarikciler:
        print("Kayıtlı tedarikçi yok.")
        return
    print(f"\nToplam {len(tedarikciler)} tedarikçi:\n")
    for t in tedarikciler:
        print(f"  {t['ad']} | Tel: {t['telefon']} | E-posta: {t['eposta']}")


def ana_menu():
    """
    Ana program döngüsü.
    Kullanıcı 4 girene kadar menüyü tekrar gösterir.
    """
    print("\nSanayi Yedek Parça Yönetim Sistemi - CLI Test Aracı")

    while True:
        menu_goster()
        secim = input("Seçiminiz (1-4): ").strip()

        if secim == "1":
            parcalari_listele()
        elif secim == "2":
            kategori_ara()
        elif secim == "3":
            tedarikcileri_listele()
        elif secim == "4":
            print("\nÇıkılıyor. Görüşmek üzere!\n")
            break
        else:
            print("Geçersiz seçim, lütfen 1-4 arasında bir değer girin.")


if __name__ == "__main__":
    ana_menu()
