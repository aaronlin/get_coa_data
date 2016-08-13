from bottle import route, run
import sqlite3
import json


db = sqlite3.connect('../data/AgriDB.sqlite')
cursor = db.cursor()
resume_schema = ['pid', 'date', 'operation', 'detail', 'memo']

@route('/resume/<pid>')
def get_resume(pid):
    cursor.execute('select * from OnP where PID = %s order by Date' % pid)
    result = []
    for resume in cursor.fetchall():
        result.append(dict(zip(resume_schema, resume)))
    return json.dumps(result)


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
