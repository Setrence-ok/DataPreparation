from sale_date import *
from country_of_origin import *
from fuel_type import *
from dealer_name import *
from engine_volume import *
from region_area import *
from transmission import *
from type_conversions import *
from quan_price_sale import *
from drive_type import *
from year_of_release  import *

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
    'Продажа, USD': 'sale_USD',
    'Класс 2013': 'class_2013',
    'Страна-производитель': 'country_of_origin'
}

df = df.rename(columns=column_mapping)

# Удаление пустых строк и дубликатов
df = df.dropna(how='all')
df = df.drop_duplicates()

print("\nПропущенные значения:")
print(df.isnull().sum())
df['country_of_origin'] = df['country_of_origin'].apply(country_to_alpha3)
df['fuel_type'] = df['fuel_type'].apply(encode_fuel_type)
df['drive_type'] = df['drive_type'].apply(standardize_drive_type)

analyze_numeric_anomalies(df)
df = clean_numeric_columns(df)
analyze_after_cleaning(df)
analyze_special_case(df)
df = final_numeric_conversions(df)

analyze_date_components(df)
df = create_sale_date_column(df)
analyze_created_dates(df)
df = remove_original_columns(df)
df = final_date_check(df)
analyze_company_names(df)

df = clean_company_names(df)
analyze_changes(df)
analyze_mercur_auto(df)
df = final_company_cleaning(df)
final_company_check(df)

analyze_engine_volume(df)
df = apply_engine_cleaning(df)
analyze_cleaning_changes(df)
print(df.info())
analyze_special_cases(df)
df = final_engine_cleaning(df)

df['area'] = df.apply(correct_area, axis=1)
df['area'] = df['area'].str.title()
df['region'] = df['region'].str.title()
df['region'] = df.apply(correct_region, axis=1)

df['transmission_box'] = df['transmission_box'].apply(classify_transmission_simple)

df = final_data_type_conversions(df)
df = clean_year_column(df)
df[['price_USD', 'sale_USD']] = df[['price_USD', 'sale_USD']].round(2)
df = df.dropna(subset=['year_of_release', 'area', 'engine_volume'])

# После всех обработок данных
output_filename = 'processed_data.csv'

# Сохраняем DataFrame
try:
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"✅ Результат сохранён в файл: {output_filename}")
    print(f"   Всего записей: {len(df)}")

    # Дополнительная информация
    print("\n📊 Обзор данных:")
    print(df.info())

except Exception as e:
    print(f"❌ Ошибка при сохранении: {e}")



