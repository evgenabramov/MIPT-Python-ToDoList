# -*- coding: utf-8 -*-
import argparse


def build_connect_parser():
    connect_parser = subs.add_parser('connect', description='Connect client to server with specified port')
    connect_parser.set_defaults(method='connect')
    connect_parser.add_argument('--host', required=False, default='localhost', help='Host for connecting')
    connect_parser.add_argument('--port', required=False, default=50000, help='Port for connecting')
    return connect_parser


def build_add_task_parser():
    add_task_parser = subs.add_parser('add_task', description='Add task to list')
    add_task_parser.set_defaults(method='add_task')
    add_task_parser.add_argument('--name', nargs='*', required=True, help='Name of task',
                                 default=argparse.SUPPRESS)
    add_task_parser.add_argument('--due-date', required=False,
                                 dest='due_date', help='Due date of task')
    add_task_parser.add_argument('--with-description', dest='has_description', action='store_true',
                                 help='Shows that task has a description (optional argument)')
    return add_task_parser


def build_delete_task_parser():
    delete_task_parser = subs.add_parser('delete_task', description='Delete task from list')
    delete_task_parser.set_defaults(method='delete_task')
    delete_task_parser.add_argument('--name', nargs='*', required=True, help='Name of task',
                                    default=argparse.SUPPRESS)
    return delete_task_parser


def build_mark_completed_parser():
    mark_completed_parser = subs.add_parser('mark_completed', description='Tag task as completed')
    mark_completed_parser.set_defaults(method='mark_completed')
    mark_completed_parser.add_argument('--name', nargs='*', required=True, help='Name of task',
                                       default=argparse.SUPPRESS)
    return mark_completed_parser


def build_view_tasks_parser():
    view_tasks_parser = subs.add_parser('show_tasks', description='Show tasks with due date until the specified one')
    view_tasks_parser.set_defaults(method='show_tasks')
    view_tasks_parser.add_argument('--latest-date', required=False, dest='latest_date', help='Latest date of tasks')
    view_tasks_parser.add_argument('--with-completed', dest='with_completed', action='store_true',
                                   help='Include completed task (optional argument)')
    return view_tasks_parser


def build_edit_task_parser():
    edit_task_parser = subs.add_parser('edit_task', description='Edit task with specified name')
    edit_task_parser.set_defaults(method='edit_task')
    edit_task_parser.add_argument('--name', nargs='*', required=True, help='Name of modifying task',
                                  default=argparse.SUPPRESS)
    edit_task_parser.add_argument('--due-date', required=False, help='Due date of task')
    edit_task_parser.add_argument('--with-description', dest='has_description', action='store_true',
                                  help='Shows that task has a description (optional argument)')
    return edit_task_parser


def build_delete_all_tasks_parser():
    delete_all_tasks_parser = subs.add_parser('delete_all_tasks', description='Delete all tasks from list')
    delete_all_tasks_parser.set_defaults(method='delete_all_tasks')
    return delete_all_tasks_parser


command_parser = argparse.ArgumentParser()
subs = command_parser.add_subparsers()
connect_parser = build_connect_parser()
add_task_parser = build_add_task_parser()
delete_task_parser = build_delete_task_parser()
mark_completed_parser = build_mark_completed_parser()
view_tasks_parser = build_view_tasks_parser()
edit_task_parser = build_edit_task_parser()
delete_all_tasks_parser = build_delete_all_tasks_parser()
