import pandas as pd
import numpy as np
import re

def analyze_engine_volume(df):
    """
    Анализирует проблемы в данных объема двигателя
    """
    print("АНАЛИЗ ИСХОДНЫХ ДАННЫХ:")

    if 'engine_volume' in df.columns:
        total_values = len(df)
        missing_values = df['engine_volume'].isnull().sum()
        unique_values = df['engine_volume'].nunique()

        print(f"Всего значений: {total_values}")
        print(f"Пропуски: {missing_values}")
        print(f"Уникальных значений: {unique_values}")

        # Анализ проблемных значений
        sample_problems = []
        for val in df['engine_volume'].unique()[:50]:  # первые 50 уникальных значений
            if pd.isna(val):
                continue
            val_str = str(val)
            # Ищем проблемные значения
            if any(problem in val_str.lower() for problem in
                   ['л.с.', 'кип', 'mt', 'at', 'turbo', 'gdi', 'mpi', 'crdi', 't-gdi']):
                sample_problems.append(val_str)
            elif any(char in val_str for char in [',', '.', 'l', 'L']):
                try:
                    # Пробуем преобразовать в число
                    test_val = float(val_str.replace(',', '.').replace('L', '').replace('l', ''))
                    if test_val > 50:  # Подозрительно большие значения
                        sample_problems.append(f"{val_str} -> {test_val}")
                except:
                    sample_problems.append(val_str)

        print(f"\nПримеры проблемных значений ({len(sample_problems)}):")
        for problem in sample_problems[:20]:
            print(f"  - {problem}")

    else:
        print("Столбец engine_volume не найден")


