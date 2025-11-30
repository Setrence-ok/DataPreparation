import pandas as pd
import numpy as np
from datetime import datetime
import pycountry

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


def encode_fuel_type(fuel_type):
    """
    Кодирует вид топлива в краткие категории:
    F - бензин, D - дизель, E - электро, HYB - гибрид
    """
    if pd.isna(fuel_type):
        return 'UNK'

    fuel_str = str(fuel_type).lower().strip()

    # Бензин
    if any(word in fuel_str for word in ['бензин', 'petrol', 'gasoline']):
        return 'F'

    # Дизель
    elif any(word in fuel_str for word in ['дизель', 'diesel']):
        return 'D'

    # Электро
    elif any(word in fuel_str for word in ['электро', 'электричество', 'electric']):
        return 'E'

    # Гибрид
    elif any(word in fuel_str for word in ['гибрид', 'hybrid']):
        return 'HYB'

    # Числовые значения и мусор
    elif fuel_str in ['2', '1,6', '0']:
        return 'UNK'  # Неопределимый тип

    else:
        return 'UNK'


def standardize_drive_type(drive_type):
    """
    Приводит тип привода к единому формату
    """
    if pd.isna(drive_type):
        return 'UNK'

    drive_str = str(drive_type).lower().strip()

    # Передний привод
    if any(word in drive_str for word in ['передний', 'fwd', 'ff', '2wd', '2 wd', '2wd', 'передний (ff)']):
        return 'FWD'

    # Задний привод
    elif any(word in drive_str for word in ['задний', 'rwd']):
        return 'RWD'

    # Полный привод
    elif any(word in drive_str for word in ['полный', 'awd', '4wd', '4 wd', '4x4', '4x4', 'quattro', '4motion']):
        return 'AWD'

    # Мусор и неопределимые значения
    elif drive_str in ['0', '#н/д', 'астана', 'пап', '4x2.2', '4x2', '4x2']:
        return 'UNK'

    else:
        return 'UNK'


def analyze_numeric_anomalies(df):
    """
    Анализирует аномалии в числовых столбцах
    """
    print("АНАЛИЗ АНОМАЛИЙ ДО ОЧИСТКИ:")

    # Количество
    if 'quantity' in df.columns:
        qty = df['quantity']
        print(f"\n--- КОЛИЧЕСТВО ---")
        print(f"Пропуски: {qty.isnull().sum()}")
        print(f"Отрицательные значения: {(qty < 0).sum()}")
        print(f"Нулевые значения: {(qty == 0).sum()}")
        print(f"Значения > 10 (оптовые): {(qty > 10).sum()}")
        print(f"Значения > 50 (крупные оптовые): {(qty > 50).sum()}")
        print(f"Мин: {qty.min()}, Макс: {qty.max()}")
        print(f"Медиана: {qty.median()}")

        # Детальный анализ аномальных значений
        negative_qty = df[qty < 0]
        bulk_qty = df[qty > 10]

        if not negative_qty.empty:
            print(f"\nОтрицательные значения (возвраты):")
            print(negative_qty[['brand', 'model', 'quantity']].head())

        if not bulk_qty.empty:
            print(f"\nОптовые заказы (>10 шт):")
            print(bulk_qty[['brand', 'model', 'quantity']].value_counts().head(10))

    # Стоимость
    if 'price_USD' in df.columns:
        price = df['price_USD']
        print(f"\n--- СТОИМОСТЬ (ЦЕНА) ---")
        print(f"Пропуски: {price.isnull().sum()}")
        print(f"Отрицательные значения: {(price < 0).sum()}")
        print(f"Нулевые значения: {(price == 0).sum()}")
        print(f"Мин: {price.min()}, Макс: {price.max()}")
        print(f"Медиана: {price.median()}")
        print(f"Среднее: {price.mean()}")

    # Итоговая стоимость
    if 'Sale_USD' in df.columns:
        sale = df['Sale_USD']
        print(f"\n--- ИТОГОВАЯ СТОИМОСТЬ ---")
        print(f"Пропуски: {sale.isnull().sum()}")
        print(f"Отрицательные значения: {(sale < 0).sum()}")
        print(f"Нулевые значения: {(sale == 0).sum()}")
        print(f"Мин: {sale.min()}, Макс: {sale.max()}")
        print(f"Медиана: {sale.median()}")
        print(f"Среднее: {sale.mean()}")


