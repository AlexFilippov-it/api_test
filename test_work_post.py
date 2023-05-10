import requests
import json
import jsonschema
import pytest
import datetime
from test_db_connection import get_db_connection



# Test - 1. Check status code
@pytest.mark.regres
@pytest.mark.parametrize("code", [200])
def test_url_status(api_url_works, code, request_method):
    target = api_url_works
    response = request_method(url=target)
    assert response.status_code == code


# Test - 2. Check request Encoding and Content-Type
@pytest.mark.regres
def test_url_content_type(api_url_works, request_method, pytestconfig):
    target = api_url_works
    response = request_method(url=target)
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type


# Test - 3. Check validate schema from answer
@pytest.mark.regres
def test_api_json_schema_works(api_url_works):
    res = requests.get(api_url_works)

    with open("files/shema_works.json", "r") as f:
        schema = json.load(f)

    jsonschema.validate(instance=res.json(), schema=schema)


# Test - 4. Add a new record for table Works and after that check it
@pytest.mark.regres
def test_create_work(api_url_works, pytestconfig):
    target = api_url_works
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("files/create_work.json") as f:
        data = json.load(f)
        data["start_date"] = now

    response = requests.post(url=target, json=data)
    assert response.status_code == 201
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type

    # Establishing a database connection
    try:
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

    except Exception as e:
        print(f"Error: {e}")


# Test - 5. Check created record with using By ID from table Works
@pytest.mark.regres
def test_get_one_work_by_id(api_url_works, pytestconfig):
    target = api_url_works
    # Получение id созданной записи из БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vector.works WHERE text LIKE '%autotest%'")
    result = cur.fetchone()
    cur.close()
    conn.close()
    assert result is not None, "Запись не найдена в БД"
    id = result[0]

    # Формирование URL для GET-запроса из полученого id и выполняем поиск по нему
    target = f"{api_url_works}/{id}"

    # Выполнение GET-запроса и проверка ответа
    response = requests.get(target)
    assert response.status_code == 200, "Статус код не равен 200"
    assert response.json()["text"] == "autotest - произвольный текcт для проверки поля", \
        "Поле 'text' не соответствует ожидаемому значению"
    assert response.json()["id"] == id, "Поле 'id' не соответствует ожидаемому значению"
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type


# Test - 6. Look for a record which include "autotest" and update it with using Put request
@pytest.mark.regres
def test_api_works_update(api_url_works):
    target = api_url_works
    response = requests.get(target)

    if response.status_code == 200:
        works = response.json()
        for work in works:
            if "autotest" in work["text"]:
                # Находим первую работу, в которой в колонке text есть вхождение autotest
                id = work["id"]
                break

        # Отправляем PUT-запрос на обновление работы с ID
        target = f"{api_url_works}/{id}"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("files/update_work.json") as f:
            data = json.load(f)
            data["id"] = id
            data["start_date"] = now

        response = requests.put(target, json=data)

        if response.status_code == 204:
            print(f"Работа с id {id} обновлена")
            assert response.status_code == 204, "Статус код не равен 204"
        else:
            print(f"Ошибка запроса: {response.status_code}")
    else:
        print(f"Ошибка запроса: {response.status_code}")


# Test - 7. Check delete requests
@pytest.mark.regres
def test_api_works_delete(api_url_works, pytestconfig):
    target = api_url_works
    response = requests.get(target)
    works = response.json()
    found_works = []
    for work in works:
        if work["text"] == "autotest - обновленный текcт для проверки поля":
            found_works.append(work)

    # Проверяем, что найдена только одна запись
    assert len(found_works) == 1
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type

    # Получаем id найденной записи
    work_id = found_works[0]["id"]

    # Отправляем DELETE запрос для удаления найденной записи
    response = requests.delete(f"{api_url_works}/{work_id}")

    # Проверяем, что статус код ответа равен 204 (No Content)
    assert response.status_code == 204


@pytest.mark.regres
def test_look_for_autotest_in_base():
    try:
        conn = get_db_connection()
        assert conn is not None

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vector.works WHERE text LIKE '%autotest%'")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()

        assert result == 0
    except Exception as e:
        pytest.fail(f"Failed to execute query: {e}")
