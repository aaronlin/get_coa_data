from bottle import run, response
import bottle
import sqlite3
import json


db = sqlite3.connect('../data/AgriDB.sqlite')
cursor = db.cursor()
resume_schema = ['pid', 'date', 'operation', 'detail', 'memo']
app = bottle.app()

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


@app.route('/resume/<pid>')
def get_resume(pid):
    cursor.execute(
        '''
        select * from OnP where PID = %s order by Date
        ''' % pid)
    result = []
    for resume in cursor.fetchall():
        result.append(dict(zip(resume_schema, resume)))
    return json.dumps(result)

app.install(EnableCors())


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
