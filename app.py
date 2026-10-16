from flask import (Flask, render_template, request, redirect,
                   url_for, jsonify, flash, send_file)
import csv
import os
import io
from datetime import datetime
import webbrowser

import database as vt
from models import Parca, Kategori, Tedarikci, StokHareketi

app = Flask(__name__)
app.secret_key = "sanayi_parca_gizli_anahtar_2026"

LOG_DOSYASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uygulama.log")

def log_yaz(mesaj):
    """
    Uygulama logunu dosyaya yazar.
    Dosya işlemleri - with bloğuyla açıp otomatik kapatıyoruz.
    """
    try:
        with open(LOG_DOSYASI, "a", encoding="utf-8") as f:
            zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{zaman}] {mesaj}\n")
    except Exception as hata:
        print(f"Log yazılamadı: {hata}")


@app.route("/")
def ana_sayfa():
    """Ana sayfa - özet istatistikleri gösterir."""
    try:
        ozet = vt.pano_ozeti()
        log_yaz("Ana sayfa açıldı.")
        return render_template("index.html", ozet=ozet)
    except Exception as hata:
        log_yaz(f"Ana sayfa hatası: {hata}")
        flash(f"Bir hata oluştu: {hata}", "danger")
        return render_template("index.html", ozet={})


@app.route("/kategoriler")
def kategoriler():
    """Kategoriler sayfası - GET isteğiyle liste döner."""
    try:
        liste = vt.kategori_listele()
        agac = vt.kategori_agaci_duz()
        return render_template("kategoriler.html", kategoriler=liste, agac=agac)
    except Exception as hata:
        flash("Kategoriler yüklenemedi.", "danger")
        return render_template("kategoriler.html", kategoriler=[], agac=[])


