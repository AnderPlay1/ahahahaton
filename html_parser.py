from bs4 import BeautifulSoup
import db_functions as db
import glob
import os
import re

def parse_file(contents: str):
    html = BeautifulSoup(contents, features="html.parser")
    standings = html.select('#standings > tbody > tr')
    result = []
    for i in standings:
        try:
            rank, name, *tasks, total = i.children
        except:
            print('Something went wrong on split, the tr:')
            print(i)
        try:
            parser = r'(.*) \((.*), ([\d]+) класс\)'
            match = re.search(parser, name.get_text())
            name, region, grade = match.group(1), match.group(2), match.group(3)
        except:
            print('Matching name string failed on:')
            print(name.get_text())
        
        tasks = [i.get_text() for i in tasks]
        tasks = [int(i) if i != '.' else -1 for i in tasks]
        tasks += [0] * (8 - len(tasks))

        result.append({
            'rank': rank.get_text(),
            'name': name,
            'region': region,
            'grade': int(grade),
            'tasks': tasks,
            'total': int(total.get_text())
        })
    return result


def parse_moscow():
    contents = open('Materials/Moscow.csv', 'rb').read().decode('windows-1251')
    data = contents.split('\n')
    res = []
    for i in range(1, len(data)):
        if not data[i]:
            continue
        rank, name, grade, school, *tasks, total, result = data[i].split(';')
        res.append({
            'name': name,
            'grade': int(grade),
            'school': school,
            'result': result,
        })
    return res


def parse_spb():
    contents = open('Materials/SPB.csv', 'rb').read().decode('windows-1251')
    data = contents.split('\n')
    res = []
    for i in range(1, len(data)):
        if not data[i]:
            continue
        rank, name, *tasks, total = data[i].split(';')
        parser = r'(.*) \((.*), ([\d]+) класс\)'
        match = re.search(parser, name)
        if not match:
            print(f'Match failed on `{name}`')
        name, school, grade = match.group(1), match.group(2), match.group(3)
        res.append({
            'name': name,
            'grade': int(grade),
            'school': school
        })
    return res


def parse_the_data():
    '''
    @returns [{
      'rank': str,
      'name': str,
      'surname': str,
      'patronymic': str,
      'region': str,
      'grade': int,
      'tasks': List[int]         # -1 - no attempts, other - score
      'total': int,
      'school': Optional[string]
      'round': int,
      'result': Optional[string] # участник/призер/победитель,
      'time': int,               # 120/150/...
    }]
    '''
    moscow_data = parse_moscow()
    spb_data = parse_spb()
    files = glob.glob('Materials/*/*.html')
    res = []
    for f in files:
        print(f'Parsing {f}')
        time = f.split('/')[-1].removesuffix('.html')
        if 'First' in f:
            round = 1
        else:
            round = 2

        contents = open(f, 'r').read()
        parsed = parse_file(contents)
        for i in parsed:
            i['school'] = None
            i['result'] = None
            for m in moscow_data:
                if (m['name'].lower() in i['name'].lower() 
                    and m['grade'] == i['grade']):
                    i['school'] = m['school']
                    i['result'] = m['result']
            for s in spb_data:
                if (s['name'].lower() in i['name'].lower()
                    and s['grade'] == i['grade']):
                    i['school'] = s['school']
                
            i['round'] = round
            i['time'] = int(time)
            
            name_parts = i['name'].split(' ')
            name_parts += [''] * (3 - len(name_parts))
            i['name'] = name_parts[1].strip()
            i['surname'] = name_parts[0].strip()
            i['patronymic'] = name_parts[2].strip()

            res.append(i)
    return res


def populate_db():
    results = parse_the_data()
    db.add_results(results)


