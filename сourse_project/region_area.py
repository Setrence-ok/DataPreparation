import numpy as np


def correct_area(row):
    region = row['area']

    # Если область указана как город
    if region == 'г.Алматы':
        return 'Алматинская область'
    elif region == 'г.Нур-Султан':
        return 'Акмолинская область'
    elif region == 'Экспорт область':
        return np.nan
    else:
        return region

def correct_region(row):
    region = row['region']

    # Если область указана как город
    if region == 'Экспорт':
        return np.nan
    else:
        return region