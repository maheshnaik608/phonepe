
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "phonepe-demo-secret"

balance = 25000.00
transactions = []

@app.route("/")
def home():
    return render_template(
        "index.html",
        balance=balance,
        transactions=transactions
    )

@app.route("/send", methods=["POST"])
def send_money():
    global balance

    name = request.form.get("name")
    mobile = request.form.get("mobile")
    amount = float(request.form.get("amount", 0))

    if not name or not mobile or amount <= 0:
        flash("Please enter valid payment details!")
    elif amount > balance:
        flash("Insufficient demo balance!")
    else:
        balance -= amount

        transactions.insert(0, {
            "name": name,
            "mobile": mobile,
            "amount": amount,
            "type": "Money Sent",
            "status": "Successful"
        })

        flash(f"₹{amount:.2f} sent successfully!")

    return redirect(url_for("home"))

@app.route("/add-money", methods=["POST"])
def add_money():
    global balance

    amount = float(request.form.get("amount", 0))

    if amount > 0:
        balance += amount
        transactions.insert(0, {
            "name": "Demo Wallet",
            "mobile": "-",
            "amount": amount,
            "type": "Money Added",
            "status": "Successful"
        })
        flash(f"₹{amount:.2f} added to demo balance!")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
