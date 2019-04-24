#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import json
import argparse
import datetime

app = flask.Flask(__name__)
app.tasks = []


@app.route('/add_task', methods=['POST'])
def add_task():
    print('NEW TASK HAS BEEN ADDED:', flask.request.json)
    new_task = json.loads(flask.request.json)
    if new_task['due_date'] is not None:
        new_task['due_date'] = datetime.datetime.strptime(new_task['due_date'], '%d-%m-%Y')
    new_task['completed'] = False
    app.tasks.append(new_task)
    return 'OK'


@app.route('/delete_task', methods=['POST'])
def delete_task():
    name = flask.request.args['name']
    for index, task in enumerate(app.tasks):
        if task['name'] == name:
            print('TASK {} HAS BEEN DELETED'.format(name))
            app.tasks.remove(task)
    return 'OK'


@app.route('/mark_completed', methods=['POST'])
def mark_completed():
    name = flask.request.args['name']
    for index, task in enumerate(app.tasks):
        if task['name'] == name:
            print('TASK {} HAS BEEN MARKED AS COMPLETED'.format(name))
            task['completed'] = True
    return 'OK'


@app.route('/view_tasks', methods=['GET'])
def view_tasks():
    latest_date = json.loads(flask.request.json)['latest_date']
    with_completed = json.loads(flask.request.json)['with_completed']
    if latest_date is not None:
        latest_date = datetime.datetime.strptime(latest_date, '%d-%m-%Y')
    result = []
    for task in app.tasks:
        if ((latest_date is None) or (task['due_date'] is not None and task['due_date'] < latest_date)) and (
                with_completed or not task['completed']):
            result.append(str(task))
    return json.dumps('\n'.join(result))


@app.route('/delete_all_tasks', methods=['POST'])
def delete_all_tasks():
    print("ALL TASKS DELETED")
    app.tasks.clear()
    return 'OK'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int)
    args = parser.parse_args()

    app.run('::', args.port, debug=True, threaded=True)
