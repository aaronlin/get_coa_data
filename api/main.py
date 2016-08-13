from bottle import Bottle, route, run, response
import sqlite3
import json


db = sqlite3.connect('../data/AgriDB.sqlite')
cursor = db.cursor()
resume_schema = ['pid', 'date', 'operation', 'detail', 'memo']
app = Bottle()


@app.hook('after_request')
def enable_cors():
    print("after_request hook")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@route('/resume/<pid>')
@enable_cors
def get_resume(pid):
    cursor.execute(
        '''
        select * from OnP where PID = %s order by Date
        ''' % pid)
    result = []
    for resume in cursor.fetchall():
        result.append(dict(zip(resume_schema, resume)))
    return json.dumps(result)


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
