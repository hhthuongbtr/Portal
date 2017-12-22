import MySQLdb as mdb
import json
from django.conf import settings

class Database:
    def connect(self):
        db = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        port = int(settings.DATABASES['default']['PORT'])
        return mdb.connect(host=host, port=port, user=user, passwd=password, db=db, charset='utf8')

    def close_connect(self, session):
        return session.close()

    '''
    INSERT, UPDATE, DELETE, CREATE, and SET statement
    '''
    def execute_non_query(self, query):
        if not query:
            print 'No query!'
            return 0
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            session.commit()
            self.close_connect(session)
            return 1
        except Exception as e:
            return 0

    '''SELECT'''
    def execute_query(self, query):
        if not query:
            print 'No query!'
            return 0
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            self.close_connect(session)
            return rows
        except Exception as e:
            print 'Bug: ' + str(e)
            return 1