import psycopg2
from lib import Task

params = dict(dbname='default', user="evgenabramov", password="12345678", host="localhost")


def connect_database(name, user, password):
    params['dbname'] = name
    params['user'] = user
    params['password'] = password
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks(
                task_name VARCHAR(40),
                due_date DATE,
                description VARCHAR(1000),
                completed BOOLEAN DEFAULT False
            );
        ''')


def add_task(task):
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (task_name, due_date, description) VALUES (%s, %s, %s);',
                    (task.name, task.get_database_representation(), task.description))


def delete_task(name):
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks WHERE task_name = %s;', [name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return False
        cur.execute('DELETE FROM tasks WHERE task_name = %s;', [name])
        return True


def mark_completed(name):
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks WHERE task_name = %s;', [name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return False
        cur.execute('UPDATE tasks SET completed = True WHERE task_name = %s;', [name])
        return True


def show_tasks(latest_date, with_completed):
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM tasks
        WHERE (NOT completed OR %s) AND ((%s IS NULL) OR (due_date IS NOT NULL AND due_date < %s))
        ORDER BY due_date''', (with_completed, latest_date, latest_date))
        rows = cur.fetchall()
        chosen = []
        for row in rows:
            name, due_date, description, completed = row
            chosen.append(Task({'name': name,
                                'due_date': str(due_date),
                                'description': description,
                                'completed': completed}))
        return chosen


def delete_all_tasks():
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE tasks;')
