import requests
import cerberus

url = "http://localhost:3000/works"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Запрос выполнен успешно")
    print(data)
else:
    print(f"Произошла ошибка, статус-код: {response.status_code}")