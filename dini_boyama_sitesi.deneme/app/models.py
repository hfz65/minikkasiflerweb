from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BoyamaSayfasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100))
    aciklama = db.Column(db.Text)
    resim_yolu = db.Column(db.String(200))

class Bilmeceler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    soru = db.Column(db.String(255), nullable=False)
    cevap = db.Column(db.String(255), nullable=False)
    kategori = db.Column(db.String(100))  # örn: 'Hayvanlar', 'Ramazan', 'Eğlenceli'
