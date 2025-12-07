import pandas as pd


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
    if 'sale_USD' in df.columns:
        sale = df['sale_USD']
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


    # 2. Стоимость - проверяем на корректность
    if 'price_USD' in df.columns:
        print("Проверка СТОИМОСТИ:")
        # Убедимся что нет отрицательных цен
        negative_prices = (df['price_USD'] < 0).sum()
        if negative_prices > 0:
            print(f"  Исправлено отрицательных цен: {negative_prices}")
            df['price_USD'] = df['price_USD'].clip(lower=0)

    # 3. Итоговая стоимость - проверяем на корректность
    if 'sale_USD' in df.columns:
        print("Проверка ИТОГОВОЙ СТОИМОСТИ:")
        negative_sales = (df['sale_USD'] < 0).sum()
        if negative_sales > 0:
            print(f"  Исправлено отрицательных итогов: {negative_sales}")
            df['sale_USD'] = df['sale_USD'].clip(lower=0)

    return df


def analyze_after_cleaning(df):
    """
    Анализ после очистки числовых столбцов
    """
    print("\nРЕЗУЛЬТАТЫ ПОСЛЕ ОЧИСТКИ:")

    numeric_cols = ['quantity', 'price_USD', 'sale_USD']

    for col in numeric_cols:
        if col in df.columns:
            print(f"\n--- {col.upper()} ---")
            print(f"Тип данных: {df[col].dtype}")
            print(f"Пропуски: {df[col].isnull().sum()}")
            print(f"Мин: {df[col].min():.2f}")
            print(f"Макс: {df[col].max():.2f}")
            print(f"Медиана: {df[col].median():.2f}")
            print(f"Среднее: {df[col].mean():.2f}")


def analyze_special_case(df):
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
        largest_orders = bulk_orders.nlargest(5, 'quantity')[['brand', 'model', 'quantity', 'sale_USD']]
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
        df['sale_USD'] = pd.to_numeric(df['sale_USD'], errors='coerce').astype('float64')
        print("sale_USD → float64")

    return df