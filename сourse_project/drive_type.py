import pandas as pd


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