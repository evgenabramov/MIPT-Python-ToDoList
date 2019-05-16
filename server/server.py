#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import json
import argparse

import database

app = flask.Flask(__name__)


@app.route('/add_task', methods=['POST'])
def add_task():
    database.add_task(Task(flask.request.json))
    return 'OK'


@app.route('/delete_task', methods=['POST'])
def delete_task():
    is_correct_query = database.delete_task(flask.request.args['name'])
    if not is_correct_query:
        return json.dumps('There is no task with such name')
    return json.dumps('OK')


@app.route('/mark_completed', methods=['POST', 'GET'])
def mark_completed():
    is_correct_query = database.mark_completed(flask.request.args['name'])
    if not is_correct_query:
        return json.dumps('There is no task with such name')
    return json.dumps('OK')


@app.route('/show_tasks', methods=['GET'])
def show_tasks():
    latest_date = Task.get_datetime_representation(flask.request.json['latest_date'])
    with_completed = flask.request.json['with_completed']
    chosen = [task.get_sending_representation() for task in database.show_tasks(latest_date, with_completed)]
    return json.dumps(chosen)


@app.route('/delete_all_tasks', methods=['POST'])
def delete_all_tasks():
    database.delete_all_tasks()
    return 'OK'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int, help='Port for connecting')
    parser.add_argument('--host', default='localhost', type=str, help='Host for connecting')
    parser.add_argument('--database-name', dest='database_name', required=True, help='The name of server database')
    parser.add_argument('--user', required=True, help='User name')
    parser.add_argument('--password', required=True, help='Password for database user')
    args = parser.parse_args()

    database.connect_database(args.database_name, args.user, args.password)
    app.run('{}::'.format(args.host), args.port, debug=True, threaded=True)
