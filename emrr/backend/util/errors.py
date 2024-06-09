from routes import app
from flask import render_template

@app.errorhandler(403)
def forbidden(e):
    return render_template('null.html'), 403


@app.errorhandler(500)
def serverError(e):
    return render_template('null.html'), 500


@app.errorhandler(Exception)
def defaultHandler(e):
    return render_template('null.html')