import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

def eda(df):
    # Настройка отображения
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    # Создание дополнительных признаков для анализа
    df['sale_month'] = df['sale_date'].dt.month
    df['sale_quarter'] = df['sale_date'].dt.quarter
    df['car_age'] = 2019 - df['year_of_release']

    # ОБЩИЙ ОБЗОР РЫНКА
    print("=" * 60)
    print("ОБЩИЙ ОБЗОР РЫНКА")
    print("=" * 60)

    total_sales_usd = df['sale_USD'].sum()
    total_quantity = df['quantity'].sum()
    avg_price = df['price_USD'].mean()
    avg_sale = df['sale_USD'].mean()

    print(f"Всего продаж на сумму: ${total_sales_usd:,.0f}")
    print(f"Всего продано автомобилей: {total_quantity:,}")
    print(f"Средняя цена автомобиля: ${avg_price:,.0f}")
    print(f"Средняя сумма сделки: ${avg_sale:,.0f}")
    print(f"Период данных: {df['sale_date'].min().date()} - {df['sale_date'].max().date()}")
    print(f"Количество уникальных дилеров: {df['dealer_name'].nunique()}")
    print(f"Количество уникальных марок: {df['brand'].nunique()}")

    # ДИНАМИКА ПРОДАЖ ПО МЕСЯЦАМ
    monthly_stats = df.groupby('sale_month').agg({
        'sale_USD': 'sum',
        'quantity': 'sum',
        'price_USD': 'mean'
    }).reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # График 1: Продажи в USD по месяцам
    axes[0, 0].plot(monthly_stats['sale_month'], monthly_stats['sale_USD'], marker='o', linewidth=2)
    axes[0, 0].set_title('Объем продаж по месяцам (USD)', fontsize=14)
    axes[0, 0].set_xlabel('Месяц')
    axes[0, 0].set_ylabel('Сумма продаж, USD')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].fill_between(monthly_stats['sale_month'], monthly_stats['sale_USD'], alpha=0.3)

    # График 2: Количество продаж по месяцам
    axes[0, 1].bar(monthly_stats['sale_month'], monthly_stats['quantity'], color='skyblue')
    axes[0, 1].set_title('Количество продаж по месяцам', fontsize=14)
    axes[0, 1].set_xlabel('Месяц')
    axes[0, 1].set_ylabel('Количество автомобилей')
    for i, v in enumerate(monthly_stats['quantity']):
        axes[0, 1].text(i + 0.7, v + 5, str(v), fontsize=9)

    # График 3: Средняя цена по месяцам
    axes[1, 0].plot(monthly_stats['sale_month'], monthly_stats['price_USD'], marker='s', color='orange', linewidth=2)
    axes[1, 0].set_title('Средняя цена автомобиля по месяцам', fontsize=14)
    axes[1, 0].set_xlabel('Месяц')
    axes[1, 0].set_ylabel('Средняя цена, USD')
    axes[1, 0].grid(True, alpha=0.3)

    # График 4: Распределение типов топлива
    fuel_dist = df['fuel_type'].value_counts()
    axes[1, 1].pie(fuel_dist.values, labels=fuel_dist.index, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title('Распределение по типу топлива', fontsize=14)

    plt.tight_layout()
    plt.show()

    # ТОП-10 МАРОК ПО ПРОДАЖАМ
    print("\n" + "=" * 60)
    print("3. ТОП-10 МАРОК ПО ПРОДАЖАМ")
    print("=" * 60)

    top_brands_sales = df.groupby('brand').agg({
        'sale_USD': 'sum',
        'quantity': 'sum',
        'price_USD': 'mean'
    }).sort_values('sale_USD', ascending=False).head(10)

    print("Топ-10 марок по объему продаж:")
    print(top_brands_sales)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Топ брендов по сумме продаж
    axes[0].barh(top_brands_sales.index, top_brands_sales['sale_USD'] / 1e6, color='steelblue')
    axes[0].set_title('Топ-10 марок по объему продаж (млн USD)', fontsize=14)
    axes[0].set_xlabel('Сумма продаж, млн USD')
    axes[0].invert_yaxis()

    # Топ брендов по количеству
    top_brands_qty = df.groupby('brand')['quantity'].sum().sort_values(ascending=False).head(10)
    axes[1].barh(top_brands_qty.index, top_brands_qty.values, color='lightcoral')
    axes[1].set_title('Топ-10 марок по количеству продаж', fontsize=14)
    axes[1].set_xlabel('Количество автомобилей')
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.show()

    # АНАЛИЗ «МЕРКУР АВТО»
    print("\n" + "=" * 60)
    print("АНАЛИЗ ПОЗИЦИИ «МЕРКУР АВТО»")
    print("=" * 60)

    merkur_data = df[df['dealer_name'] == 'Mercur Auto']

    if len(merkur_data) > 0:
        merkur_sales_usd = merkur_data['sale_USD'].sum()
        merkur_quantity = merkur_data['quantity'].sum()
        merkur_avg_price = merkur_data['price_USD'].mean()
        merkur_share_usd = (merkur_sales_usd / total_sales_usd) * 100
        merkur_share_qty = (merkur_quantity / total_quantity) * 100

        print(f"«Меркур Авто» - ключевые показатели:")
        print(f"- Объем продаж: ${merkur_sales_usd:,.0f}")
        print(f"- Количество проданных авто: {merkur_quantity}")
        print(f"- Средняя цена: ${merkur_avg_price:,.0f}")
        print(f"- Доля рынка (в деньгах): {merkur_share_usd:.2f}%")
        print(f"- Доля рынка (в штуках): {merkur_share_qty:.2f}%")

        # Сравнение с общим рынком
        comparison = pd.DataFrame({
            'Показатель': ['Средняя цена', 'Средняя сумма сделки', 'Средний объем двигателя'],
            'Меркур Авто': [
                merkur_avg_price,
                merkur_data['sale_USD'].mean(),
                merkur_data['engine_volume'].mean()
            ],
            'Весь рынок': [
                df['price_USD'].mean(),
                df['sale_USD'].mean(),
                df['engine_volume'].mean()
            ]
        })

        print("\nСравнение с общим рынком:")
        print(comparison)

        # Топ-5 марок у «Меркур Авто»
        merkur_top_brands = merkur_data.groupby('brand').agg({
            'sale_USD': 'sum',
            'quantity': 'sum'
        }).sort_values('sale_USD', ascending=False).head(5)

        print("\nТоп-5 марок у «Меркур Авто»:")
        print(merkur_top_brands)

        # Визуализация позиции «Меркур Авто»
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Доля на рынке
        market_share = [merkur_share_usd, 100 - merkur_share_usd]
        axes[0, 0].pie(market_share, labels=['Меркур Авто', 'Остальные'], autopct='%1.1f%%', colors=['gold', 'lightblue'])
        axes[0, 0].set_title('Доля «Меркур Авто» на рынке (в деньгах)', fontsize=14)

        # Топ бренды «Меркур Авто»
        axes[0, 1].bar(merkur_top_brands.index, merkur_top_brands['sale_USD'] / 1e6, color='orange')
        axes[0, 1].set_title('Топ-5 марок «Меркур Авто» (млн USD)', fontsize=14)
        axes[0, 1].set_ylabel('Сумма продаж, млн USD')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Сравнение средней цены
        price_comparison = [merkur_avg_price, df['price_USD'].mean()]
        axes[1, 0].bar(['Меркур Авто', 'Весь рынок'], price_comparison, color=['gold', 'steelblue'])
        axes[1, 0].set_title('Сравнение средней цены', fontsize=14)
        axes[1, 0].set_ylabel('Средняя цена, USD')
        for i, v in enumerate(price_comparison):
            axes[1, 0].text(i, v + 1000, f'${v:,.0f}', ha='center', fontsize=10)

        # Распределение по сегментам
        if 'segment_2013' in merkur_data.columns:
            merkur_segments = merkur_data['segment_2013'].value_counts()
            axes[1, 1].pie(merkur_segments.values, labels=merkur_segments.index, autopct='%1.1f%%')
            axes[1, 1].set_title('Распределение продаж «Меркур Авто» по сегментам', fontsize=14)

        plt.tight_layout()
        plt.show()

    else:
        print("Данные по «Меркур Авто» не найдены в датасете")

    # ГЕОГРАФИЧЕСКИЙ АНАЛИЗ
    print("\n" + "=" * 60)
    print("ГЕОГРАФИЧЕСКИЙ АНАЛИЗ")
    print("=" * 60)

    if 'region' in df.columns:
        region_stats = df.groupby('region').agg({
            'sale_USD': 'sum',
            'quantity': 'sum',
            'price_USD': 'mean',
            'dealer_name': 'nunique'
        }).sort_values('sale_USD', ascending=False).head(10)

        print("Топ-10 регионов по объему продаж:")
        print(region_stats)

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Продажи по регионам
        axes[0].barh(region_stats.index, region_stats['sale_USD'] / 1e6, color='teal')
        axes[0].set_title('Топ-10 регионов по объему продаж (млн USD)', fontsize=14)
        axes[0].set_xlabel('Сумма продаж, млн USD')
        axes[0].invert_yaxis()

        # Средняя цена по регионам
        top_regions_price = region_stats.sort_values('price_USD', ascending=False).head(10)
        axes[1].barh(top_regions_price.index, top_regions_price['price_USD'], color='salmon')
        axes[1].set_title('Топ-10 регионов по средней цене', fontsize=14)
        axes[1].set_xlabel('Средняя цена, USD')
        axes[1].invert_yaxis()

        plt.tight_layout()
        plt.show()

    # АНАЛИЗ ТЕХНИЧЕСКИХ ХАРАКТЕРИСТИК
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Распределение коробок передач
    if 'transmission_box' in df.columns:
        transmission_dist = df['transmission_box'].value_counts()
        axes[0, 0].bar(transmission_dist.index, transmission_dist.values, color='lightgreen')
        axes[0, 0].set_title('Распределение по типу КПП', fontsize=14)
        axes[0, 0].set_ylabel('Количество')
        axes[0, 0].tick_params(axis='x', rotation=45)

    # Распределение приводов
    if 'drive_type' in df.columns:
        drive_dist = df['drive_type'].value_counts()
        axes[0, 1].bar(drive_dist.index, drive_dist.values, color='lightcoral')
        axes[0, 1].set_title('Распределение по типу привода', fontsize=14)
        axes[0, 1].set_ylabel('Количество')
        axes[0, 1].tick_params(axis='x', rotation=45)

    # Распределение объема двигателя
    if 'engine_volume' in df.columns:
        axes[1, 0].hist(df['engine_volume'].dropna(), bins=30, edgecolor='black', alpha=0.7)
        axes[1, 0].set_title('Распределение объема двигателя', fontsize=14)
        axes[1, 0].set_xlabel('Объем двигателя, л')
        axes[1, 0].set_ylabel('Количество')

    # Распределение возраста автомобилей
    axes[1, 1].hist(df['car_age'].dropna(), bins=30, edgecolor='black', alpha=0.7, color='purple')
    axes[1, 1].set_title('Распределение возраста автомобилей', fontsize=14)
    axes[1, 1].set_xlabel('Возраст, лет')
    axes[1, 1].set_ylabel('Количество')

    plt.tight_layout()
    plt.show()

    # КОРРЕЛЯЦИОННЫЙ АНАЛИЗ
    print("\n" + "=" * 60)
    print("КОРРЕЛЯЦИОННЫЙ АНАЛИЗ")
    print("=" * 60)

    # Выбираем числовые колонки для корреляции
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 1:
        correlation = df[numeric_cols].corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, fmt='.2f', linewidths=1)
        plt.title('Матрица корреляций', fontsize=16)
        plt.tight_layout()
        plt.show()

        # Наиболее значимые корреляции
        print("Наиболее значимые корреляции:")
        corr_pairs = correlation.unstack().sort_values(ascending=False)
        unique_pairs = pd.DataFrame(corr_pairs).reset_index()
        unique_pairs = unique_pairs[unique_pairs['level_0'] != unique_pairs['level_1']]
        print(unique_pairs.head(10))

    # ТОП-10 МОДЕЛЕЙ ПО ПРОДАЖАМ
    print("\n" + "=" * 60)
    print("ТОП-10 МОДЕЛЕЙ ПО ПРОДАЖАМ")
    print("=" * 60)

    top_models = df.groupby(['brand', 'model']).agg({
        'sale_USD': 'sum',
        'quantity': 'sum',
        'price_USD': 'mean'
    }).sort_values('sale_USD', ascending=False).head(10)

    print("Топ-10 моделей по объему продаж:")
    print(top_models)

    # СЕГМЕНТАЦИЯ И КЛАССЫ
    print("\n" + "=" * 60)
    print("АНАЛИЗ ПО СЕГМЕНТАМ И КЛАССАМ")
    print("=" * 60)

    if 'segment_2013' in df.columns and 'class_2013' in df.columns:
        # Анализ по сегментам
        segment_stats = df.groupby('segment_2013').agg({
            'sale_USD': ['sum', 'count'],
            'price_USD': 'mean'
        }).round(2)

        print("Статистика по сегментам:")
        print(segment_stats)

        # Анализ по классам
        class_stats = df.groupby('class_2013').agg({
            'sale_USD': 'sum',
            'quantity': 'sum'
        }).sort_values('sale_USD', ascending=False).head(10)

        print("\nТоп-10 классов по объему продаж:")
        print(class_stats)

    # АНАЛИЗ КОНКУРЕНТОВ
    print("\n" + "=" * 60)
    print("АНАЛИЗ КОНКУРЕНТОВ")
    print("=" * 60)

    top_dealers = df.groupby('dealer_name').agg({
        'sale_USD': 'sum',
        'quantity': 'sum',
        'price_USD': 'mean',
        'brand': 'nunique'
    }).sort_values('sale_USD', ascending=False).head(10)

    print("Топ-10 дилеров по объему продаж:")
    print(top_dealers)

    # Если «Меркур Авто» в топе, покажем его позицию
    if 'Меркур Авто' in top_dealers.index:
        merkur_rank = top_dealers.index.get_loc('Меркур Авто') + 1
        print(f"\n«Меркур Авто» занимает {merkur_rank}-е место среди всех дилеров")

    # ВЫЯВЛЕНИЕ ТОЧЕК РОСТА ДЛЯ «МЕРКУР АВТО»
    print("\n" + "=" * 60)
    print("ВЫЯВЛЕНИЕ ТОЧЕК РОСТА")
    print("=" * 60)

    if len(merkur_data) > 0:
        # Какие популярные бренды отсутствуют у «Меркур Авто»?
        all_brands = set(df['brand'].unique())
        merkur_brands = set(merkur_data['brand'].unique())
        missing_brands = all_brands - merkur_brands

        # Топ отсутствующих брендов по продажам на рынке
        missing_brands_sales = df[df['brand'].isin(missing_brands)].groupby('brand')['sale_USD'].sum()
        top_missing = missing_brands_sales.sort_values(ascending=False).head(5)

        print("Топ-5 популярных брендов, которых нет у «Меркур Авто»:")
        print(top_missing)

        # Регионы, где «Меркур Авто» слаб
        if 'region' in df.columns:
            all_regions = df.groupby('region')['sale_USD'].sum().sort_values(ascending=False)
            merkur_regions = merkur_data.groupby('region')['sale_USD'].sum()

            # Регионы с высокими продажами, но низким присутствием «Меркур Авто»
            potential_regions = all_regions.head(10).index.difference(merkur_regions.index)
            print(f"\nТоп-10 регионов, где «Меркур Авто» отсутствует: {list(potential_regions)}")

    # СВОДНАЯ СТАТИСТИКА
    print("\n" + "=" * 60)
    print("СВОДНАЯ СТАТИСТИКА")
    print("=" * 60)

    summary_stats = pd.DataFrame({
        'Показатель': [
            'Общий объем продаж (USD)',
            'Общее количество продаж',
            'Средняя цена автомобиля',
            'Количество уникальных дилеров',
            'Количество уникальных марок',
            'Самый популярный бренд',
            'Самый дорогой бренд (средняя цена)',
            'Самый продаваемый месяц',
            'Средний возраст автомобиля'
        ],
        'Значение': [
            f"${total_sales_usd:,.0f}",
            f"{total_quantity:,}",
            f"${avg_price:,.0f}",
            df['dealer_name'].nunique(),
            df['brand'].nunique(),
            top_brands_sales.index[0] if len(top_brands_sales) > 0 else 'N/A',
            df.groupby('brand')['price_USD'].mean().idxmax() if len(df) > 0 else 'N/A',
            monthly_stats.loc[monthly_stats['sale_USD'].idxmax(), 'sale_month'] if len(monthly_stats) > 0 else 'N/A',
            f"{df['car_age'].mean():.1f} лет"
        ]
    })

    print(summary_stats.to_string(index=False))