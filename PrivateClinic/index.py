from flask import Flask, render_template
from PrivateClinic import app
@app.route("/")
def index():
    return render_template('display.html')

if __name__ == "__main__":
    app.run(debug=True)