import json
import requests
import jsonschema
import pytest
from test_db import get_db_connection


# Test - 1. Create a new record for resources/personnel/military_rank_list,
# Check Encoding, Content-Type and status code with using post requests
@pytest.mark.regres
@pytest.mark.parametrize("code", [201])
def test_military_rank_list(base_url, code, pytestconfig):
    # Получение последнего id из таблицы vector.military_rank_list
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM vector.military_rank_list")
    last_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    target = base_url + "resources/personnel/military_rank_list"
    data = {"id": last_id + 1, "title": "Полковник - autotest"}

    response = requests.post(target, json=data)

    assert response.status_code == code, f"Ошибка: статус ответа равен {response.status_code}"
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT title FROM vector.military_rank_list WHERE title LIKE '%autotest%'")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    assert len(rows) == 1, "Ошибка: в колонке title больше 1-ой записи, содержащих 'autotest'"


# Test - 2. Create a new record for resources/personnel/positions,
# Check Encoding, Content-Type and status code with using post requests
@pytest.mark.regres
@pytest.mark.parametrize("code", [201])
def test_position_list(base_url, code, pytestconfig):
    # Получение последнего id из таблицы vector.military_rank_list
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM vector.positions_list")
    last_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    target = base_url + "resources/personnel/positions"
    data = {"id": last_id + 1, "title": "Главный инженер в/ч - autotest"}

    response = requests.post(target, json=data)

    assert response.status_code == code, f"Ошибка: статус ответа равен {response.status_code}"
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT title FROM vector.positions_list WHERE title LIKE '%autotest%'")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    assert len(rows) == 1, "Ошибка: в колонке title больше 1-ой записи, содержащих 'autotest'"


# Test - 3. Create a new record for resources/personnel,
# Check Encoding, Content-Type and status code with using post requests
def test_create_personnel(base_url, pytestconfig):
    # Получаем id из таблицы vector.positions_list
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM vector.positions_list")
    position_id = cur.fetchone()[0]
    cur.close()

    # Получаем id из таблицы vector.military_rank_list
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM vector.military_rank_list")
    military_rank_id = cur.fetchone()[0]
    cur.close()

    # Получаем последний id из таблицы vector.personnel и увеличиваем на 1
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM vector.personnel")
    personnel_id = cur.fetchone()[0] + 1
    cur.close()
    conn.close()

    # Заменяем значения в файле personnel.json
    with open("files/personnel.json", "r+") as f:
        payload = json.load(f)

        payload["id"] = personnel_id
        payload["position"]["id"] = position_id
        payload["militaryRank"]["id"] = military_rank_id

        f.seek(0)  # перемещаем указатель в начало файла
        json.dump(payload, f, indent=4, ensure_ascii=False)  # записываем измененный объект в файл

    # Отправляем POST запрос
    res = requests.post(base_url + "resources/personnel", json=payload)

    # Проверяем статус код
    assert res.status_code == 201, f"Ошибка: неверный статус код {res.status_code}"
    expected_content_type = pytestconfig.getoption("content_type")
    assert res.headers["Content-Type"] == expected_content_type


# Test - 4. Check created a new record vector.personnel with autotest
def test_personnel_contains_autotest(base_url):
    # Выполняем запрос для проверки наличия только одной записи с подстрокой "autotest" в поле "name"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM vector.personnel WHERE name = 'Никодимович - autotest'")
    count = cur.fetchone()[0]
    cur.close()

    # Закрываем соединение с базой данных
    conn.close()

    # Проверяем, что найдена только одна запись
    assert count == 1, f"Found {count} personnel records with 'autotest' in surName, name, and fatherName fields"


# Test - 5. Check validate schema from answer, also Encoding, Content-Type and status code
def test_api_json_schema_validator(base_url, pytestconfig):
    res = requests.get(base_url + "resources/personnel")

    with open("files/shema_personnel.json", "r") as f:
        schema = json.load(f)

    jsonschema.validate(instance=res.json()[0], schema=schema)
    expected_content_type = pytestconfig.getoption("content_type")
    assert res.headers["Content-Type"] == expected_content_type


