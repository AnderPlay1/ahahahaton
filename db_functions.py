import sqlite3

connect = sqlite3.connect("Database.db")
cursor = connect.cursor()

def add_user(data):
    """
    :param data: Dict{name:str, surname:str, patronymic:str, grade:int, region:str, school:str}
    :return: -
    """
    params = [data['name'], data['surname'], data['patronymic'], data['grade'], data['region'], data['school']]
    cursor.execute("INSERT INTO Users (name, surname, patronymic, form, region, school) VALUES (?, ?, ?, ?, ?, ?)", params)
    connect.commit()

def add_results(data):
    """
    :param data: List[Dict{name:str, surname:str, patronymic:str, grade:int, region:str, school:str, rank:str, tasks:List[int], round:int, time:str}]
    :return: -
    """
    for item in data:
        params = [item['name'], item['surname'], item['patronymic'], item["grade"], item['region'], item['school']]
        id_user = cursor.execute("SELECT ID FROM Users WHERE name = ? AND surname = ? AND patronymic = ? AND form = ? AND region = ? AND school = ?", params).fetchall()
        if len(id_user) == 0:
            add_user(item)
            id_user = cursor.execute(
                "SELECT ID FROM Users WHERE name = ? AND surname = ? AND patronymic = ? AND form = ? AND region = ? AND school = ?", params).fetchall()
        id_user = id_user[0][0]
        params = [id_user, item["time"], item["round"], item["rank"]]
        params += item["tasks"]
        cursor.execute("INSERT INTO Scores (ID_user, time, tour, rank, task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
    connect.commit()

def get_final_sum_for_user(id_user):
    """
    :param id_user: int
    :return: result:int
    """
    result = cursor.execute("SELECT sum(task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8) FROM Scores WHERE ID_user = ? ORDER BY time LIMIT 1", [id_user]).fetchall()
    if len(result) == 0:
        result = 0
    else:
        result = sum(result[0])
    return result

def get_all_students():
    """
    :return: List[Tuple(ID:int, name:str, surname:str, patronymic:str, form:int, region:str, school:str)]
    """
    result = cursor.execute("SELECT * FROM Users").fetchall()
    return result

def get_results_for_time(time, tour):
    """
    :param time: str
    :param tour: Tuple(int)
    :return: List[Tuple(rank:str, form:int, name:str, surname:str, patronymic:str, region:str, school:str, task_1:int, task_2:int, ... , task_8:int)]
    """
    result = cursor.execute("SELECT rank, form, name, surname, patronymic, region, school, task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8 FROM Scores JOIN Users ON Scores.ID_user = Users.ID WHERE time = ? AND tour IN ? ORDER BY rank", [time, tour]).fetchall()
    return result

def get_results_for_user(id_user):
    """
    :param id_user: int
    :return: List[Tuple(ID:int, ID_user:int, time:str, tour:int, rank:str, task_1:int, task_2:int, ... , task_8:int)]
    """
    result = cursor.execute("SELECT * FROM Scores WHERE ID_User = ? ORDER BY tour, time DESC", [id_user]).fetchall()
    return result

def get_region_for_school(school):
    """
    :param school: str
    :return: region: str
    """
    result = cursor.execute("SELECT region FROM Users WHERE school = ? LIMIT 1", [school]).fetchall()[0][0]
    return result

def get_students_for_region(region):
    """
    :param region: str
    :return: List[Tuple(ID:int, name:str, surname:str, patronymic:str, form:int, region:str, school:str)]
    """
    result = cursor.execute("SELECT * FROM Users WHERE region = ?", [region]).fetchall()
    return result

def get_students_for_school(school):
    """
    :param school: str
    :return: List[Tuple(ID:int, name:str, surname:str, patronymic:str, form:int, region:str, school:str)]
    """
    result = cursor.execute("SELECT * FROM Users WHERE school = ?", [school]).fetchall()
    return result

def get_student(id_user):
    """
    :param id_user: int
    :return: List[Tuple(ID:int, name:str, surname:str, patronymic:str, form:int, region:str, school:str)]
    """
    result = cursor.execute("SELECT * FROM Users WHERE ID = ?", [id_user]).fetchall()
    return result

def get_final_results_for_user(id_user):
    """
    :param id_user: int
    :return: List[Tuple(ID_user:int, task_1:int, task_2:int, ... , task_8:int)]
    """
    result = cursor.execute("SELECT ID_user, task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8 FROM Scores WHERE ID_user = ? ORDER BY tour, tyme DESC LIMIT 1", [id_user]).fetchall()
    return result

def get_rank_for_user(id_user, tour):
    """
    :param id_user: int
    :param tour: int
    :return: rank: str
    """
    result = cursor.execute("SELECT rank FROM Scores WHERE id_user = ? AND tour = ? ORDER BY time DESC LIMIT 1", [id_user, tour]).fetchall()[0][0]
    return result

def get_school_for_user(name, surname, patronymic):
    """
    :param name: str
    :param surname: str
    :param patronymic: str
    :return: school: str or None
    """
    result = cursor.execute("SELECT school FROM Users WHERE name = ? AND surname = ? AND patronymic = ?", [name, surname, patronymic]).fetchall()
    return result

def get_final_result_for_student(id_user, tour):
    """
    :param id_user: int
    :param tour: int
    :return: Tuple(task_1:int, task_2:int, ... , task_8:int)
    """
    result = cursor.execute("SELECT task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8 FROM Scores WHERE id_user = ? AND tour = ? ORDER BY time DESC LIMIT 1",[id_user, tour]).fetchall()[0]
    return result