@app.route("/kategoriler/ekle", methods=["POST"])
def kategori_ekle():
    """Formdan gelen veriyle yeni kategori ekler."""
    try:
        ad = request.form.get("ad", "").strip()
        ust_no = request.form.get("ust_kategori_no")
        ust_no = int(ust_no) if ust_no else None

        if not ad:
            flash("Kategori adı boş bırakılamaz!", "warning")
            return redirect(url_for("kategoriler"))

        sonuc = vt.kategori_ekle(ad, ust_no)
        if sonuc:
            flash(f"'{ad}' kategorisi eklendi.", "success")
            log_yaz(f"Kategori eklendi: {ad}")
        else:
            flash("Kategori eklenemedi.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("kategoriler"))


@app.route("/kategoriler/guncelle/<int:kno>", methods=["POST"])
def kategori_guncelle(kno):
    """Mevcut kategoriyi günceller."""
    try:
        ad = request.form.get("ad", "").strip()
        ust_no = request.form.get("ust_kategori_no")
        ust_no = int(ust_no) if ust_no else None

        if not ad:
            flash("Kategori adı boş bırakılamaz!", "warning")
            return redirect(url_for("kategoriler"))

        if vt.kategori_guncelle(kno, ad, ust_no):
            flash("Kategori güncellendi.", "success")
        else:
            flash("Güncelleme başarısız.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("kategoriler"))


@app.route("/kategoriler/sil/<int:kno>", methods=["POST"])
def kategori_sil(kno):
    """Kategoriyi siler. Bağlı parça varsa hata mesajı gösterir."""
    try:
        if vt.kategori_sil(kno):
            flash("Kategori silindi.", "success")
        else:
            flash("Silinemedi. Bu kategoriye bağlı parçalar olabilir.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("kategoriler"))


@app.route("/tedarikciler")
def tedarikciler():
    """Tedarikçiler listesi sayfası."""
    try:
        liste = vt.tedarikci_listele()
        return render_template("tedarikciler.html", tedarikciler=liste)
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
        return render_template("tedarikciler.html", tedarikciler=[])


@app.route("/tedarikciler/ekle", methods=["POST"])
def tedarikci_ekle():
    """Yeni tedarikçi ekler."""
    try:
        ad = request.form.get("ad", "").strip()
        telefon = request.form.get("telefon", "").strip()
        eposta = request.form.get("eposta", "").strip()
        adres = request.form.get("adres", "").strip()

        if not ad or not eposta:
            flash("Firma adı ve e-posta zorunludur!", "warning")
            return redirect(url_for("tedarikciler"))

        sonuc = vt.tedarikci_ekle(ad, telefon, eposta, adres)
        if sonuc:
            flash(f"'{ad}' eklendi.", "success")
            log_yaz(f"Tedarikçi eklendi: {ad}")
        else:
            flash("Bu e-posta zaten kayıtlı!", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("tedarikciler"))


@app.route("/tedarikciler/guncelle/<int:tno>", methods=["POST"])
def tedarikci_guncelle(tno):
    """Tedarikçi bilgilerini günceller."""
    try:
        ad = request.form.get("ad", "").strip()
        telefon = request.form.get("telefon", "").strip()
        eposta = request.form.get("eposta", "").strip()
        adres = request.form.get("adres", "").strip()

        if vt.tedarikci_guncelle(tno, ad, telefon, eposta, adres):
            flash("Tedarikçi güncellendi.", "success")
        else:
            flash("Güncelleme başarısız.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("tedarikciler"))


@app.route("/tedarikciler/sil/<int:tno>", methods=["POST"])
def tedarikci_sil(tno):
    """Tedarikçiyi siler."""
    try:
        if vt.tedarikci_sil(tno):
            flash("Tedarikçi silindi.", "success")
        else:
            flash("Silinemedi. Bağlı parçalar olabilir.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("tedarikciler"))


@app.route("/parcalar")
def parcalar():
    """Parça listesi sayfası. Arama ve kategori filtresi destekliyor."""
    try:
        arama = request.args.get("arama", "")
        kat_no = request.args.get("kategori_no", "")
        kat_no = int(kat_no) if kat_no else None

        liste = vt.parca_listele(arama=arama, kategori_no=kat_no)
        kat_listesi = vt.kategori_listele()
        ted_listesi = vt.tedarikci_listele()

        return render_template("parcalar.html",
                               parcalar=liste,
                               kategoriler=kat_listesi,
                               tedarikciler=ted_listesi,
                               arama=arama,
                               secili_kategori=kat_no)
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
        return render_template("parcalar.html", parcalar=[],
                               kategoriler=[], tedarikciler=[],
                               arama="", secili_kategori=None)


@app.route("/parcalar/ekle", methods=["POST"])
def parca_ekle():
    """Yeni parça ekler."""
    try:
        ad = request.form.get("ad", "").strip()
        parca_kodu = request.form.get("parca_kodu", "").strip().upper()
        kategori_no = int(request.form.get("kategori_no", 0))
        tedarikci_no = int(request.form.get("tedarikci_no", 0))
        fiyat = float(request.form.get("fiyat", 0))
        stok = int(request.form.get("stok_miktari", 0))
        aciklama = request.form.get("aciklama", "").strip()

        if not ad or not parca_kodu:
            flash("Parça adı ve kodu zorunludur!", "warning")
            return redirect(url_for("parcalar"))

        sonuc = vt.parca_ekle(ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok, aciklama)
        if sonuc:
            flash(f"'{ad}' eklendi.", "success")
            log_yaz(f"Parça eklendi: {ad} ({parca_kodu})")
        else:
            flash("Parça kodu zaten mevcut!", "danger")
    except ValueError:
        flash("Fiyat ve stok sayısal olmalıdır!", "warning")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("parcalar"))


@app.route("/parcalar/guncelle/<int:pno>", methods=["POST"])
def parca_guncelle(pno):
    """Parça bilgilerini günceller."""
    try:
        ad = request.form.get("ad", "").strip()
        parca_kodu = request.form.get("parca_kodu", "").strip().upper()
        kategori_no = int(request.form.get("kategori_no", 0))
        tedarikci_no = int(request.form.get("tedarikci_no", 0))
        fiyat = float(request.form.get("fiyat", 0))
        stok = int(request.form.get("stok_miktari", 0))
        aciklama = request.form.get("aciklama", "").strip()

        if vt.parca_guncelle(pno, ad, parca_kodu, kategori_no, tedarikci_no, fiyat, stok, aciklama):
            flash("Parça güncellendi.", "success")
        else:
            flash("Güncelleme başarısız.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("parcalar"))


@app.route("/parcalar/sil/<int:pno>", methods=["POST"])
def parca_sil(pno):
    """Parçayı siler."""
    try:
        if vt.parca_sil(pno):
            flash("Parça silindi.", "success")
        else:
            flash("Silme başarısız.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("parcalar"))


@app.route("/stok")
def stok():
    """Stok hareketleri sayfası."""
    try:
        parca_no = request.args.get("parca_no", "")
        parca_no = int(parca_no) if parca_no else None
        hareketler = vt.stok_hareketi_listele(parca_no)
        parca_listesi = vt.parca_listele()
        return render_template("stok.html",
                               hareketler=hareketler,
                               parcalar=parca_listesi,
                               secili_parca=parca_no)
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
        return render_template("stok.html", hareketler=[], parcalar=[], secili_parca=None)


@app.route("/stok/ekle", methods=["POST"])
def stok_ekle():
    """Stok giriş veya çıkış hareketi ekler."""
    try:
        parca_no = int(request.form.get("parca_no", 0))
        miktar = int(request.form.get("miktar", 0))
        hareket_tipi = request.form.get("hareket_tipi", "giris")
        aciklama = request.form.get("aciklama", "").strip()

        if miktar <= 0:
            flash("Miktar sıfırdan büyük olmalıdır!", "warning")
            return redirect(url_for("stok"))

        sonuc = vt.stok_hareketi_ekle(parca_no, miktar, hareket_tipi, aciklama)
        if sonuc:
            tip_str = "Giriş" if hareket_tipi == "giris" else "Çıkış"
            flash(f"Stok {tip_str}: {miktar} adet kaydedildi.", "success")
            log_yaz(f"Stok hareketi: {tip_str} - {miktar} adet, Parça NO={parca_no}")
        else:
            flash("İşlem başarısız. Yetersiz stok olabilir!", "danger")
    except ValueError:
        flash("Miktar sayısal olmalıdır!", "warning")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("stok"))


@app.route("/stok/sil/<int:hno>", methods=["POST"])
def stok_sil(hno):
    """Stok hareketini siler ve stoğu geri alır."""
    try:
        if vt.stok_hareketi_sil(hno):
            flash("Stok hareketi silindi.", "success")
        else:
            flash("Silme başarısız.", "danger")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
    return redirect(url_for("stok"))


@app.route("/istatistik")
def istatistik():
    """İstatistik ve grafik sayfası."""
    try:
        return render_template("istatistik.html")
    except Exception as hata:
        flash(f"Hata: {hata}", "danger")
        return render_template("istatistik.html")


@app.route("/api/istatistik/grafik/<grafik_tipi>")
def istatistik_grafik(grafik_tipi):
    """
    Matplotlib ile grafik oluşturup PNG olarak döndürür.
    Pandas ile veritabanı verilerini analiz ediyoruz.
    Numpy ile sayısal işlemler yapıyoruz.
    """
    try:
        import numpy as np
        import pandas as pd
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot as plt

        plt.rcParams.update({
            "text.color": "white",
            "axes.labelcolor": "white",
            "axes.edgecolor": "#444",
            "xtick.color": "white",
            "ytick.color": "white",
            "figure.facecolor": "#1a1a2e",
            "axes.facecolor": "#1a1a2e",
            "legend.facecolor": "#1a1a2e",
            "legend.edgecolor": "#444",
            "legend.labelcolor": "white",
        })

        baglanti = vt.veritabanina_baglan()

        if grafik_tipi == "stok_degeri":
            df = pd.read_sql_query(
                "SELECT ad, fiyat, stok_miktari, (fiyat * stok_miktari) AS deger FROM parca ORDER BY deger DESC LIMIT 10",
                baglanti
            )
            fig, ax = plt.subplots(figsize=(10, 5))
            renkler = plt.cm.viridis(np.linspace(0.3, 0.9, len(df)))
            ax.barh(df["ad"], df["deger"], color=renkler)
            ax.set_xlabel("Stok Değeri (₺)", fontsize=12)
            ax.set_title("En Yüksek Stok Değerine Sahip Parçalar", fontsize=14, fontweight="bold")
            ax.invert_yaxis()
            plt.tight_layout()

        elif grafik_tipi == "kategori_dagilim":
            df = pd.read_sql_query(
                "SELECT k.ad, COUNT(p.no) AS adet FROM kategori k LEFT JOIN parca p ON k.no = p.kategori_no GROUP BY k.no HAVING adet > 0 ORDER BY adet DESC",
                baglanti
            )
            fig, ax = plt.subplots(figsize=(9, 6))
            renkler = plt.cm.Set3(np.arange(len(df)))
            parcalar_grafik, etiketler, oto_etiketler = ax.pie(
                df["adet"], labels=df["ad"], autopct="%1.1f%%",
                colors=renkler, startangle=140,
                pctdistance=0.75, labeldistance=1.15,
                textprops={"fontsize": 9}
            )
            for oto in oto_etiketler:
                oto.set_color("#333")
                oto.set_fontweight("bold")
            ax.set_title("Kategorilere Göre Parça Dağılımı", fontsize=14, fontweight="bold")

        elif grafik_tipi == "hareket_trend":
            df = pd.read_sql_query(
                "SELECT DATE(tarih) AS gun, hareket_tipi, SUM(miktar) AS toplam FROM stok_hareketi GROUP BY gun, hareket_tipi ORDER BY gun",
                baglanti
            )
            fig, ax = plt.subplots(figsize=(12, 5))
            df["gun"] = pd.to_datetime(df["gun"])
            for tip in ["giris", "cikis"]:
                veri = df[df["hareket_tipi"] == tip]
                etiket = "Giriş" if tip == "giris" else "Çıkış"
                renk = "#2ecc71" if tip == "giris" else "#e74c3c"
                ax.bar(veri["gun"], veri["toplam"], label=etiket, color=renk, width=1.5)
            ax.set_xlabel("Tarih", fontsize=12)
            ax.set_ylabel("Miktar", fontsize=12)
            ax.set_title("Stok Hareket Trendi (Günlük)", fontsize=14, fontweight="bold")
            ax.legend()
            from matplotlib.dates import DateFormatter
            ax.set_xticks(df["gun"].unique())
            ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45, ha="right", fontsize=9)
            plt.tight_layout()

        elif grafik_tipi == "tedarikci_parca":
            from matplotlib.ticker import MaxNLocator
            df = pd.read_sql_query(
                "SELECT t.ad, COUNT(p.no) AS adet FROM tedarikci t LEFT JOIN parca p ON t.no = p.tedarikci_no GROUP BY t.no ORDER BY adet DESC",
                baglanti
            )
            fig, ax = plt.subplots(figsize=(12, 5))
            renkler = plt.cm.plasma(np.linspace(0.2, 0.8, len(df)))
            ax.bar(df["ad"], df["adet"], color=renkler)
            ax.set_ylabel("Parça Sayısı", fontsize=12)
            ax.set_title("Tedarikçi Bazında Parça Sayısı", fontsize=14, fontweight="bold")
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.xticks(rotation=35, ha="right", fontsize=9)
            plt.tight_layout()

        else:
            baglanti.close()
            return "Geçersiz grafik tipi", 404

        baglanti.close()

        tampon = io.BytesIO()
        fig.savefig(tampon, format="png", dpi=100, bbox_inches="tight",
                    facecolor="#1a1a2e", edgecolor="none")
        plt.close(fig)
        tampon.seek(0)
        return send_file(tampon, mimetype="image/png")

    except ImportError:
        return "numpy, pandas ve matplotlib kurulu olmalı: pip install numpy pandas matplotlib", 500
    except Exception as hata:
        log_yaz(f"Grafik hatası: {hata}")
        return f"Grafik oluşturulamadı: {hata}", 500


@app.route("/api/istatistik/ozet")
def istatistik_ozet():
    """
    Numpy ile hesaplanan istatistikleri JSON olarak döndürür.
    Pandas ile veri analizi yapıyoruz.
    """
    try:
        import numpy as np
        import pandas as pd

        baglanti = vt.veritabanina_baglan()
        df = pd.read_sql_query("SELECT * FROM parca", baglanti)
        baglanti.close()

        fiyatlar = np.array(df["fiyat"].tolist())
        stoklar = np.array(df["stok_miktari"].tolist())

        ozet = {
            "toplam_parca": int(len(df)),
            "ortalama_fiyat": round(float(np.mean(fiyatlar)), 2),
            "max_fiyat": round(float(np.max(fiyatlar)), 2),
            "min_fiyat": round(float(np.min(fiyatlar)), 2),
            "toplam_stok": int(np.sum(stoklar)),
            "ortalama_stok": round(float(np.mean(stoklar)), 2),
            "toplam_deger": round(float(np.sum(fiyatlar * stoklar)), 2),
            "std_fiyat": round(float(np.std(fiyatlar)), 2),
        }
        return jsonify(ozet)
    except Exception as hata:
        return jsonify({"hata": str(hata)}), 500


@app.route("/api/csv/parcalar")
def csv_parcalar():
    """Parça listesini CSV dosyası olarak indirir."""
    try:
        liste = vt.parca_listele()
        cikti = io.StringIO()
        yazar = csv.writer(cikti)
        yazar.writerow(["NO", "Ad", "Parça Kodu", "Kategori", "Tedarikçi", "Fiyat", "Stok", "Açıklama"])
        for p in liste:
            yazar.writerow([p["no"], p["ad"], p["parca_kodu"],
                            p["kategori_adi"], p["tedarikci_adi"],
                            p["fiyat"], p["stok_miktari"], p["aciklama"]])
        cikti.seek(0)
        tampon = io.BytesIO(cikti.getvalue().encode("utf-8-sig"))
        log_yaz("CSV dışa aktarıldı.")
        return send_file(tampon, mimetype="text/csv",
                         as_attachment=True,
                         download_name="parcalar.csv")
    except Exception as hata:
        flash(f"CSV hatası: {hata}", "danger")
        return redirect(url_for("parcalar"))


@app.route("/api/kategoriler")
def api_kategoriler():
    """Kategorileri JSON olarak döndürür (GET)."""
    agac = vt.kategori_agaci()
    return jsonify(agac)


@app.route("/api/parcalar")
def api_parcalar():
    """
    Tüm parçaları JSON olarak döndürür (GET).
    Burada OOP kullanıyoruz - Parca.satirdan_oku() ile nesneye çevirip
    sozluge_cevir() ile JSON'a dönüştürüyoruz.
    """
    liste = vt.parca_listele()
    sonuc = []
    for p in liste:
        nesne = Parca.satirdan_oku(p)
        sonuc.append(nesne.sozluge_cevir())
    return jsonify(sonuc)


@app.route("/api/parcalar/<int:pno>", methods=["GET", "PUT", "DELETE"])
def api_parca_detay(pno):
    """
    RESTful API - GET, PUT, DELETE metodlarını destekler.
    Bu route sayesinde farklı HTTP metodlarını göstermiş oluyoruz.
    """
    if request.method == "GET":
        parca = vt.parca_getir(pno)
        if parca:
            return jsonify(Parca.satirdan_oku(parca).sozluge_cevir())
        return jsonify({"hata": "Parça bulunamadı"}), 404

    elif request.method == "DELETE":
        sonuc = vt.parca_sil(pno)
        return jsonify({"basari": sonuc})

    elif request.method == "PUT":
        veri = request.get_json() or {}
        yeni_fiyat = veri.get("fiyat", 0)
        return jsonify({"mesaj": "PUT isteği alındı", "gelen_fiyat": yeni_fiyat})


@app.errorhandler(404)
def sayfa_bulunamadi(hata):
    """404 - Sayfa bulunamadı."""
    return render_template("hata.html", kod=404, mesaj="Sayfa bulunamadı!"), 404


@app.errorhandler(500)
def sunucu_hatasi(hata):
    """500 - Sunucu hatası."""
    log_yaz(f"500 hatası: {hata}")
    return render_template("hata.html", kod=500, mesaj="Sunucu hatası oluştu!"), 500


if __name__ == "__main__":
    if not os.path.exists(vt.VT_YOLU):
        print("Veritabanı bulunamadı, oluşturuluyor...")
        vt.veritabanini_baslat()
    else:
        print("Veritabanı mevcut.")

    print("=" * 45)
    
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        webbrowser.open("http://127.0.0.1:5000")
        
    app.run(debug=True)
