import requests
from lxml import html
import csv

# URL выбранного сайта
url = "https://www.worldometers.info/world-population/"

# Заголовки HTTP-запроса с User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

try:
    # Отправка GET-запроса
    response = requests.get(url, headers=headers)
    # Проверяем статус ответа
    if response.status_code == 200:
        print("HTML-страница успешно загружена.")

        # Парсинг содержимого HTML
        tree = html.fromstring(response.content)
        
        # XPath для извлечения строк таблицы
        table_rows = tree.xpath('//table[contains(@class, "table")]/tbody/tr')

        # Создаём список для хранения извлечённых данных
        data = []

        # Проходим по строкам таблицы
        for row in table_rows:
            # Извлекаем текст ячеек
            cells = row.xpath('./td/text()')
            data.append(cells)

        # Проверяем данные
        if data:
            print("Данные успешно извлечены из таблицы:")
            for row in data[:5]:  # Вывод первых 5 строк для проверки
                print(row)
        else:
            print("Не удалось извлечь данные из таблицы.")
    else:
        print(f"Ошибка загрузки страницы. Код: {response.status_code}")
except Exception as e:
    print(f"Произошла ошибка при загрузке страницы: {e}")

# Имя файла для сохранения данных
output_file = "population_data.csv"

try:
    # Открываем CSV-файл для записи
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Записываем заголовок (вручную указанный, т.к. в таблице может его не быть)
        writer.writerow(["Year", "Growth Rate", "Population Change", "Median Age", "Fertility Rate", "Urban Population %"])
        
        # Записываем данные
        writer.writerows(data)
        
    print(f"Данные успешно сохранены в файл {output_file}.")
except Exception as e:
    print(f"Ошибка при сохранении данных в CSV: {e}")
