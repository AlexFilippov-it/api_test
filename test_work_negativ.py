import requests
import json
import jsonschema
import pytest
import datetime
from test_db import get_db_connection


# Test - 1. Check create work with id
def test_create_work_with_invalid_id(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["id"] = invalid_date
            #print(f"Trying to create work with projectId = {invalid_date}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid float number" in response.json()["details"]["requestBody.id"]["message"]


# Test - 2. Check create work with invalid date
def test_create_work_with_invalid_date(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/date_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["start_date"] = invalid_date

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid ISO 8601 datetime format, i.e. YYYY-MM-DDTHH:mm:ss"\
                   in response.json()["details"]["requestBody.start_date"]["message"]


# Test - 3. Check create work with invalid projectId
def test_create_work_with_invalid_projectid(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["projectId"] = invalid_date
            #print(f"Trying to create work with projectId = {invalid_date}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid float number" in response.json()["details"]["requestBody.projectId"]["message"]


# Test - 4. Check create with invalid typeId
def test_create_work_with_invalid_typeid(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["typeId"] = invalid_date
            #print(f"Trying to create work with projectId = {invalid_date}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid float number" in response.json()["details"]["requestBody.typeId"]["message"]


# Test - 5. Check create with invalid duration
def test_create_work_with_invalid_duration(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["duration"] = invalid_date
            #print(f"Trying to create work with projectId = {invalid_date}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid float number" in response.json()["details"]["requestBody.duration"]["message"]


# Test - 6. Check create with invalid progress
def test_create_work_with_invalid_progress(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["progress"] = invalid_date
            #print(f"Trying to create work with projectId = {invalid_date}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid float number" in response.json()["details"]["requestBody.progress"]["message"]


# Test - 7. Check create with invalid parent
def test_create_work_with_invalid_parent(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_date in f:
            invalid_date = invalid_date.strip()
            data["parent"] = invalid_date
            #print(f"Trying to create work with projectId = {invalid_date}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "invalid float number" in response.json()["details"]["requestBody.parent"]["message"]


# Test - 8. Check create work with invalid resource id
def test_create_work_with_invalid_resource_id(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_id in f:
            invalid_id = invalid_id.strip()
            data["resources"] = [{"id": invalid_id, "title": "Несуществующий ресурс", "type": {"id": 1, "title": "ВВСТ"}}]

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "details" in response.json()
            assert "resources.$0.id" in response.json()["details"]
            assert "invalid float number" in response.json()["details"]["resources.$0.id"]["message"]



# Test - 9. Check create work with invalid resource type id
def test_create_work_with_invalid_resource_type_id(api_url_works, pytestconfig):
    target = api_url_works

    with open("files/create_work.json") as f:
        data = json.load(f)

    with open("notvalid/projectid_notvalid.txt") as f:
        for invalid_id in f:
            invalid_id = invalid_id.strip()
            data["resources"] = [{"id": 2, "title": "Несуществующий ресурс", "type": {"id": invalid_id, "title": "ВВСТ"}}]
            # print(f"Trying to create work with projectId = {invalid_id}")

            response = requests.post(url=target, json=data)
            assert response.status_code == 422
            expected_content_type = pytestconfig.getoption("content_type")
            assert response.headers["Content-Type"] == expected_content_type
            assert "details" in response.json()
            assert "resources.$0.type.id" in response.json()["details"]
            assert "invalid float number" in response.json()["details"]["resources.$0.type.id"]["message"]


# Test - 10. Add a new record for table Works and after that check it
def test_create_work_for_check_negativ_test(api_url_works):
    target = api_url_works
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("files/create_work.json") as f:
        data = json.load(f)
        data["start_date"] = now

    response = requests.post(url=target, json=data)
    assert response.status_code == 201

# Test - 11. Check update record for table Works with invalid ID Put request
def test_api_works_update_id_invalid(api_url_works):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["id"] = invalid_date
                # print(f"Trying to create work with projectId = {invalid_date}")
                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                assert "invalid float number" in response.json()["details"]["requestBody.id"]["message"]


# Test - 12. Check update record for table Works with invalid Date Put request
def test_api_works_update_date_invalid(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/date_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["start_date"] = invalid_date

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "invalid ISO 8601 datetime format, i.e. YYYY-MM-DDTHH:mm:ss" \
                       in response.json()["details"]["requestBody.start_date"]["message"]


# Test - 13. Check update record for table Works with invalid Date Put request
def test_api_works_update_projectid_invalid(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["projectId"] = invalid_date
                # print(f"Trying to create work with projectId = {invalid_date}")

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "invalid float number" in response.json()["details"]["requestBody.projectId"]["message"]


# Test - 14. Check update with invalid typeId
def test_update_work_with_invalid_typeid(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["typeId"] = invalid_date
                # print(f"Trying to create work with projectId = {invalid_date}")

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "invalid float number" in response.json()["details"]["requestBody.typeId"]["message"]


# Test - 15. Check update with invalid duration
def test_update_work_with_invalid_duration(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["duration"] = invalid_date
                # print(f"Trying to create work with projectId = {invalid_date}")

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "invalid float number" in response.json()["details"]["requestBody.duration"]["message"]


# Test - 16. Check update with invalid progress
def test_update_work_with_invalid_progress(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["progress"] = invalid_date
                # print(f"Trying to create work with projectId = {invalid_date}")

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "invalid float number" in response.json()["details"]["requestBody.progress"]["message"]


# Test - 17. Check update with invalid parent
def test_update_work_with_invalid_parent(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_date in f:
                invalid_date = invalid_date.strip()
                data["parent"] = invalid_date
                # print(f"Trying to create work with projectId = {invalid_date}")

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "invalid float number" in response.json()["details"]["requestBody.parent"]["message"]


# Test - 18. Check update work with invalid resource id
def test_update_work_with_invalid_resource_id(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_id in f:
                invalid_id = invalid_id.strip()
                data["resources"] = [
                    {"id": invalid_id, "title": "Несуществующий ресурс", "type": {"id": 1, "title": "ВВСТ"}}]

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "details" in response.json()
                assert "resources.$0.id" in response.json()["details"]
                assert "invalid float number" in response.json()["details"]["resources.$0.id"]["message"]


# Test - 19. Check create work with invalid resource type id
def test_update_work_with_invalid_resource_type_id(api_url_works, pytestconfig):
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

        with open("files/create_work.json") as f:
            data = json.load(f)

        with open("notvalid/projectid_notvalid.txt") as f:
            for invalid_id in f:
                invalid_id = invalid_id.strip()
                data["resources"] = [
                    {"id": 2, "title": "Несуществующий ресурс", "type": {"id": invalid_id, "title": "ВВСТ"}}]
                # print(f"Trying to create work with projectId = {invalid_id}")

                response = requests.put(url=target, json=data)
                assert response.status_code == 422
                expected_content_type = pytestconfig.getoption("content_type")
                assert response.headers["Content-Type"] == expected_content_type
                assert "details" in response.json()
                assert "resources.$0.type.id" in response.json()["details"]
                assert "invalid float number" in response.json()["details"]["resources.$0.type.id"]["message"]


# Test - 20. Delete Check record after negativ requests
@pytest.mark.regres
def test_api_works_delete_after_negativ_check(api_url_works, pytestconfig):
    target = api_url_works
    response = requests.get(target)
    works = response.json()
    found_works = []
    for work in works:
        if work["text"] == "autotest - произвольный текcт для проверки поля":
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


# Test - 21. Check created record with using Invalid ID
def test_get_one_work_by_id_negative(api_url_works, pytestconfig):
    target = api_url_works

    with open("notvalid/delete_notvalid.txt") as f:
        for invalid_id in f:
            invalid_id = invalid_id.strip()

            # Формирование URL для GET-запроса с невалидным id
            target = f"{api_url_works}/{invalid_id}"

            # Выполнение GET-запроса и проверка ответа
            response = requests.get(target)

            if response.status_code == 404:
                assert response.text == "Not found",\
                    f"Некорректный текст ошибки для id = {invalid_id}"
            elif response.status_code == 422:
                error_message = "invalid float number"
                error_value = invalid_id
                response_json = response.json()
                assert response_json["message"] == "Validation Failed",\
                    f"Некорректный текст ошибки для id = {invalid_id}"
                assert response_json["details"]["id"]["message"] == error_message,\
                    f"Некорректный текст ошибки для id = {invalid_id}"
                assert response_json["details"]["id"]["value"] == error_value,\
                    f"Некорректное значение поля value для id = {invalid_id}"
            else:
                assert False, f"Некорректный статус код для id = {invalid_id}"
