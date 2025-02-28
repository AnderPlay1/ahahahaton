from db_functions import get_school_for_user, get_region_for_school

name,surname,patronymic = input().split()
school = get_school_for_user(name,surname,patronymic)
region = get_region_for_school(school)
print(school, region)