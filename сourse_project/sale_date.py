import pandas as pd

def create_month_mapping():
    """
    Создает mapping русских названий месяцев в числовые
    """
    month_mapping = {
        'Январь': 1,
        'Февраль': 2,
        'Март': 3,
        'Апрель': 4,
        'Май': 5,
        'Июнь': 6,
        'Июль': 7,
        'Август': 8,
        'Сентябрь': 9,
        'Октябрь': 10,
        'Ноябрь': 11,
        'Декабрь': 12
    }
    return month_mapping

def create_sale_date(year, month_name):
    """
    Создает дату продажи - последний день месяца
    """
    try:
        # Преобразуем название месяца в число
        month_mapping = create_month_mapping()
        month_num = month_mapping.get(month_name)

        if month_num is None:
            return pd.NaT
        # Определяем последний день месяца
        if month_num in [1, 3, 5, 7, 8, 10, 12]:
            last_day = 31
        elif month_num in [4, 6, 9, 11]:
            last_day = 30
        elif month_num == 2:
            # Февраль 2019 - не високосный
            last_day = 28
        else:
            return pd.NaT
        return pd.Timestamp(year=year, month=month_num, day=last_day)
    except Exception as e:
        return pd.NaT


def create_sale_date_column(df):
    """
    Создает столбец с датой продажи
    """
    # Проверяем наличие необходимых столбцов
    if 'year' not in df.columns or 'month' not in df.columns:
        print("Отсутствуют столбцы year или month")
        return df
    # Создаем новый столбец
    df['sale_date'] = df.apply(
        lambda row: create_sale_date(row['year'], row['month']),
        axis=1
    )
    # Проверяем результат
    successful_dates = df['sale_date'].notna().sum()
    failed_dates = df['sale_date'].isna().sum()

    if failed_dates > 0:
        print("Проблемные записи:")
        problem_rows = df[df['sale_date'].isna()][['year', 'month']].head()
        print(problem_rows)

    return df


def remove_original_columns(df):
    """
    Удаляет исходные столбцы Год и Месяц
    """
    columns_to_drop = []
    if 'year' in df.columns:
        columns_to_drop.append('year')
        print(f"Удален столбец: year")

    if 'month' in df.columns:
        columns_to_drop.append('month')
        print(f"Удален столбец: month")

    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        print(f"Итоговые столбцы: {list(df.columns)}")
    else:
        print("Столбцы year и month не найдены")

    return df