def clean_engine_volume(value, brand=None, model=None):
    """
    Очищает, исправляет и округляет объем двигателя до 1 знака после запятой
    """
    if pd.isna(value):
        return np.nan

    original_value = str(value).strip()

    # 1. Заменяем запятые на точки
    cleaned = original_value.replace(',', '.')

    # 2. Убираем литеру L и пробелы
    cleaned = cleaned.replace('L', '').replace('l', '').replace(' ', '')

    # 3. Обработка мусорных значений
    lower_cleaned = cleaned.lower()

    # Мусорные значения - возвращаем NaN
    garbage_values = ['mt', 'at', 'н/д', '#h/д', '#н/д', 'кип', 'л.с.', 'квт']
    if any(garbage in lower_cleaned for garbage in garbage_values):
        return np.nan

    # 4. Извлекаем числовую часть (первое число)
    numbers = re.findall(r'\d+\.?\d*', cleaned)
    if not numbers:
        return np.nan

    try:
        numeric_value = float(numbers[0])

        # 5. Исправление очевидных ошибок

        # Случай 1: Если значение > 50 - скорее всего перепутаны объем и мощность
        if numeric_value > 50:
            # Делим на 10 для получения разумного объема
            corrected = numeric_value / 10
            # Проверяем что получилось разумное значение (0.5 - 8.0 литров)
            if 0.5 <= corrected <= 8.0:
                return round(corrected, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ
            else:
                return np.nan

        # Случай 2: Особые случаи для конкретных моделей
        if brand and model:
            brand_lower = str(brand).lower()
            model_lower = str(model).lower()

            # Chevrolet Niva - известная проблема с аномальными значениями
            if 'chevrolet' in brand_lower and 'niva' in model_lower:
                if numeric_value > 10:  # Исправляем 21.6, 20.6 и т.д.
                    return round(numeric_value / 10, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ

            # Jaguar - перепутаны объем и мощность
            if 'jaguar' in brand_lower and numeric_value > 10:
                return round(numeric_value / 10, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ

        # 6. Проверка на разумный диапазон (0.5 - 8.0 литров для легковых авто)
        if 0.5 <= numeric_value <= 8.0:
            return round(numeric_value, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ
        else:
            return np.nan

    except (ValueError, TypeError):
        return np.nan


def apply_engine_cleaning(df):
    """
    Применяет очистку объема двигателя
    """
    print("ПРИМЕНЕНИЕ ОЧИСТКИ...")

    # Сохраняем оригинальные значения для анализа
    df['engine_volume_original'] = df['engine_volume']

    # Применяем очистку с учетом бренда и модели для особых случаев
    df['engine_volume_cleaned'] = df.apply(
        lambda row: clean_engine_volume(row['engine_volume'], row.get('brand'), row.get('model')),
        axis=1
    )

    # Анализ результатов
    original_non_null = df['engine_volume_original'].notna().sum()
    cleaned_non_null = df['engine_volume_cleaned'].notna().sum()
    cleaned_count = original_non_null - cleaned_non_null

    print(f"РЕЗУЛЬТАТЫ ОЧИСТКИ:")
    print(f"Было непустых значений: {original_non_null}")
    print(f"Стало непустых значений: {cleaned_non_null}")
    print(f"Потеряно значений при очистке: {cleaned_count}")
    print(f"Процент сохраненных: {cleaned_non_null / original_non_null * 100:.1f}%")

    return df


def analyze_cleaning_changes(df):
    """
    Анализирует какие изменения были сделаны
    """
    print("\nАНАЛИЗ ИЗМЕНЕНИЙ:")

    # Примеры исправленных значений
    changed_values = df[df['engine_volume_cleaned'].notna()].head(20)

    print("Примеры исправленных значений:")
    for idx, row in changed_values.iterrows():
        original = row['engine_volume_original']
        cleaned = row['engine_volume_cleaned']
        if original != str(cleaned):
            print(f"  '{original}' -> {cleaned:.1f}")

    # Статистика по очищенным значениям
    print(f"\nСТАТИСТИКА ОЧИЩЕННЫХ ЗНАЧЕНИЙ:")
    if df['engine_volume_cleaned'].notna().sum() > 0:
        cleaned_volumes = df['engine_volume_cleaned'].dropna()
        print(f"Мин: {cleaned_volumes.min():.1f}")
        print(f"Макс: {cleaned_volumes.max():.1f}")
        print(f"Медиана: {cleaned_volumes.median():.1f}")
        print(f"Среднее: {cleaned_volumes.mean():.1f}")

        # Распределение по диапазонам
        print(f"\nРАСПРЕДЕЛЕНИЕ:")
        bins = [0, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0]
        distribution = pd.cut(cleaned_volumes, bins=bins).value_counts().sort_index()
        print(distribution)


def analyze_special_cases(df):
    """
    Анализ особых случаев упомянутых в задании
    """
    print("\nОСОБЫЕ СЛУЧАИ:")

    # 1. Jaguar с объемом 400
    jaguar_cases = df[(df['brand'] == 'Jaguar') & (df['engine_volume_original'].notna())]
    if not jaguar_cases.empty:
        print("JAGUAR - исправление перепутанных объема и мощности:")
        for idx, row in jaguar_cases.iterrows():
            print(f"  {row['model']}: '{row['engine_volume_original']}' -> {row['engine_volume_cleaned']:.1f}")

    # 2. Chevrolet Niva
    niva_cases = df[(df['brand'] == 'Chevrolet') & (df['model'] == 'Niva') & (df['engine_volume_original'].notna())]
    if not niva_cases.empty:
        print("\nCHEVROLET NIVA - исправление аномалий:")
        for idx, row in niva_cases.iterrows():
            print(f"  '{row['engine_volume_original']}' -> {row['engine_volume_cleaned']:.1f}")

    # 3. Другие проблемные бренды
    problem_brands = df[
        (df['engine_volume_original'].notna()) &
        (df['engine_volume_cleaned'].isna())
        ]['brand'].value_counts().head(5)

    if not problem_brands.empty:
        print(f"\nБренды с наибольшим количеством потерянных значений:")
        print(problem_brands)


def final_engine_cleaning(df):
    """
    Финальные преобразования для объема двигателя с округлением
    """
    print("\nФИНАЛЬНЫЕ ПРЕОБРАЗОВАНИЯ:")

    # Заменяем оригинальный столбец очищенным
    df['engine_volume'] = df['engine_volume_cleaned']

    # Удаляем временные столбцы
    df = df.drop(columns=['engine_volume_cleaned', 'engine_volume_original'])

    # Дополнительное округление на всякий случай (если какие-то значения прошли мимо)
    df['engine_volume'] = df['engine_volume'].round(1)

    # Заполняем пропуски медианой по бренду (тоже с округлением)
    if 'brand' in df.columns:
        brand_medians = df.groupby('brand')['engine_volume'].median().round(1)

        def fill_with_brand_median(row):
            if pd.isna(row['engine_volume']) and row['brand'] in brand_medians:
                return brand_medians[row['brand']]
            return row['engine_volume']

        df['engine_volume'] = df.apply(fill_with_brand_median, axis=1)

    print(f"Финальная статистика объема двигателя (округлено до 0.1):")
    print(f"Пропуски: {df['engine_volume'].isnull().sum()}")
    print(f"Мин: {df['engine_volume'].min():.1f}")
    print(f"Макс: {df['engine_volume'].max():.1f}")
    print(f"Медиана: {df['engine_volume'].median():.1f}")

    # Проверяем что все значения округлены правильно
    unique_decimals = set()
    for val in df['engine_volume'].dropna():
        decimal_part = val - int(val) if val != 0 else 0
        if decimal_part > 0:
            unique_decimals.add(round(decimal_part, 2))

    print(f"Уникальные десятичные части: {sorted(unique_decimals)}")

    return df