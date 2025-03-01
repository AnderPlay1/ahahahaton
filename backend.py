import db_functions as db


def data_to_region_stat():
    """
    :return: Dict(Dict[str:int], Dict[str:int], Dict[str:int], Dict[str:int], Dict[str:int])
    """
    response = dict()
    participants = dict()
    winners = dict()
    prizer = dict()
    diplomas = dict()
    # запрос к бд
    data = db.get_all_students()
    # ([0.id, 1.name, 2.sur, 3.opt, 4.form, 5.reg, 6.school])
    for user in data:

        points = db.get_final_sum_for_user(user[0])  # запрос к бд по сум баллам
        print(user, points)
        if user[5] not in participants:
            participants[user[5]] = 1
        else:
            participants[user[5]] += 1

        if points >= 573:
            if user[5] not in winners:
                winners[user[5]] = 1
            else:
                winners[user[5]] += 1
            print(user[5])
            if user[5] not in diplomas:
                diplomas[user[5]] = 1
            else:
                diplomas[user[5]] += 1

        if 464 <= points < 573:
            if user[5] not in prizer:
                prizer[user[5]] = 1
            else:
                prizer[user[5]] += 1

            if user[5] not in diplomas:
                diplomas[user[5]] = 1
            else:
                diplomas[user[5]] += 1

    response["participants"] = places(participants)
    response["winners"] = places(winners)
    response["prizer"] = places(prizer)
    response["diplomas"] = places(diplomas)
    return response


def places(arr: dict[str, int]) -> list[dict[str, str, int]]:
    arr2 = list(arr.items())
    # print(arr2)
    arr2.sort(key=lambda x: (x[1], x[0]), reverse=True)
    qqq = list(arr2[x][1] for x in range(len(arr2)))
    places = []
    now = 1
    print(sorted(list(set(qqq))))
    for i in sorted(list(set(qqq)), reverse=True):
        cnt = qqq.count(i)
        w = ""
        if cnt == 1:
            w = f"{now}"
        else:
            w = f"{now}-{now + cnt - 1}"
        for j in range(now, now + cnt):
            places.append({"place": w, "name": arr2[j - 1][0], "cnt": arr2[j - 1][1]})
        now += cnt
    return places


def places_for_schools(arr: dict[str, int]) -> list[dict[str, str, int]]:
    arr2 = list(arr.items())
    # print(arr2)
    arr2.sort(key=lambda x: (x[1], x[0]), reverse=True)
    qqq = list(arr2[x][1] for x in range(len(arr2)))
    places = []
    now = 1
    print(sorted(list(set(qqq))))
    for i in sorted(list(set(qqq)), reverse=True):
        cnt = qqq.count(i)
        w = ""
        if cnt == 1:
            w = f"{now}"
        else:
            w = f"{now}-{now + cnt - 1}"
        for j in range(now, now + cnt):
            places.append({"place": w, "name": arr2[j - 1][0], "region": db.get_region_for_school(arr2[j - 1][0]), "cnt": arr2[j - 1][1]})
        now += cnt
    return places


