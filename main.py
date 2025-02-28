from flask import Flask, render_template, session, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/')
def statistics_by_region():
    return render_template('stat.html')

@app.route('/stat_by_school')
def statistics_by_school():
    return render_template('stat.html')

@app.route('/results')
def results():
    return render_template('stat.html')

@app.route('/dashboard/<int:id>')
def dashboard(id):
    return render_template('stat.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)