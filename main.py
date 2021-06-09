from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)




class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", all_cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get('name')
        map_url = request.form.get('mapurl')
        img_url = request.form.get('imgurl')
        location = request.form.get('location')
        seats = request.form.get('seats')
        coffee_price = request.form.get('price')
        if bool(request.form.get("has_toilet")):
            has_toilet = 1
        else:
            has_toilet = 0
        if bool(request.form.get("has_wifi")):
            has_wifi = 1
        else:
            has_wifi = 0
        if bool(request.form.get("can_take_calls")):
            can_take_calls = 1
        else:
            can_take_calls = 0
        if bool(request.form.get("has_sockets")):
            has_sockets = 1
        else:
            has_sockets = 0
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            seats=seats,
            coffee_price=f"£{coffee_price}",
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            has_sockets=has_sockets
        )
        db.session.add(new_cafe)
        db.session.commit()
        print(has_toilet)
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)