#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import json
import datetime

from client import parser
from lib import Task
from client.context_manager import get_stream

host = 'localhost'
port = 50000


def initialize_port():
    try:
        with open('link_data.json', 'r') as link_data_file:
            link_data = json.load(link_data_file)
            global host, port
            host, port = link_data['host'], link_data['port']
    except FileNotFoundError:
        pass


def connect(connection_host, connection_port):
    with open('link_data.json', 'w') as link_data_file:
        json.dump({'host': connection_host, 'port': connection_port}, link_data_file)
    global host, port
    host, port = connection_host, connection_port


def is_correct_date(date):
    try:
        if date is not None:
            datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        print('Can\'t recognize date (format : DD-MM-YYYY)')
        return False
    return True


def add_task(name, due_date, has_description):
    if not is_correct_date(due_date):
        return

    description = None
    if has_description:
        print('Task description (exit with Ctrl+D):')
        with get_stream(sys.stdin, 'r') as input_stream:
            description = input_stream.read()

    task = {'name': name, 'due_date': due_date, 'description': description}
    url = 'http://{}:{}/add_task'.format(host, port)
    requests.post(url, json=task)


def delete_task(name):
    url = 'http://{}:{}/delete_task?name={}'.format(host, port, name)
    query_result = requests.post(url).json()
    print(query_result)


def mark_completed(name):
    url = 'http://{}:{}/mark_completed?name={}'.format(host, port, name)
    query_result = requests.post(url).json()
    print(query_result)


def show_tasks(latest_date, with_completed):
    if not is_correct_date(latest_date):
        return

    data = {'latest_date': latest_date, 'with_completed': with_completed}
    url = 'http://{}:{}/show_tasks'.format(host, port)
    response = requests.get(url, json=data)
    chosen = response.json()

    for task in chosen:
        task = Task(task)
        print(task)


def edit_task(name, due_date, has_description):
    if not is_correct_date(due_date):
        return

    delete_task(name)
    add_task(name, due_date, has_description)


def delete_all_tasks():
    url = 'http://{}:{}/delete_all_tasks'.format(host, port)
    requests.post(url)


if __name__ == '__main__':
    initialize_port()

    args = parser.command_parser.parse_args()
    if args.method == 'connect':
        connect(args.host, args.port)
    elif args.method == 'add_task':
        add_task(' '.join(args.name), args.due_date, args.has_description)
    elif args.method == 'delete_task':
        delete_task(' '.join(args.name))
    elif args.method == 'mark_completed':
        mark_completed(' '.join(args.name))
    elif args.method == 'show_tasks':
        show_tasks(args.latest_date, args.with_completed)
    elif args.method == 'edit_task':
        edit_task(' '.join(args.name), args.due_date, args.has_description)
    elif args.method == 'delete_all_tasks':
        delete_all_tasks()