def clean_numeric_columns(df):
    """
    Очищает числовые столбцы и обрабатывает аномалии
    """
    print("\nОЧИСТКА ЧИСЛОВЫХ СТОЛБЦОВ:")

    # 1. Количество - обрабатываем аномалии
    if 'quantity' in df.columns:
        print("Обработка КОЛИЧЕСТВА:")

        # Заполняем пропуски (предполагаем 1 продажу)
        df['quantity'] = df['quantity'].fillna(1)
        print(f"  Заполнено пропусков: {df['quantity'].isnull().sum()}")

        # Отрицательные значения = возвраты (оставляем как есть для анализа)
        returns_count = (df['quantity'] < 0).sum()
        print(f"  Возвратов обнаружено: {returns_count}")

        # Очень большие значения = оптовые заказы (оставляем как есть)
        bulk_count = (df['quantity'] > 50).sum()
        print(f"  Крупных оптовых заказов (>50): {bulk_count}")

        # Проверяем логику: цена * количество ≈ итоговая стоимость
        if all(col in df.columns for col in ['price_USD', 'quantity', 'Sale_USD']):
            df['calculated_total'] = df['price_USD'] * df['quantity']
            discrepancy = abs(df['Sale_USD'] - df['calculated_total']) > 1
            print(f"  Расхождений в расчетах: {discrepancy.sum()}")

    # 2. Стоимость - проверяем на корректность
    if 'price_USD' in df.columns:
        print("Проверка СТОИМОСТИ:")
        # Убедимся что нет отрицательных цен
        negative_prices = (df['price_USD'] < 0).sum()
        if negative_prices > 0:
            print(f"  Исправлено отрицательных цен: {negative_prices}")
            df['price_USD'] = df['price_USD'].clip(lower=0)

    # 3. Итоговая стоимость - проверяем на корректность
    if 'Sale_USD' in df.columns:
        print("Проверка ИТОГОВОЙ СТОИМОСТИ:")
        negative_sales = (df['Sale_USD'] < 0).sum()
        if negative_sales > 0:
            print(f"  Исправлено отрицательных итогов: {negative_sales}")
            df['Sale_USD'] = df['Sale_USD'].clip(lower=0)

    return df


def analyze_after_cleaning(df):
    """
    Анализ после очистки числовых столбцов
    """
    print("\nРЕЗУЛЬТАТЫ ПОСЛЕ ОЧИСТКИ:")

    numeric_cols = ['quantity', 'price_USD', 'Sale_USD']

    for col in numeric_cols:
        if col in df.columns:
            print(f"\n--- {col.upper()} ---")
            print(f"Тип данных: {df[col].dtype}")
            print(f"Пропуски: {df[col].isnull().sum()}")
            print(f"Мин: {df[col].min():.2f}")
            print(f"Макс: {df[col].max():.2f}")
            print(f"Медиана: {df[col].median():.2f}")
            print(f"Среднее: {df[col].mean():.2f}")


def analyze_special_cases(df):
    """
    Детальный анализ особых случаев
    """
    print("\nДЕТАЛЬНЫЙ АНАЛИЗ ОСОБЫХ СЛУЧАЕВ:")

    # 1. Возвраты (отрицательное количество)
    if 'quantity' in df.columns:
        returns = df[df['quantity'] < 0]
        if not returns.empty:
            print("📉 ВОЗВРАТЫ (отрицательное количество):")
            print(f"Всего возвратов: {len(returns)}")
            print("Топ брендов по возвратам:")
            print(returns['brand'].value_counts().head(5))

    # 2. Оптовые заказы
    bulk_orders = df[df['quantity'] > 10]
    if not bulk_orders.empty:
        print("\n📦 ОПТОВЫЕ ЗАКАЗЫ (>10 шт):")
        print(f"Всего оптовых заказов: {len(bulk_orders)}")
        print("Топ брендов по оптовым продажам:")
        print(bulk_orders['brand'].value_counts().head(5))

        print("\nСамые крупные оптовые заказы:")
        largest_orders = bulk_orders.nlargest(5, 'quantity')[['brand', 'model', 'quantity', 'Sale_USD']]
        print(largest_orders)

    # 3. Проверка Skoda (как в примере задания)
    if 'brand' in df.columns:
        skoda_orders = df[(df['brand'] == 'Skoda') & (df['quantity'] > 50)]
        if not skoda_orders.empty:
            print(f"\n🚕 SKODA - возможный таксопарк (>50 шт):")
            print(skoda_orders[['model', 'quantity', 'dealer_name']].head())


def final_numeric_conversions(df):
    """
    Финальные преобразования типов числовых столбцов
    """
    print("\nФИНАЛЬНЫЕ ПРЕОБРАЗОВАНИЯ ТИПОВ:")

    # Преобразуем в оптимальные типы
    if 'quantity' in df.columns:
        # Для количества используем int, но сохраняем отрицательные значения
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('int64')
        print("quantity → int64 (сохранены отрицательные значения)")

    if 'price_USD' in df.columns:
        df['price_USD'] = pd.to_numeric(df['price_USD'], errors='coerce').astype('float64')
        print("price_USD → float64")

    if 'Sale_USD' in df.columns:
        df['Sale_USD'] = pd.to_numeric(df['Sale_USD'], errors='coerce').astype('float64')
        print("Sale_USD → float64")

    return df


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

