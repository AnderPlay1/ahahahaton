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
    #запрос к бд
    data = db.get_all_students()# ([0.id, 1.name, 2.sur, 3.opt, 4.form, 5.reg, 6.school])
    for user in data:
        points = db.get_final_sum_for_user(user[0])#запрос к бд по сум баллам
        if user[5] not in participants:
            participants[user[5]] = 1
        else:
            participants[user[5]] += 1

        if  464 <= points < 573:
            if user[5] not in winners:
                winners[user[5]] = 1
            else:
                winners[user[5]] += 1

            if user[5] not in diplomas:
                diplomas[user[5]] = 1
            else:
                diplomas[user[5]] += 1

        if points >= 573:
            if user[5] not in prizer:
                prizer[user[5]] = 25
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
    #print(arr2)
    arr2.sort(key=lambda x: (x[1], x[0]))
    qqq = list(arr2[x][1] for x in range(len(arr2)))
    places = []
    now = 1
    for i in set(qqq):
        cnt = qqq.count(i)
        w = ""
        if cnt == 1:
            w = f'{now}'
        else:
            w = f'{now}-{now + cnt - 1}'
        for j in range(now, now + cnt):
            places.append({'place': w, 'name': arr2[j - 1][0], 'cnt': arr2[j - 1][1]})
        now += cnt
    return places

def places_for_schools(arr: dict[str, int]) -> list[dict[str, str, int]]:
    arr2 = list(arr.items())
    #print(arr2)
    arr2.sort(key=lambda x: (x[1], x[0]))
    qqq = list(arr2[x][1] for x in range(len(arr2)))
    places = []
    now = 1
    for i in set(qqq):
        cnt = qqq.count(i)
        w = ""
        if cnt == 1:
            w = f'{now}'
        else:
            w = f'{now}-{now + cnt - 1}'
        for j in range(now, now + cnt):
            places.append({'place': w,
                           'name': arr2[j - 1][0],
                           'region': 132,#запрос к бд
                            'cnt': arr2[j - 1][1]})
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

    #запрос к бд по региону Москва
    #запрос к бд по региону Питер

    data = []# ([0.id, 1.name, 2.sur, 3.opt, 4.form, 5.reg, 6.school])
    for user in data:
        points = db.get_final_sum_for_user(user[0]) #запрос к бд по сумме баллам
        if user[6] not in participants:
            participants[user[6]] = 1
        else:
            participants[user[6]] += 1

        if  464 <= points < 573:
            if user[6] not in winners:
                winners[user[6]] = 1
            else:
                winners[user[6]] += 1

            if user[6] not in diplomas:
                diplomas[user[6]] = 1
            else:
                diplomas[user[6]] += 1

        if points >= 573:
            if user[6] not in prizer:
                prizer[user[6]] = 25
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

