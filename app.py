# -*- coding: utf-8 -*-
from enum import Enum
from flask import Flask, render_template, request, flash, redirect, url_for
from markupsafe import Markup
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *
from flask_bootstrap import Bootstrap5, SwitchField
from zebra import Zebra

app = Flask(__name__)
app.secret_key = "dev"

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

#z = Zebra("ZDesigner ZD620-300dpi ZPL")
z = Zebra("ZTC-ZD620-300dpi-ZPL")

z.setup(direct_thermal=True, label_height=(300 * 2, 0), label_width=300 * 4)

FIRST_LOGO = """
^FO768,416^GFA,09984,09984,00052,:Z64:
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:6FBC
"""


def print_badge(
    first: str,
    last: str,
    position: str,
    event: str,
    first_alumni: bool,
    speed: int = 3,
    darkness: int = 30,
):
    if first_alumni:
        extra_images = FIRST_LOGO
    else:
        extra_images = ""

    z.output(
        rf"""^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR{speed},{speed}~SD{darkness}^JUS^LRN^CI0^XZ
^XA
^MMT
^PW1200
^LL0600
^LS0
^FO0,448^GFA,08960,08960,00056,:Z64:
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:F89F{extra_images}
^FT0,130^A@N,117,112,TRE000.FNT
^FH\
^FB1200,1,0,C ^FH\^CI17^F8 ^FD{first}^FS ^CI0
^FT0,240^A@N,75,72,TRE000.FNT
^FH\
^FB1200,1,0,C ^FH\^CI17^F8 ^FD{last}^FS ^CI0
^FT0,333^A@N,58,60,DUB001.FNT
^FH\
^FB1200,1,0,C ^FH\^CI17^F8 ^FD{position}^FS ^CI0
^FT0,424^A@N,58,60,DUB001.FNT
^FH\
^FB1200,1,0,C ^FH\^CI17^F8 ^FD{event}^FS ^CI0
^LRY^FO1,269^GB1198,0,93^FS^LRN
^PQ1,0,1,Y^XZ"""
    )


class HelloForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    event = SelectField(
        "Event",
        choices=[
            ("2024 Ventura County Regional", "2024 Ventura County Regional"),
            ("2024 Hueneme Port Regional", "2024 Hueneme Port Regional"),
        ],
    )
    first_alumni = BooleanField("FIRST Alumni?")
    submit = SubmitField()


@app.route("/", methods=["GET", "POST"])
def index():
    form = HelloForm()

    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data

        flash(f"Label printed for {first} {last}!")

        print_badge(
            first=first,
            last=last,
            position=form.position.data,
            event=form.event.data,
            first_alumni=form.first_alumni.data,
        )
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        form=form,
    )


@app.route("/bulk", methods=["GET", "POST"])
def bulk():
    form = HelloForm()

    return render_template(
        "bulk.html",
        form=form,
    )


if __name__ == "__main__":
    app.run(debug=True)
