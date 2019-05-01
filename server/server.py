#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import json
import argparse
import database
from lib import Task

app = flask.Flask(__name__)


@app.route('/add_task', methods=['POST'])
def add_task():
    database.add_task(Task(json.loads(flask.request.json)))
    return 'OK'


@app.route('/delete_task', methods=['POST'])
def delete_task():
    database.delete_task(flask.request.args['name'])
    return 'OK'


@app.route('/mark_completed', methods=['POST'])
def mark_completed():
    database.mark_completed(flask.request.args['name'])
    return 'OK'


@app.route('/show_tasks', methods=['GET'])
def show_tasks():
    latest_date = Task.get_date(json.loads(flask.request.json)['latest_date'])
    with_completed = json.loads(flask.request.json)['with_completed']
    chosen = [task.get_sending_representation() for task in database.show_tasks(latest_date, with_completed)]
    return json.dumps(chosen)


@app.route('/delete_all_tasks', methods=['POST'])
def delete_all_tasks():
    database.delete_all_tasks()
    return 'OK'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int, help='Port for connecting')
    parser.add_argument('--database-name', dest='database_name', required=True, help='The name of server database')
    args = parser.parse_args()

    database.connect_database(args.database_name)
    app.run('::', args.port, debug=True, threaded=True)