def data_to_school_stat():
    """
    :return: Dict(Dict[str:int], Dict[str:int], Dict[str:int], Dict[str:int], Dict[str:int])
    """
    response = dict()
    participants = dict()
    winners = dict()
    prizer = dict()
    diplomas = dict()

    # запрос к бд по региону Москва
    # запрос к бд по региону Питер
    data = []  # ([0.id, 1.name, 2.sur, 3.opt, 4.form, 5.reg, 6.school])
    data1 = db.get_student_for_region("Москва")
    data2 = db.get_student_for_region("Санкт-Петербург")

    for user in data1:
        points = db.get_final_sum_for_user(user[0])
        # запрос к бд по сумме баллам
        if user[6] == None:
            continue
        if user[6] not in participants:
            participants[user[6]] = 1
        else:
            participants[user[6]] += 1

        if points >= 573:
            if user[6] not in winners:
                winners[user[6]] = 1
            else:
                winners[user[6]] += 1

            if user[6] not in diplomas:
                diplomas[user[6]] = 1
            else:
                diplomas[user[6]] += 1

        if 464 <= points < 573:
            if user[6] not in prizer:
                prizer[user[6]] = 1
            else:
                prizer[user[6]] += 1

            if user[6] not in diplomas:
                diplomas[user[6]] = 1
            else:
                diplomas[user[6]] += 1

    for user in data2:
        points = db.get_final_sum_for_user(user[0])  # запрос к бд по сумме баллам
        if user[6] == None:
            continue
        if user[6] not in participants:
            participants[user[6]] = 1
        else:
            participants[user[6]] += 1

        if points >= 573:
            if user[6] not in winners:
                winners[user[6]] = 1
            else:
                winners[user[6]] += 1

            if user[6] not in diplomas:
                diplomas[user[6]] = 1
            else:
                diplomas[user[6]] += 1

        if 464 <= points < 573:
            if user[6] not in prizer:
                prizer[user[6]] = 1
            else:
                prizer[user[6]] += 1

            if user[6] not in diplomas:
                diplomas[user[6]] = 1
            else:
                diplomas[user[6]] += 1

    response["participants"] = places_for_schools(participants)
    response["winners"] = places_for_schools(winners)
    response["prizer"] = places_for_schools(prizer)
    response["diplomas"] = places_for_schools(diplomas)
    return response


def results():
    """
    :return:
    """


def dashboard_data(id):
    """
    :param id:int
    :return: Dict('first_name': string
        'last_name': string
        "middle_name": string,
        "school": string,
        "region": string,
        "class": int,
        "score1": int,
        "score2": int,
        "score_sum": int,
        "place1": string,
        "place2": string,
        "results": list,
        "avatar": None)
    """
    data = db.get_student(id)
    # ([0.id, 1.name, 2.sur, 3.opt, 4.form, 5.reg, 6.school])
    score1 = sum(db.get_final_result_for_student(data[0][0], 1))
    score2 = sum(db.get_final_result_for_student(data[0][0], 2)) - score1

    return {
        "first_name": data[0][1],
        "last_name": data[0][2],
        "middle_name": data[0][3],
        "school": data[0][6],
        "region": data[0][5],
        "class": data[0][4],
        "score1": score1,
        "score2": score2,
        "score_sum": db.get_final_sum_for_user(data[0][0]),
        "place1": db.get_rank_for_user(data[0][0], 1),
        "place2": db.get_rank_for_user(data[0][0], 2),
        "results": db.get_final_result_for_student(data[0][0], 2),
        "avatar": None,
    }

def type_of_participant(arr: list[dict[str,int,str,str,int,None|str,list[int],int]]):
    """
    :param arr: List[Dict[str, int, str, str, str, int, List[int], int]]
    :return: List[Dict[str, int, str, str, str, int, List[int], int, str]]
    """
    total_participants = 377
    
    # Sort by total score in descending order
    sorted_arr = sorted(arr, key=lambda x: x["total"], reverse=True)
    
    # Group participants by place
    place_groups = {}
    for participant in sorted_arr:
        if "-" in participant["place"]:
            start, end = map(int, participant["place"].split("-"))
            place_key = f"{start}-{end}"
        else:
            place_key = participant["place"]
        
        if place_key not in place_groups:
            place_groups[place_key] = []
        place_groups[place_key].append(participant)
    
    # Assign types based on place groups
    winners_cutoff = int(total_participants * 0.08)
    prizers_cutoff = int(total_participants * 0.46)
    
    
    # print(participants_processed, prizers_cutoff, winners_cutoff)
    for place_key in sorted(place_groups.keys(), key=lambda x: int(x.split("-")[-1])):
        participants_processed = int(place_key.split('-')[0]) - 1
        group = place_groups[place_key]
        
        if participants_processed + len(group) <= winners_cutoff and all(p["total"] >= 400 for p in group):
            type_to_assign = "Победитель"
        elif participants_processed + len(group)<= prizers_cutoff and all(p["total"] >= 400 for p in group):
            type_to_assign = "Призер"
        else:
            type_to_assign = "Участник"
        
        # Assign same type to all participants in the group
        for participant in group:
            participant["type"] = type_to_assign
    print(arr)
    return arr