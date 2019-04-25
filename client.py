#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import parser
import sys
import json
import datetime
from context_manager import get_stream

port = 50000


def initialize_port():
    try:
        with open('.port-info', 'r') as output_file:
            global port
            port = int(output_file.read())
    except FileNotFoundError:
        pass


def connect(connection_port):
    with open('.port-info', 'w') as output_file:
        output_file.write(connection_port)
    global port
    port = connection_port


def add_task(name, due_date, has_description):
    try:
        if due_date is not None:
            datetime.datetime.strptime(due_date, '%d-%m-%Y')
    except ValueError:
        print('Can\'t recognize date (format : DD-MM-YYYY)')
        return

    description = None
    if has_description:
        print('Task description (exit with Ctrl+D):')
        with get_stream(sys.stdin, 'r') as input_stream:
            description = input_stream.read()

    task = {'name': name, 'due_date': due_date, 'description': description}
    url = 'http://localhost:{}/add_task'.format(port)
    requests.post(url, json=json.dumps(task))
    return


def delete_task(name):
    url = 'http://localhost:{}/delete_task?name={}'.format(port, name)
    requests.post(url)
    return


def mark_completed(name):
    url = 'http://localhost:{}/mark_completed?name={}'.format(port, name)
    requests.post(url)
    return


def view_tasks(latest_date, with_completed):
    try:
        if latest_date is not None:
            datetime.datetime.strptime(latest_date, '%d-%m-%Y')
    except ValueError:
        print('Can\'t recognize date (format : DD-MM-YYYY)')
        return
    data = {'latest_date': latest_date, 'with_completed': with_completed}
    url = 'http://localhost:{}/view_tasks'.format(port)
    response = requests.get(url, json=json.dumps(data))
    tasks = response.json()
    print(tasks)
    return


def edit_task(name, due_date, has_description):
    delete_task(name)
    add_task(name, due_date, has_description)
    return


def delete_all_tasks():
    url = 'http://localhost:{}/delete_all_tasks'.format(port)
    requests.post(url)
    return


if __name__ == '__main__':
    initialize_port()

    args = parser.command_parser.parse_args()
    if args.method == 'connect':
        connect(args.port)
    elif args.method == 'add_task':
        add_task(' '.join(args.name), args.due_date, args.has_description)
    elif args.method == 'delete_task':
        delete_task(' '.join(args.name))
    elif args.method == 'mark_completed':
        mark_completed(' '.join(args.name))
    elif args.method == 'view_tasks':
        view_tasks(args.latest_date, args.with_completed)
    elif args.method == 'edit_task':
        edit_task(' '.join(args.name), args.due_date, args.has_description)
    elif args.method == 'delete_all_tasks':
        delete_all_tasks()
