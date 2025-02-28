


def data_to_region_stat():
    response = dict()
    participants = dict()
    winners = dict()
    prizer = dict()
    diplomas = dict()

    #запрос к бд
    data = []# ([0.id, 1.name, 2.sur, 3.opt, 4.reg, 5.school])
    for user in data:
        points = 0#запрос к бд по сум баллам
        if user[4] not in participants:
            participants[user[4]] = 1
        else:
            participants[user[4]] += 1

        if points >= win_points:
            if user[4] not in winners:
                winners[user[4]] = 1
            else:
                winners[user[4]] += 1

            if user[4] not in diplomas:
                diplomas[user[4]] = 1
            else:
                diplomas[user[4]] += 1

        if points >= prizer_points:
            if user[4] not in prizer:
                prizer[user[4]] = 1
            else:
                prizer[user[4]] += 1

            if user[4] not in diplomas:
                diplomas[user[4]] = 1
            else:
                diplomas[user[4]] += 1

    response["participants"] = participants
    response["winners"] = winners
    response["prizer"] = prizer
    response["diplomas"] = diplomas


def places(arr: list[dict[str, int]]) -> list[dict[str, str, int]]:
    arr2 = [(arr[x]['name'], arr[x]['cnt']) for x in range(len(arr))]
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
