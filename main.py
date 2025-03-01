from flask import Flask, render_template, session, request, redirect, url_for, flash
import os

if os.path.exists("Database.db"):
    print("\u001b[35;1m Killed all goidas \u001b[0m")
    os.remove("Database.db")
from backend import (
    data_to_region_stat,
    data_to_school_stat,
    dashboard_data,
    type_of_participant,
)
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
    tour = request.args.get("tour", "both")
    grade = request.args.get("grade", "all")
    time = request.args.get("time", "end")
    school = request.args.get("school", "all")
    rich = request.args.get("rich", "1")
    # print(tour)
    users = [
        {
            "place": human[4],
            "id": human[1],
            "name": " ".join(db.get_student(human[1])[0][1:4]),
            "region": db.get_student(human[1])[0][5],
            "grade": db.get_student(human[1])[0][4],
            "school": db.get_student(human[1])[0][6],
            "scores": human[5:],
            "total": sum(
                max(human[i], 0)
                for i in range(5, 13)
                if (tour == "both")
                or (tour == "2" and i > 8)
                or (tour == "1" and i < 9)
            ),
        }
        for human in search(tour, time, grade, school)
    ]
    users.sort(key=lambda x: (-x["total"], x["name"]))
    users = type_of_participant(users)
    if tour == "both" and int(rich) == 1:
        users = type_of_participant(users)
    else:
        if tour == '2':
            for i in range(len(users)):
                users[i]['place'] = str(i)
        for x in users:
            x["type"] = "Участник"
    return render_template(
        "results.html",
        participants=users,
    )


@app.route("/dashboard/<int:id>")
def dashboard(id):
    user = dashboard_data(id)
    first_places = [(x * 60, y) for x, y in db.get_rank_for_user_time(id, 1)]
    first_scores = [(x * 60, y) for x, y in db.get_scores_for_user_time(id, 1)]
    w = (0, int(first_places[-1][-1].split("-")[0]))
    ww = (0, first_scores[-1][-1])
    return render_template(
        "dashboard.html",
        user_id=id,
        user=user,
        score_data=[(0, 0)]
        + [(x * 60, y) for x, y in db.get_scores_for_user_time(id, 1)],
        score_data2=[ww] + [(x * 60, y) for x, y in db.get_scores_for_user_time(id, 2)],
        data=[
            (x * 60, int(y.split("-")[0])) for x, y in db.get_rank_for_user_time(id, 1)
        ],
        data2=[w]
        + [(x * 60, int(y.split("-")[0])) for x, y in db.get_rank_for_user_time(id, 2)],
    )


if __name__ == "__main__":

    import __init__db

    parser.populate_db()
    app.run(host="0.0.0.0", port=5000)
