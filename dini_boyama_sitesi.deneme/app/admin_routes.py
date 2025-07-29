import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from .models import db, BoyamaSayfasi, Bilmeceler  # ✅ Bilmeceler modeli eklendi

admin = Blueprint("admin", __name__)
ADMIN_PASSWORD = ".5Meter"

# 🔐 Admin Giriş
@admin.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin.admin_panel"))
    return render_template("admin_login.html")


# 🖼️ Boyama Sayfaları Paneli
@admin.route("/admin/panel", methods=["GET", "POST"])
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("admin.admin_login"))

    if request.method == "POST":
        baslik = request.form["baslik"]
        aciklama = request.form["aciklama"]
        dosya = request.files["resim"]

        if dosya:
            dosya_adi = secure_filename(dosya.filename)
            yol = os.path.join("app/static/uploads", dosya_adi)
            dosya.save(yol)

            yeni = BoyamaSayfasi(baslik=baslik, aciklama=aciklama, resim_yolu=dosya_adi)
            db.session.add(yeni)
            db.session.commit()

    arama = request.args.get("q")
    if arama:
        sayfalar = BoyamaSayfasi.query.filter(
            (BoyamaSayfasi.baslik.ilike(f"%{arama}%")) |
            (BoyamaSayfasi.aciklama.ilike(f"%{arama}%"))
        ).all()
    else:
        sayfalar = BoyamaSayfasi.query.all()

    return render_template("admin.html", sayfalar=sayfalar, arama=arama)


# ✅ BİLMECE PANELİ – Listele & Ekle
@admin.route("/admin/bilmeceler", methods=["GET", "POST"])
def admin_bilmeceler():
    if not session.get("admin"):
        return redirect(url_for("admin.admin_login"))

    if request.method == "POST":
        soru = request.form["soru"]
        cevap = request.form["cevap"]
        kategori = request.form["kategori"]
        yeni = Bilmeceler(soru=soru, cevap=cevap, kategori=kategori)
        db.session.add(yeni)
        db.session.commit()

    bilmeceler = Bilmeceler.query.all()
    return render_template("admin_bilmeceler.html", bilmeceler=bilmeceler)


# 📝 Bilmece Düzenle
@admin.route("/admin/bilmece/duzenle/<int:id>", methods=["GET", "POST"])
def admin_bilmece_duzenle(id):
    if not session.get("admin"):
        return redirect(url_for("admin.admin_login"))

    bilmece = Bilmeceler.query.get_or_404(id)

    if request.method == "POST":
        bilmece.soru = request.form["soru"]
        bilmece.cevap = request.form["cevap"]
        bilmece.kategori = request.form["kategori"]
        db.session.commit()
        return redirect(url_for("admin.admin_bilmeceler"))

    return render_template("admin_bilmece_duzenle.html", bilmece=bilmece)


# 🗑 Bilmece Sil
@admin.route("/admin/bilmece/sil/<int:id>")
def admin_bilmece_sil(id):
    if not session.get("admin"):
        return redirect(url_for("admin.admin_login"))

    bilmece = Bilmeceler.query.get_or_404(id)
    db.session.delete(bilmece)
    db.session.commit()
    return redirect(url_for("admin.admin_bilmeceler"))


# 🖼 Sil
@admin.route("/admin/delete/<int:id>")
def admin_delete(id):
    if not session.get("admin"):
        return redirect(url_for("admin.admin_login"))

    sayfa = BoyamaSayfasi.query.get_or_404(id)
    dosya_yolu = os.path.join("app/static/uploads", sayfa.resim_yolu)
    if os.path.exists(dosya_yolu):
        os.remove(dosya_yolu)

    db.session.delete(sayfa)
    db.session.commit()
    return redirect(url_for("admin.admin_panel"))


# ✏️ Düzenle
@admin.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def admin_edit(id):
    if not session.get("admin"):
        return redirect(url_for("admin.admin_login"))

    sayfa = BoyamaSayfasi.query.get_or_404(id)

    if request.method == "POST":
        sayfa.baslik = request.form["baslik"]
        sayfa.aciklama = request.form["aciklama"]
        db.session.commit()
        return redirect(url_for("admin.admin_panel"))

    return render_template("admin_edit.html", sayfa=sayfa)
