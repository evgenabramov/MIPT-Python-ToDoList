# Клиент-серверное приложение "Список дел"
> Проект по курсу 'Python' ФИВТ МФТИ, 2 семестр, 2019 год

### Описание команд

В качестве интерфейса взаимодействия с пользователем выступает консольный ввод.

Запуск сервера:
```bash
./server.py --host [HOST] --port [PORT]
```

Подключение клиента к серверу:
```bash
./client.py connect --port [PORT] --database-name [DB NAME] --user [USER] --password [PASSWORD] 
```

Структура запосов:
1. Добавить новую задачу:

    ```bash
    ./client.py add_task --name [NAME] [--due-date [DATE]] [--with-description]
    ```

    При указании `--with-description` в запросе будет предложено ввести 
    описание задачи прямо в консоли, для выхода нужно использовать `Ctrl+D`.

2. Удалить задачу из списка:

    ```bash
    ./client.py delete_task --name [NAME]
    ```
    
3. Пометить задачу выполненной:

    ```bash
    ./client.py mark_completed --name [NAME]    
    ```
    
4. Просмотреть список задач:

    ```bash
    ./client.py show_tasks [--latest-date [LATEST DATE]] [--with-completed]  
    ```
    
5. Редактировать задачу:

    ```bash
    ./client.py edit_task --name [NAME] [--due-date [DATE]] [--with-description]
    ```
    
6. Удалить все задачи:

    ```bash
    ./client.py delete_all_tasks
    ```


[Ссылка](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e) с информацией о том, как настроить базу данных на сервере и пользователя: 