# Test - 6. Check a record by ID, also Encoding and Content-Type
@pytest.mark.regres
def test_get_personnel_by_id(base_url, pytestconfig):
    # Получаем последнее цифровое значение из колонки "id" таблицы "personnel"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.personnel ORDER BY id DESC LIMIT 1")
    last_id = cur.fetchone()[0]
    cur.close()

    # Проверяем, что значение last_id не пустое
    assert last_id is not None

    # Делаем GET запрос к ресурсу "personnel" с полученным id
    res = requests.get(f"{base_url}resources/personnel/{last_id}")

    # Проверяем, что запрос завершился успешно, а также Encoding, Content-Type
    assert res.status_code == 200
    expected_content_type = pytestconfig.getoption("content_type")
    assert res.headers["Content-Type"] == expected_content_type

    # Проверяем, что в ответе в поле "name" содержится слово "autotest"
    assert "autotest" in res.json()["name"]


# Test - 7. Delete all records from base permits_to_personnel (временно, после правок кода на бэке удалить)
def test_delete_permits_by_id(base_url):
    # Получаем значение колонки "id" из таблицы "permits_to_personnel"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.permits_to_personnel")
    permit_ids = cur.fetchall()
    cur.close()

    # Удаляем записи, которые содержат значения из колонки "id"
    conn = get_db_connection()
    cur = conn.cursor()
    for permit_id in permit_ids:
        cur.execute(f"DELETE FROM vector.permits_to_personnel WHERE id = {permit_id[0]}")
    conn.commit()
    cur.close()

    # Проверяем, что все записи были удалены
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vector.permits_to_personnel")
    permits = cur.fetchall()
    cur.close()
    assert len(permits) == 0


# Test - 8. Delete personnel by id, check Status code
def test_delete_personnel_by_id(base_url):
    # Получаем все записи, содержащие слово "autotest" в колонке "name" таблицы "personnel"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.personnel WHERE name = 'Никодимович - autotest'")
    personnel_id = cur.fetchone()[0]
    cur.close()

    # Создаем новый тест для каждой записи, содержащей слово "autotest" в колонке "name"
    url = f"{base_url}resources/personnel/{personnel_id}"
    response = requests.delete(url)

    # Проверяем, что статус код равен 204,
    assert response.status_code == 204
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.personnel WHERE name LIKE '%Никодимович - autotest%'")
    personnel = cur.fetchall()
    cur.close()

    # Проверяем, что не найдено ни одного совпадения
    assert len(personnel) == 0


# Test - 9. Delete personnel military rank by ID, check Status code
def test_delete_personnel_military_rank(base_url):
    # Получаем ID записи, содержащей слово "autotest" в колонке "title" таблицы "military_rank_list"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.military_rank_list WHERE title LIKE '%autotest%'")
    military_rank_id = cur.fetchone()[0]
    cur.close()

    # Отправляем DELETE запрос на URL, содержащий ID военного звания
    url = f"{base_url}resources/personnel/military_rank_list/{military_rank_id}"
    response = requests.delete(url)

    # Проверяем, что статус код равен 204
    assert response.status_code == 204
    # Отправляем запрос в базу и ищем все записи, которые содержат autotest
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.military_rank_list WHERE title LIKE '%autotest%'")
    personnel = cur.fetchall()
    cur.close()

    # Проверяем, что не найдено ни одного совпадения
    assert len(personnel) == 0


# Test - 10. Delete Positions list by ID, check Status code
def test_delete_positions_by_id(base_url):
    # Получаем ID записей, содержащие слово "autotest" в колонке "title" таблицы "positions_list"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.positions_list WHERE title LIKE '%autotest%'")
    positions = cur.fetchall()
    cur.close()

    # Отправляем DELETE запрос на URL, содержащий ID должностей
    for p in positions:
        position_id = p[0]
        url = f"{base_url}resources/personnel/positions/{position_id}"
        response = requests.delete(url)

        # Проверяем, что статус код равен 204
        assert response.status_code == 204
        # Отправляем запрос в базу и ищем все записи, которые содержат autotest
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM vector.positions_list WHERE title LIKE '%autotest%'")
        personnel = cur.fetchall()
        cur.close()

        # Проверяем, что не найдено ни одного совпадения
        assert len(personnel) == 0
