import datetime


class Task:
    def __init__(self, values):
        self.name = values['name']
        self.due_date = self.get_date(values['due_date'])
        self.description = values['description']
        self.completed = values['completed'] if 'completed' in values.keys() else False

    def __repr__(self):
        if self.description is not None:
            output_representation = ''.join('\n' + '  ' + string for string in self.description.split('\n'))
        else:
            output_representation = None
        return '\n[ ' + '\x1b[1;32;40m' + 'NAME' + '\x1b[0m' + ': {} \n  '.format(self.name) \
               + '\x1b[1;32;40m' + 'DUE DATE' + '\x1b[0m' + ': {} \n  '.format(self.due_date.date()) \
               + '\x1b[1;32;40m' + 'DESCRIPTION' + '\x1b[0m' + ': {} \n  '.format(output_representation) \
               + '\x1b[1;32;40m' + 'COMPLETED' + '\x1b[0m' + ': {} ]'.format(self.completed)

    @classmethod
    def get_date(cls, date):
        if isinstance(date, datetime.datetime) or date is None:
            return date
        try:
            date = datetime.datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return date

    def get_sending_representation(self):
        return {'name': self.name,
                'due_date': datetime.datetime.strftime(self.due_date, '%d-%m-%Y'),
                'description': self.description,
                'completed': self.completed}
