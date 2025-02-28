from flask import Flask, render_template, session, request, redirect, url_for, flash
from backend import data_to_region_stat, data_to_school_stat
import html_parser as parser

app = Flask(__name__)

@app.route('/')
def statistics_by_region():
    return render_template('stat.html', arr = data_to_region_stat())

@app.route('/stat_by_school')
def statistics_by_school():
    return render_template('stat.html', arr = data_to_school_stat())

@app.route('/results')
def results():
    return render_template('stat.html', arr = {})

@app.route('/dashboard/<int:id>')
def dashboard(id):
    return render_template('stat.html', arr = {})

@app.route('/standings')
def standings():
    round  = request.args.get('round')  or 'both' # 1/2/both
    grade  = request.args.get('grade')  or 'all'  # all/11/10/9/10l/9l/8l
    style  = request.args.get('style')  or 'rich' # rich/bare
    school = request.args.get('school') or 'all'  # all/<school name>
    time   = request.args.get('time')   or 'end'  # end/<time>
    


if __name__ == "__main__":
    import __init__db
    parser.populate_db()
    app.run(host="0.0.0.0", port=5000)
