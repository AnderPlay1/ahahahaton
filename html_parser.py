from bs4 import BeautifulSoup
import os
import re


def parse_file(contents: str):
    html = BeautifulSoup(contents)
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
            'grade': grade,
            'tasks': tasks,
            'total': int(total.get_text())
        })
    return result
