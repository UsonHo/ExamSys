from django.test import TestCase


# Create your tests here.

class Test(object):
    print('2')
    name = 'uson'
    age = '26'
    print('3')

    def __init__(self, gender):
        print('4')
        self.gender = gender

    def __new__(cls, *args, **kwargs):
        print('1')
        # return object.__new__(*args, **kwargs)
        return object.__new__(cls)

    def python(self):
        print('5')


person = Test('男')
person.python()
