import datetime


class Task:
    def __init__(self, values):
        self.name = values['name']
        self.due_date = self.get_datetime_representation(values['due_date'])
        self.description = values['description']
        self.completed = values['completed'] if 'completed' in values.keys() else False

    def __str__(self):
        if self.description is not None:
            output_representation = ''.join('\n' + '  ' + string for string in self.description.split('\n'))
        else:
            output_representation = None
        date_output = self.due_date
        if not self.due_date is None:
            date_output = self.due_date.date()
        return '\n[ ' + '\x1b[1;32;40m' + 'NAME' + '\x1b[0m' + ': {} \n  '.format(self.name) \
               + '\x1b[1;32;40m' + 'DUE DATE' + '\x1b[0m' + ': {} \n  '.format(date_output) \
               + '\x1b[1;32;40m' + 'DESCRIPTION' + '\x1b[0m' + ': {} \n  '.format(output_representation) \
               + '\x1b[1;32;40m' + 'COMPLETED' + '\x1b[0m' + ': {} ]'.format(self.completed)

    @classmethod
    def get_datetime_representation(cls, date):
        if isinstance(date, datetime.date) or date is None:
            return date
        try:
            date = datetime.datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return date

    def get_database_representation(self):
        return None if self.due_date is None else datetime.datetime.strftime(self.due_date, '%Y-%m-%d')

    def get_sending_representation(self):
        return {'name': self.name,
                'due_date': self.get_database_representation(),
                'description': self.description,
                'completed': self.completed}
