from flask import Flask, render_template, url_for
from PrivateClinic import app
from PrivateClinic.admin import *


@app.route("/")
def index():
    return render_template('display.html')
@app.route("/login")
def user_login():
    return render_template('login.html')
@app.route("/appointment")
def appointment_book():
    return render_template('appointment.html')
if __name__ == "__main__":
    from PrivateClinic import admin

    app.run(debug=True)
