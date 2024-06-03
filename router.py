from flask import render_template, request, redirect, url_for, session
from app import app
from classes import *

@app.route("/", methods=["GET", "POST"])
def home():
    if not "marketID" in session:
        return render_template("home.html")
    elif request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        try:
            session["userID"] = request.form["userID"]
        except TypeError:
            print("Zadej cislo")
        return redirect(url_for("home"))

@app.route("/market", methods=["GET", "POST"])
def market():
    if request.method == "GET" and "marketID" in session:
        market = Market.all_markets[session["marketID"]]
        return render_template("market.html", market=market)
    elif request.method == "POST":
        try:
            marketID = int(request.form["marketID"])
        except TypeError:
            print("Zadej cislo")
            return redirect(url_for("home"))
        session["marketID"] = marketID
    return redirect(url_for("home"))