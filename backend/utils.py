# coding=utf-8
import os
import MySQLdb
from settings import database


def create_connection():
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    return db


def load_template(template_name=""):
    template_dir = os.path.dirname(__file__) + '/templates/'
    f = open(template_dir + template_name + '.html')
    _template = f.read()
    f.close()
    return _template 
