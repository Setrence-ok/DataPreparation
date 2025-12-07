import pandas as pd

def create_company_mapping():
    """
    Создает mapping для приведения названий к единому формату
    """
    company_mapping = {
        # Меркур Авто
        'mercur auto': 'Mercur Auto',
        'mercur autos': 'Mercur Auto',
        'меркур авто': 'Mercur Auto',

        # Astana Motors
        'astana motors': 'Astana Motors',

        # Каспиан Моторс / Caspian Motors
        'каспиан моторс': 'Caspian Motors',
        'сaspian motors': 'Caspian Motors',
        'caspian motors': 'Caspian Motors',

        # ММС Rus
        'ммс рус': 'MMC Rus',
        'ммс rus': 'MMC Rus',
        'мmc rus': 'MMC Rus',

        # Ravon Motors
        'равон моторс казахстан': 'Ravon Motors Kazakhstan',
        'ravon motors kazakhstan': 'Ravon Motors Kazakhstan',

        # Автокплитал / Autokapital
        'autokapital': 'Autokapital',
        'автокплитал': 'Autokapital',

        # Hino Motors
        'хино моторс казахстан': 'Hino Motors Kazakhstan',
        'hino motors': 'Hino Motors Kazakhstan',
        'hino motors ': 'Hino Motors Kazakhstan',

        # Hyundai
        'hyundai com trans kazakhstan': 'Hyundai Com Trans Kazakhstan',

        # Другие очевидные дубликаты
        'nissan manufacturing rus': 'Nissan Manufacturing RUS',
        'toyota motor kazakhstan': 'Toyota Motor Kazakhstan',
        'volkswagen group rus': 'Volkswagen Group Rus',
        'subaru kazakhstan': 'Subaru Kazakhstan',
        'scania central asia': 'Scania Central Asia',
        'renault россия': 'Renault Россия',
        'allur auto': 'Allur Auto',
        'terra motors': 'TERRA MOTORS',
        'tk kama3': 'TK KAMA3',
        'man truck & bus kazakhstan': 'MAN Truck & Bus Kazakhstan'
    }
    return company_mapping


def standardize_company_name(name):
    """
    Приводит название компании к единому формату
    """
    if pd.isna(name):
        return name
    original_name = str(name).strip()
    name_lower = original_name.lower().strip()
    company_mapping = create_company_mapping()
    # Проверяем есть ли точное соответствие в mapping
    if name_lower in company_mapping:
        return company_mapping[name_lower]
    # Проверяем частичные совпадения
    for key, value in company_mapping.items():
        if key in name_lower:
            return value
    # Если не нашли в mapping, возвращаем оригинал с нормальным регистром
    return original_name


def clean_company_names(df):
    """
    Очищает и стандартизирует названия компаний
    """
    if 'dealer_name' not in df.columns:
        return df
    # Сохраняем оригинальные названия для анализа
    df['dealer_name_original'] = df['dealer_name']
    # Применяем стандартизацию
    df['dealer_name_cleaned'] = df['dealer_name'].apply(standardize_company_name)

    return df


def final_company_cleaning(df):
    """
    Финальные преобразования для столбца компаний
    """
    # Заменяем оригинальный столбец очищенным
    df['dealer_name'] = df['dealer_name_cleaned']
    # Удаляем временные столбцы
    df = df.drop(columns=['dealer_name_cleaned', 'dealer_name_original'])
    return df