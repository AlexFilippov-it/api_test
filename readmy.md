Описание тестов.

Файл test_work_post.py проверки для запроса works

- Проверка статус кода
- Проверка Encoding and Content-Type
- Проверка validate schema из файла
- Добавление новой записи из файла, подключение к базе и поиск созданной записи в ней (post запрос)
- Проверка созданной записи с использованием ID в запросе (get запрос)
- Проверка обновления записи с использованием ID в запросе (put запрос)
- Проверка удаления записи с использованием ID в запросе (delete запрос)

Файл test_resources.py проверки для запроса resources

- Проверка статус кода
- Проверка Encoding and Content-Type
- Проверка validate schema из файла
- Добавление нового ресурса (post запрос) и его проверка запросом в базу
- Проверка обновления ресурса с использованием ID в запросе (put запрос)
- Проверка обновления ресурса запросом в базу
- Проверка удаления ресурса с использованием ID в запросе
- Проверка удаленного ресураса запросом в базу

Файл test_personnel.py

- Проверка добавления новой записи для resources/personnel/military_rank_list
- Проверка всех записей для resources/personnel/military_rank_list
- Проверка validate schema из файла для resources/personnel/military_rank_list
- Проверка создания новой записи для resources/personnel/positions и проверка созданной записи запросом в базу
- Проверка создания новой записи для resources/personnel (post запрос)
- Проверка созданной записи для resources/personnel запросом в базу
- Проверка validate schema из файла для resources/personnel
- Проверка записи для resources/personnel с использованием ID в запросе
- Удаляем все записи из таблицы permits_to_personnel (временный тест)
- Проверка удаления записи для resources/personnel с использованием ID в запросе
- Проверка удаления personnel military rank by ID
- Проверка удаления Positions list by ID
