import pandas as pd
import numpy as np


def final_data_type_conversions(df):
    """
    Выполняет финальные преобразования типов данных в датафрейме.
    """

    # Создаем копию датафрейма, чтобы не изменять оригинал
    df_transformed = df.copy()

    # 2. Преобразование категориальных столбцов
    categorical_columns = [
        'fuel_type',
        'transmission_box',
        'drive_type',
        'segment_2013',
        'class_2013'
    ]

    for col in categorical_columns:
        if col in df_transformed.columns:
            # Преобразуем в строковый тип сначала (на случай, если есть нестроковые значения)
            df_transformed[col] = df_transformed[col].astype(str)
            # Затем в категориальный тип
            df_transformed[col] = pd.Categorical(df_transformed[col])
            print(f"Столбец '{col}' преобразован в категориальный тип")
            print(f"  Категории: {df_transformed[col].cat.categories.tolist()}")
            print(f"  Количество уникальных значений: {df_transformed[col].nunique()}")
        else:
            print(f"Столбец '{col}' не найден в датафрейме")

    return df_transformed