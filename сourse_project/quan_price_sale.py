import pandas as pd

def clean_numeric_columns(df):
    """
    Очищает числовые столбцы и обрабатывает аномалии
    """
    # Количество - обрабатываем аномалии
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

    # Стоимость - проверяем на корректность
    if 'price_USD' in df.columns:
        print("Проверка СТОИМОСТИ:")
        # Убедимся что нет отрицательных цен
        negative_prices = (df['price_USD'] < 0).sum()
        if negative_prices > 0:
            print(f"  Исправлено отрицательных цен: {negative_prices}")
            df['price_USD'] = df['price_USD'].clip(lower=0)

    # Итоговая стоимость - проверяем на корректность
    if 'sale_USD' in df.columns:
        print("Проверка ИТОГОВОЙ СТОИМОСТИ:")
        negative_sales = (df['sale_USD'] < 0).sum()
        if negative_sales > 0:
            print(f"  Исправлено отрицательных итогов: {negative_sales}")
            df['sale_USD'] = df['sale_USD'].clip(lower=0)

    return df


def final_numeric_conversions(df):
    """
    Финальные преобразования типов числовых столбцов
    """
    # Преобразуем в оптимальные типы
    if 'quantity' in df.columns:
        # Для количества используем int, но сохраняем отрицательные значения
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('int64')

    if 'price_USD' in df.columns:
        df['price_USD'] = pd.to_numeric(df['price_USD'], errors='coerce').astype('float64')

    if 'Sale_USD' in df.columns:
        df['sale_USD'] = pd.to_numeric(df['sale_USD'], errors='coerce').astype('float64')

    return df