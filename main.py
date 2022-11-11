from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import os


# Connect to Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafe.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TopsecretAPIKEY'] = os.environ.get('TopsecretAPIKEY')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)

db = SQLAlchemy(app)
del_key = os.environ.get('del_key')


class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Cafe Map Url", validators=[DataRequired()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    seats = StringField("Number of seats in cafe", validators=[DataRequired()])
    toilet = BooleanField("Has toilets?", false_values=('None', 'none', 'no'), default='yes')
    wifi = BooleanField("Has wifi?", false_values=('None', 'none', 'no'), default='yes')
    sockets = BooleanField("Has sockets?", false_values=('None', 'none', 'no'), default='yes')
    calls = BooleanField("Can take calls?", false_values=('None', 'none', 'no'), default='yes')
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    key = StringField("Your secret key", validators=[DataRequired()])
    submit = SubmitField("Submit Request")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=True)
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=True)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=True)
    has_sockets = db.Column(db.Boolean, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)

# db.create_all()


@app.route("/")
def home():
    cafes = Cafe.query.all()
    caf_len = len(cafes)
    return render_template("index.html", cafes=cafes, caf_len=caf_len)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.toilet.data,
            has_wifi=form.wifi.data,
            has_sockets=form.sockets.data,
            can_take_calls=form.calls.data,
            coffee_price=form.coffee_price.data
        )

        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add.html", form=form)


@app.route(f"/{del_key}")
def admin_site():
    cafes = Cafe.query.all()
    caf_len = len(cafes)
    return render_template("admin.html", cafes=cafes, caf_len=caf_len)


@app.route(f"/{del_key}/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("admin_site"))


if __name__ == '__main__':
    app.run(debug=True)
