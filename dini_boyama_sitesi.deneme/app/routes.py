from flask import Blueprint, render_template, request
from .models import BoyamaSayfasi, Bilmeceler  # 🆕 Bilmeceler modeli eklendi

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/boyama-sayfalari")
def boyama_sayfalari():
    arama = request.args.get("q")  # Arama kutusundan gelen değer
    if arama:
        sayfalar = BoyamaSayfasi.query.filter(
            (BoyamaSayfasi.baslik.ilike(f"%{arama}%")) |
            (BoyamaSayfasi.aciklama.ilike(f"%{arama}%"))
        ).all()
    else:
        sayfalar = BoyamaSayfasi.query.all()

    return render_template("boyama.html", sayfalar=sayfalar, arama=arama)

# ✅ Ziyaretçiler için bilmece sayfası
@main.route("/bilmeceler")
def bilmeceler():
    kategori = request.args.get("kategori")
    if kategori:
        bilmeceler = Bilmeceler.query.filter_by(kategori=kategori).all()
    else:
        bilmeceler = Bilmeceler.query.all()
    return render_template("bilmeceler.html", bilmeceler=bilmeceler, secili_kategori=kategori)
