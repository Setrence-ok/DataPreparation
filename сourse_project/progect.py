import pandas as pd
import numpy as np
from datetime import datetime
import pycountry
from func import *
from func6 import *
from func7 import *
from func8 import *

# Загрузка данных
df = pd.read_csv('autokz2019.csv', sep=';', decimal=',', thousands=' ')

# Удаление ненужных столбцов (предполагаемые названия на русском)
columns_to_drop = ['Форма расчета', 'Сегмент', 'Наименование дилерского центра',
                   'Тип клиента', 'Модификация', 'Локализация производства', 'Сегментация Eng']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Переименование столбцов на английский
column_mapping = {
    'Год': 'year',
    'Месяц': 'month',
    'Компания': 'dealer_name',
    'Бренд': 'brand',
    'Модель': 'model',
    'Год выпуска': 'year_of_release',
    'Вид топлива': 'fuel_type',
    'Объём двиг, л,': 'engine_volume',
    'Коробка передач': 'transmission_box',
    'Тип привода': 'drive_type',
    'Сегментация 2013': 'segment_2013',
    'Регион': 'region',
    'Область': 'area',
    'Количество': 'quantity',
    'Цена, USD': 'price_USD',
    'Продажа, USD': 'Sale_USD',
    'Класс 2013': 'class_2013',
    'Страна-производитель': 'country_of_origin'
}

df = df.rename(columns=column_mapping)

# Удаление пустых строк и дубликатов
df = df.dropna(how='all')
df = df.drop_duplicates()

#print("\nПропущенные значения:")
#print(df.isnull().sum())
df['country_of_origin'] = df['country_of_origin'].apply(country_to_alpha3)
df['fuel_type'] = df['fuel_type'].apply(encode_fuel_type)
df['drive_type'] = df['drive_type'].apply(standardize_drive_type)

#analyze_numeric_anomalies(df)
#df = clean_numeric_columns(df)
#analyze_after_cleaning(df)
#analyze_special_cases(df)
#df = final_numeric_conversions(df)

#analyze_date_components(df)
#df = create_sale_date_column(df)
#analyze_created_dates(df)
#df = remove_original_columns(df)
#df = final_date_check(df)
#analyze_company_names(df)

#df = clean_company_names(df)
#analyze_changes(df)
#analyze_mercur_auto(df)
#df = final_company_cleaning(df)
#final_company_check(df)

#analyze_engine_volume(df)
#df = apply_engine_cleaning(df)
#analyze_cleaning_changes(df)
#analyze_special_cases(df)
#df = final_engine_cleaning(df)

print(f'Регион: {df['region'].unique()}')
#print(f'Область: {df['area'].unique()}')






