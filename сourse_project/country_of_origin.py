def country_to_alpha3(country_name):
    """
    Преобразует название страны в ALPHA-3 код
    """
    country_mapping = {
        'Германия': 'DEU',
        'США': 'USA',
        'Австрия': 'AUT',
        'Республика Казахстан': 'KAZ',
        'Российская Федерация': 'RUS',
        'Корея': 'KOR',
        'Япония': 'JPN',
        'Таиланд': 'THA',
        'Китай': 'CHN',
        'UK': 'GBR',
        'Узбекистан': 'UZB',
        'Венгрия': 'HUN',
        'Турция': 'TUR',
        'Испания': 'ESP',
        'Нидерланды': 'NLD',
        'Польша': 'POL',
        'Швеция': 'SWE',
        'Белоруссия': 'BLR',
        'Бельгия': 'BEL'
    }
    return country_mapping[country_name]