import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def download_vhi_data(region_index, save_directory):
    url = f"https://www.ncei.noaa.gov/data/vegetation-health/vhp_4km/vhp_weekly/{region_index}.txt"
    response = requests.get(url)
    
    if response.status_code == 200:
        filename = f"{region_index}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        file_path = os.path.join(save_directory, filename)
        with open(file_path, 'w') as file:
            file.write(response.text)

def rename_regions(df):
    region_mapping = {
        1: "Вінницька",
        2: "Волинська",
        3: "Дніпропетровська",
        4: "Донецька",
        5: "Житомирська",
        6: "Закарпатська",
        7: "Запорізька",
        8: "Івано-Франківська",
        9: "Київська",
        10: "Кіровоградська",
        11: "Луганська",
        12: "Львівська",
        13: "Миколаївська",
        14: "Одеська",
        15: "Полтавська",
        16: "Рівенська",
        17: "Сумська",
        18: "Тернопільська",
        19: "Харківська",
        20: "Херсонська",
        21: "Хмельницька",
        22: "Черкаська",
        23: "Чернівецька",
        24: "Чернігівська",
        25: "Республіка Крим"
    }
    
    df['Назва'] = df['№ області'].map(region_mapping)
    return df

def vhi_extremes_by_year(vhi_data, region, year):
    region_data = vhi_data[(vhi_data['Назва'] == region) & (vhi_data['Рік'] == year)]
    max_vhi = region_data['VHI'].max()
    min_vhi = region_data['VHI'].min()
    return max_vhi, min_vhi

def extreme_drought_years(vhi_data, region, threshold_percentage):
    region_data = vhi_data[vhi_data['Назва'] == region]
    years_with_drought = []
    
    for year in region_data['Рік'].unique():
        year_data = region_data[region_data['Рік'] == year]
        drought_percentage = (year_data['VHI'] < threshold_percentage).mean() * 100
        if drought_percentage > threshold_percentage:
            years_with_drought.append((year, drought_percentage))
    
    return years_with_drought

def moderate_drought_years(vhi_data, region, threshold_percentage):
    region_data = vhi_data[vhi_data['Назва'] == region]
    years_with_drought = []
    
    for year in region_data['Рік'].unique():
        year_data = region_data[region_data['Рік'] == year]
        drought_percentage = (year_data['VHI'] < threshold_percentage).mean() * 100
        if drought_percentage > threshold_percentage:
            years_with_drought.append((year, drought_percentage))
    
    return years_with_drought

if __name__ == "__main__":
    # Папка для збереження завантажених файлів
    save_directory = "vhi_data"
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    # Завантаження даних VHI для всіх областей
    for region_index in range(1, 26):
        download_vhi_data(region_index, save_directory)

    # Зчитування даних в фрейм та перейменування індексів областей
    vhi_data = pd.DataFrame()
    for file_name in os.listdir(save_directory):
        file_path = os.path.join(save_directory, file_name)
        df = pd.read_csv(file_path, delimiter='\s+')
        vhi_data = pd.concat([vhi_data, df], ignore_index=True)

    vhi_data = rename_regions(vhi_data)
    print(vhi_data)

    # Приклади використання процедур для аналізу даних
    region = "Вінницька"
    year = 2022
    max_vhi, min_vhi = vhi_extremes_by_year(vhi_data, region, year)
    print(f"Максимальний VHI для {region} у {year}: {max_vhi}")
    print(f"Мінімальний VHI для {region} у {year}: {min_vhi}")

    threshold_percentage = 30  # Поріг для визначення екстремальної посухи
    extreme_drought_years_list = extreme_drought_years(vhi_data, region, threshold_percentage)
    print(f"Роки з екстремальними посухами для {region} (поріг {threshold_percentage}%):")
    for year, percentage in extreme_drought_years_list:
        print(f"Рік {year}: {percentage}% області")

    threshold_percentage = 40  # Поріг для визначення помірної посухи
    moderate_drought_years_list = moderate_drought_years(vhi_data, region, threshold_percentage)
    print(f"Роки з помірними посухами для {region} (поріг {threshold_percentage}%):")
    for year, percentage in moderate_drought_years_list:
        print(f"Рік {year}: {percentage}% області")
