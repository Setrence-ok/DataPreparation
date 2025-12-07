import pandas as pd
import numpy as np
import re

def clean_engine_volume(value, brand=None, model=None):
    """
    Очищает, исправляет и округляет объем двигателя до 1 знака после запятой
    """
    if pd.isna(value):
        return np.nan
    original_value = str(value).strip()
    # Заменяем запятые на точки
    cleaned = original_value.replace(',', '.')
    # Убираем литеру L и пробелы
    cleaned = cleaned.replace('L', '').replace('l', '').replace(' ', '')
    # Обработка мусорных значений
    lower_cleaned = cleaned.lower()
    # Мусорные значения
    garbage_values = ['mt', 'at', 'н/д', '#h/д', '#н/д', 'кип', 'л.с.', 'квт']
    if any(garbage in lower_cleaned for garbage in garbage_values):
        return np.nan
    # Извлекаем числовую часть
    numbers = re.findall(r'\d+\.?\d*', cleaned)
    if not numbers:
        return np.nan
    try:
        numeric_value = float(numbers[0])
        # Если значение > 50 - скорее всего перепутаны объем и мощность
        if numeric_value > 50:
            # Делим на 10 для получения разумного объема
            corrected = numeric_value / 10
            # Проверяем что получилось разумное значение (0.5 - 8.0 литров)
            if 0.5 <= corrected <= 8.0:
                return round(corrected, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ
            else:
                return np.nan
        # Особые случаи для конкретных моделей
        if brand and model:
            brand_lower = str(brand).lower()
            model_lower = str(model).lower()
            if 'chevrolet' in brand_lower and 'niva' in model_lower:
                if numeric_value > 10:  # Исправляем 21.6, 20.6 и т.д.
                    return round(numeric_value / 10, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ
            if 'jaguar' in brand_lower and numeric_value > 10:
                return round(numeric_value / 10, 1)  # ОКРУГЛЕНИЕ ДОБАВЛЕНО ЗДЕСЬ

        # Проверка на разумный диапазон (0.5 - 8.0 литров для легковых авто)
        if 0.5 <= numeric_value <= 8.0:
            return round(numeric_value, 1)
        else:
            return np.nan

    except (ValueError, TypeError):
        return np.nan


def apply_engine_cleaning(df):
    """
    Применяет очистку объема двигателя
    """
    df['engine_volume_original'] = df['engine_volume']
    df['engine_volume_cleaned'] = df.apply(
        lambda row: clean_engine_volume(row['engine_volume'], row.get('brand'), row.get('model')),
        axis=1
    )
    return df


def final_engine_cleaning(df):
    """
    Финальные преобразования для объема двигателя с округлением
    """
    # Заменяем оригинальный столбец очищенным
    df['engine_volume'] = df['engine_volume_cleaned']
    # Удаляем временные столбцы
    df = df.drop(columns=['engine_volume_cleaned', 'engine_volume_original'])
    # Дополнительное округление на всякий случай
    df['engine_volume'] = df['engine_volume'].round(1)
    # Заполняем пропуски медианой по бренду
    if 'brand' in df.columns:
        brand_medians = df.groupby('brand')['engine_volume'].median().round(1)
        def fill_with_brand_median(row):
            if pd.isna(row['engine_volume']) and row['brand'] in brand_medians:
                return brand_medians[row['brand']]
            return row['engine_volume']

        df['engine_volume'] = df.apply(fill_with_brand_median, axis=1)
    # Проверяем что все значения округлены правильно
    unique_decimals = set()
    for val in df['engine_volume'].dropna():
        decimal_part = val - int(val) if val != 0 else 0
        if decimal_part > 0:
            unique_decimals.add(round(decimal_part, 2))
    return df