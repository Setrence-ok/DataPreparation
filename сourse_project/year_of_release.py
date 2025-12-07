import pandas as pd


def clean_year_column(df, column_name='year_of_release'):
    # Создаем копию колонки как строку
    years = df[column_name].astype(str)

    # Удаляем неразрывные пробелы и другие артефакты
    years = years.str.replace('\xa0', '')  # неразрывный пробел
    years = years.str.replace(' ', '')  # обычный пробел
    years = years.str.replace('\\', '')  # обратный слеш
    years = years.str.replace('x', '')  # буква x

    # Удаляем все нецифровые символы
    years = years.str.replace(r'[^0-9]', '', regex=True)

    # Преобразуем в число, пустые строки -> NaN
    years_numeric = pd.to_numeric(years, errors='coerce')

    # Оставляем только разумные годы (например, 1900-2025)
    years_numeric = years_numeric[(years_numeric >= 1900) & (years_numeric <= 2025)]

    # Обновляем колонку в датафрейме
    df[column_name] = years_numeric

    # Преобразуем в Int64 (поддерживает NaN)
    df[column_name] = df[column_name].astype('Int64')

    return df