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
if __name__ == "__main__":
    print(places([{'name': 'a', 'cnt': 1}, {'name': 'b', 'cnt': 2}, {'name': 'c', 'cnt': 1}, {'name': 'd', 'cnt': 1}, {'name': 'e', 'cnt': 2}, {'name': 'f', 'cnt': 1}]))