from flask import Flask, render_template, session, request, redirect, url_for, flash
from backend import data_to_region_stat, data_to_school_stat, dashboard_data
import html_parser as parser
from db_functions import search
import db_functions as db

app = Flask(__name__)


@app.route("/")
def statistics_by_region():
    return render_template("stat.html", arr=data_to_region_stat())


@app.route("/stat_by_school")
def statistics_by_school():
    return render_template("stat_by_school.html", arr=data_to_school_stat())


@app.route("/results")
def results():
    # print(search("both", "end", "all", "all"))
    for human in search("2", "end", "all", "all"):
        print(human)
        # if len(db.get_student(human[1])) < 6:
        #     print(human, db.get_student(human[1]))
    users = [
        {   
            "place": human[4],
            "id": human[1],
            "name": ' '.join(db.get_student(human[1])[0][1:4]),
            "region": db.get_student(human[1])[0][5],
            "grade": db.get_student(human[1])[0][4],
            "school": db.get_student(human[1])[0][6],
            "scores": human[5:],
            "total": sum(human[5:]),
        }
        for human in search("both", "end", "all", "all")
    ]
    users.sort(key=lambda x: (-x["total"], x["name"]))
    return render_template(
        "results.html",
        participants=users,
    )


@app.route("/dashboard/<int:id>")
def dashboard(id):
    # user = dashboard_data(id)
    user = {
        "last_name": "Иванов",
        "first_name": "Иван",
        "middle_name": "Иванович",
        "school": "Гимназия №1",
        "region": "Санкт Петербург",
        "grade": 11,
        "score": 100,
        "place": 1,
        "avatar": None,
    }
    return render_template(
        "dashboard.html",
        user_id=id,
        user=user,
        data=[(0, 377), (1000, 6), (6123, 98), (18000, 3)],
        data2=[(0, 3), (1200, 6), (4123, 98), (18000, 3)],
        score_data=[(0, 0), (1200, 123), (2312, 200), (14780, 354), (18000, 377)],
        score_data2=[
            (0, 377),
            (1200, 123 + 377),
            (2312, 200 + 377),
            (14780, 354 + 377),
            (18000, 377 + 377),
        ],
    )


if __name__ == "__main__":
    import __init__db

    parser.populate_db()
    app.run(host="0.0.0.0", port=5000)
