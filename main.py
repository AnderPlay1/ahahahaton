from flask import Flask, render_template, session, request, redirect, url_for, flash
from backend import data_to_region_stat
app = Flask(__name__)

@app.route('/')
def statistics_by_region():
    return render_template('stat.html', arr = data_to_region_stat())

@app.route('/stat_by_school')
def statistics_by_school():
    return render_template('stat.html', arr = {})

@app.route('/results')
def results():
    return render_template('stat.html', arr = {})

@app.route('/dashboard/<int:id>')
def dashboard(id):
    return render_template('stat.html', arr = {})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)