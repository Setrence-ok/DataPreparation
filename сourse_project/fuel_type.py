import pandas as pd

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