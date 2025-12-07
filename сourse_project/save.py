def save(df):
    # После всех обработок данных
    output_filename = 'processed_data.csv'
    # Сохраняем DataFrame
    try:
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"Результат сохранён в файл: {output_filename}")
        print(f"Всего записей: {len(df)}")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")