import json
import requests
import jsonschema
import pytest
from test_db import get_db_connection


# Test - 1. Check status code
@pytest.mark.regres
@pytest.mark.parametrize("code", [200])
def test_url_status(base_url, code, request_method):
    target = base_url + "resources"
    response = request_method(url=target)
    assert response.status_code == code


# Test - 2. Check request Encoding and Content-Type
@pytest.mark.regres
def test_url_content_type(base_url, request_method, pytestconfig):
    target = base_url + "resources"
    response = request_method(url=target)
    expected_content_type = pytestconfig.getoption("content_type")
    assert response.headers["Content-Type"] == expected_content_type


# Test - 3. Check validate schema from answer
@pytest.mark.regres
def test_api_json_schema_resources(base_url):
    target = base_url + "resources"
    res = requests.get(target)

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "headers": {"type": "object"},
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "quantity": {"type": ["integer", "null"]},
                "type": {
                    "type": ["object", "null"],
                    "properties": {
                        "headers": {"type": "object"},
                        "id": {"type": "integer"},
                        "title": {"type": "string"}
                    },
                    "required": ["id", "title"]
                }
            },
            "required": ["id", "title"]
        }
    }

    data = res.json()
    jsonschema.validate(instance=data, schema=schema)


# Test - 4. Add new resource
def test_add_resource(base_url):
    # Получаем последний id из базы данных
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM vector.resources")
    last_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    # Создаем данные для запроса
    new_id = last_id + 1
    data = {
        "id": new_id,
        "title": "autotest - произвольный текст для проверки поля",
        "type": {
            "id": 1,
            "title": "ВВСТ"
        }
    }

    # Отправляем запрос
    res = requests.post(base_url + "resources", json=data)

    # Проверяем статус код
    assert res.status_code == 201

    # Проверяем, что запись добавлена в базу данных
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM vector.resources WHERE title LIKE '%autotest - произвольный"
                f" текст для проверки поля%'")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()

    assert result == 1


# Test - 5. Update resource by ID
def test_update_resource(base_url):
    # Находим запись с title, содержащим "autotest"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM vector.resources WHERE title LIKE '%autotest%'")
        row = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        assert False, f"Ошибка при выполнении SQL запроса: {str(e)}"

    # Проверяем, что запись найдена
    assert row is not None

    # Извлекаем id из записи
    resource_id = row[0]

    # Создаем данные для запроса
    data = {
        "id": resource_id,
        "title": "autotest - обновленный текст для проверки поля",
        "type": {
            "id": 1,
            "title": "Личный состав"
        }
    }

    # Отправляем запрос
    res = requests.put(base_url + f"resources/{resource_id}", json=data)

    # Проверяем статус код
    assert res.status_code == 204


# Test - 6. Look for words like autotest with using get requests
def test_check_autotest_resources(base_url, code, request_method):
    target = base_url + "resources"
    response = requests.get(target)

    assert response.status_code == code, f"Ожидался код статуса {code}, но получен {response.status_code}"

    # Найдем все ресурсы, содержащие "autotest" в названии
    resources = json.loads(response.content)
    autotest_resources = [r for r in resources if 'autotest' in r['title'].lower()]

    # Проверим, что найден один ресурс, содержащий "autotest" в названии
    assert len(autotest_resources) == 1, "Ресурсы с 'autotest' в названии не найдены"

    # Получим ID найденного ресурса
    autotest_id = autotest_resources[0]['id']

    # Создадим новый запрос, используя ID найденного ресурса
    target = base_url + f"resources/{autotest_id}"
    response = requests.get(target)

    # Проверим, что ответ содержит статус-код 200
    assert response.status_code == 200, f"Ожидался код статуса 200, но получен {response.status_code}"

    # Проверим, что поле 'title' ресурса содержит текст "autotest"
    resource = json.loads(response.content)
    assert 'autotest' in resource['title'].lower(), "Название ресурса не содержит 'autotest'"


# Test - 7. Check delete requests by ID
def test_delete_autotest_resource(base_url):
    target = base_url + "resources"
    response = requests.get(target)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Найдем все ресурсы, содержащие "autotest" в названии
    resources = json.loads(response.content)
    autotest_resources = [r for r in resources if 'autotest' in r['title'].lower()]

    # Получим ID найденного ресурса
    autotest_id = autotest_resources[0]['id']

    # Удалим найденный ресурс
    target = base_url + f"resources/{autotest_id}"
    response = requests.delete(target)

    # Проверим, что ответ содержит статус-код 204
    assert response.status_code == 204, f"Expected status code 204, but got {response.status_code}"


# Test - 8. Look for all records which include autotest in a base
def test_autotest_resource_not_found_in_postgres():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vector.resources WHERE title LIKE '%autotest%'")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
    except Exception as e:
        assert False, f"Ошибка при выполнении SQL запроса: {str(e)}"

    assert count == 0, f"Найдено {count} записей с 'autotest' в названии"
