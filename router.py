from flask import render_template, request, redirect, url_for, session, flash
from app import app
from classes import *

@app.route("/", methods=["GET", "POST"])
def home():
    load("save.txt")
    if not "marketID" in session:
        return render_template("home.html")
    elif request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        try:
            session["userID"] = int(request.form["userID"])
        except TypeError:
            print("Zadej cislo")
        return redirect(url_for("market"))

@app.route("/market", methods=["GET", "POST"])
def market():
    load("save.txt")
    if request.method == "GET" and "marketID" in session:
        market = Market.all_markets[session["marketID"]]
        usr = Trader.all_traders[session["userID"]]
        table = make_table(market, usr) #dělá tabulku, která pak může být zobrazena
        return render_template("market.html", market=market, table=table, usr=usr)
    elif request.method == "POST":
        try:
            marketID = int(request.form["marketID"])
        except TypeError:
            print("Zadej cislo")
            return redirect(url_for("home"))
        session["marketID"] = marketID
    return redirect(url_for("home"))

def make_table(market, user):
    table = []
    for stock in Stock.all_stocks.values():
        amount = user.stocks[stock.short]
        price = market.stocks[stock.short][2]
        max_buy = user.money // price
        table.append([stock.name, stock.short, amount, price, max_buy])
    return table

@app.route("/buy", methods=["POST"])
def buy():
    market = Market.all_markets[session["marketID"]]
    usr = Trader.all_traders[session["userID"]]
    for stockAction, amount in request.form.items():
        if not amount: continue #if form is empty
        amount = int(amount)
        short, action = stockAction.split("/")
        if action == "buy":
            market.trade(usr.code, short, amount) #buys a stock
        else:
            market.trade(usr.code, short, -amount)#sells a stock
    session.pop("userID", None)
    save("save.txt")
    return redirect(url_for("home"))

@app.errorhandler(Exception)
def error_site(e):
    flash(str(e))
    return redirect(url_for("home"))