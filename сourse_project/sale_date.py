import pandas as pd

def analyze_date_components(df):
    """
    Анализирует год и месяц перед созданием даты
    """
    print("АНАЛИЗ ИСХОДНЫХ ДАННЫХ:")

    if 'year' in df.columns:
        print(f"Год: {df['year'].unique()}")  # Должен быть только 2019

    if 'month' in df.columns:
        print(f"Месяцы: {df['month'].unique()}")
        print(f"Количество записей по месяцам:")
        print(df['month'].value_counts().sort_index())


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
        print("❌ ОШИБКА: Отсутствуют столбцы year или month")
        return df

    print("Создание даты продажи...")

    # Создаем новый столбец
    df['sale_date'] = df.apply(
        lambda row: create_sale_date(row['year'], row['month']),
        axis=1
    )

    # Проверяем результат
    successful_dates = df['sale_date'].notna().sum()
    failed_dates = df['sale_date'].isna().sum()

    print(f"✅ Успешно создано дат: {successful_dates}")
    print(f"❌ Не удалось создать: {failed_dates}")

    if failed_dates > 0:
        print("Проблемные записи:")
        problem_rows = df[df['sale_date'].isna()][['year', 'month']].head()
        print(problem_rows)

    return df


def analyze_created_dates(df):
    """
    Анализирует созданные даты продажи
    """
    print("\nАНАЛИЗ СОЗДАННЫХ ДАТ:")

    if 'sale_date' not in df.columns:
        print("❌ Столбец sale_date не создан")
        return

    print(f"Диапазон дат продаж:")
    print(f"Начало: {df['sale_date'].min()}")
    print(f"Конец: {df['sale_date'].max()}")

    print(f"\nРаспределение по месяцам:")
    monthly_sales = df['sale_date'].dt.to_period('M').value_counts().sort_index()
    print(monthly_sales)

    print(f"\nРаспределение по дням недели:")
    day_of_week = df['sale_date'].dt.day_name().value_counts()
    print(day_of_week)


def remove_original_columns(df):
    """
    Удаляет исходные столбцы Год и Месяц
    """
    print("\nУДАЛЕНИЕ ИСХОДНЫХ СТОЛБЦОВ...")

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


def final_date_check(df):
    """
    Финальная проверка дат продажи
    """
    print("\nФИНАЛЬНАЯ ПРОВЕРКА:")

    if 'sale_date' in df.columns:
        print("✅ Столбец sale_date создан успешно")
        print(f"Тип данных: {df['sale_date'].dtype}")
        print(f"Пропуски: {df['sale_date'].isnull().sum()}")
        print(f"Уникальных дат: {df['sale_date'].nunique()}")

        # Проверяем что все даты - последние дни месяца
        df['is_last_day'] = df['sale_date'].dt.is_month_end
        last_day_count = df['is_last_day'].sum()
        total_count = len(df)
        print(f"Даты являются последним днем месяца: {last_day_count}/{total_count}")

        # Удаляем временный столбец
        df = df.drop(columns=['is_last_day'])

    else:
        print("❌ Столбец sale_date не создан")

    return df

