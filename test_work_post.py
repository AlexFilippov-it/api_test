import requests
import datetime
from test_db import get_db_connection


def test_create_work(base_url):
    target = base_url + "works"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "id": 33,
        "projectId": 1,
        "text": "autotest - произвольный текcт для проверки поля",
        "start_date": now,
        "duration": 5,
        "progress": 0,
        "parent": 0,
        "typeId": 1,
        "resources": [{"id": 3, "title": "ПЭВМ", "type": {"id": 1, "title": "ВВСТ"}}]
    }

    response = requests.post(url=target, json=data)
    assert response.status_code == 201

    # Establishing a database connection
    conn = get_db_connection()

    # Сreate a cursor object for executing SQL queries
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM vector.works WHERE text LIKE '%autotest%'"
        " AND duration=5 AND progress=0 AND parent=0")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()

    assert result == 1


# Получаем id созданной записи
def test_get_one_work_by_id(base_url):
    target = base_url + "works"
    # Получение id созданной записи из БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.works WHERE text LIKE '%autotest%' AND duration=5 AND progress=0 AND parent=0")
    result = cur.fetchone()
    cur.close()
    conn.close()
    assert result is not None, "Запись не найдена в БД"
    id = result[0]

    # Формирование URL для GET-запроса из полученого id и выполняем поиск по нему
    target = base_url + f"works/{id}"

    # Выполнение GET-запроса и проверка ответа
    response = requests.get(target)
    assert response.status_code == 200, "Статус код не равен 200"
    assert response.json()["text"] == "autotest - произвольный текcт для проверки поля",\
        "Поле 'text' не соответствует ожидаемому значению"
    assert response.json()["id"] == id, "Поле 'id' не соответствует ожидаемому значению"
