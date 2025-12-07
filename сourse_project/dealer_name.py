import pandas as pd
import numpy as np
from datetime import datetime
import pycountry



def analyze_company_names(df):
    """
    Анализирует названия компаний перед очисткой
    """
    print("АНАЛИЗ ИСХОДНЫХ ДАННЫХ:")

    if 'dealer_name' in df.columns:
        unique_names = df['dealer_name'].nunique()
        total_rows = len(df)
        print(f"Всего уникальных названий: {unique_names}")
        print(f"Всего записей: {total_rows}")
        print(f"Топ-20 самых частых названий:")
        print(df['dealer_name'].value_counts().head(20))

    else:
        print("❌ Столбец dealer_name не найден")
        print(f"Доступные столбцы: {list(df.columns)}")


def create_company_mapping():
    """
    Создает mapping для приведения названий к единому формату
    """
    company_mapping = {
        # Меркур Авто - различные варианты написания
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
        'hino motors ': 'Hino Motors Kazakhstan',  # с пробелом в конце

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
        print("❌ Столбец dealer_name не найден")
        return df

    # Сохраняем оригинальные названия для анализа
    df['dealer_name_original'] = df['dealer_name']

    # Применяем стандартизацию
    df['dealer_name_cleaned'] = df['dealer_name'].apply(standardize_company_name)

    # Анализируем результаты
    original_count = df['dealer_name_original'].nunique()
    cleaned_count = df['dealer_name_cleaned'].nunique()
    reduction = original_count - cleaned_count

    print(f"РЕЗУЛЬТАТЫ СТАНДАРТИЗАЦИИ:")
    print(f"Было уникальных названий: {original_count}")
    print(f"Стало уникальных названий: {cleaned_count}")
    print(f"Удалено дубликатов: {reduction}")

    return df


def analyze_changes(df):
    """
    Анализирует какие изменения были сделаны
    """
    print("\nАНАЛИЗ ИЗМЕНЕНИЙ:")

    # Находим строки где названия изменились
    changed_names = df[df['dealer_name_original'] != df['dealer_name_cleaned']]

    if not changed_names.empty:
        print(f"Изменено названий: {len(changed_names)}")
        print("\nТоп-10 самых частых изменений:")
        changes = changed_names.groupby(['dealer_name_original', 'dealer_name_cleaned']).size().reset_index(
            name='count')
        changes = changes.sort_values('count', ascending=False).head(10)
        print(changes)
    else:
        print("Изменений не обнаружено")


def analyze_mercur_auto(df):
    """
    Специальный анализ для Меркур Авто
    """
    print("\nАНАЛИЗ МЕРКУР АВТО:")

    # Все варианты Меркур Авто
    mercur_variants = df[df['dealer_name_cleaned'] == 'Mercur Auto']
    original_variants = mercur_variants['dealer_name_original'].unique()

    print(f"Все варианты Меркур Авто:")
    for variant in original_variants:
        count = len(mercur_variants[mercur_variants['dealer_name_original'] == variant])
        print(f"  '{variant}': {count} записей")

    total_mercur = len(mercur_variants)
    print(f"Всего записей Меркур Авто после очистки: {total_mercur}")


def final_company_cleaning(df):
    """
    Финальные преобразования для столбца компаний
    """
    print("\nФИНАЛЬНЫЕ ПРЕОБРАЗОВАНИЯ:")

    # Заменяем оригинальный столбец очищенным
    df['dealer_name'] = df['dealer_name_cleaned']

    # Удаляем временные столбцы
    df = df.drop(columns=['dealer_name_cleaned', 'dealer_name_original'])

    print("Очищенные названия компаний:")
    print(df['dealer_name'].value_counts().head(15))

    return df


def final_company_check(df):
    """
    Финальная проверка очистки компаний
    """
    print("\nФИНАЛЬНАЯ ПРОВЕРКА:")

    if 'dealer_name' in df.columns:
        print("✅ Столбец dealer_name очищен успешно")
        print(f"Уникальных названий: {df['dealer_name'].nunique()}")
        print(f"Топ-10 дилерских центров:")
        print(df['dealer_name'].value_counts().head(10))

        # Проверяем что Меркур Авто объединен
        mercur_count = (df['dealer_name'] == 'Mercur Auto').sum()
        print(f"\nЗаписей Меркур Авто: {mercur_count}")

    else:
        print("❌ Столбец dealer_name не найден")