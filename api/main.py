from bottle import run, response
import bottle
import sqlite3
import json


db = sqlite3.connect('../data/AgriDB.sqlite')
cursor = db.cursor()
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
        select OnP.PID, PName, FName, Place, Date, Type, Detail, Memo
        from OnP join
            (select PID, PName, FName, Place from agrigood) as A
        on OnP.PID = A.PID
        where ONP.PID = %s
        ''' % pid)
    result = []
    schema = ['pid', 'product', 'farmer', 'place', 'date', 'operation', 'detail', 'memo']
    for resume in cursor.fetchall():
        result.append(dict(zip(schema, resume)))
    return json.dumps(result)


@app.route('/')
def get_categories():
    cursor.execute(
        '''
        select id, PName, img_path, mean_price from product
        where img_path is not null
        order by img_path desc
        ''')
    schema = ['category_id', 'category', 'img_path', 'mean_price']
    result = []
    for category in cursor.fetchall():
        result.append(dict(zip(schema, category)))
    return json.dumps(result)


@app.route('/category/<category_id>')
def get_products(category_id):
    category_id = int(category_id)
    cursor.execute(
        '''
        select PName, img_path from product where id = %d
        ''' % category_id)
    category_name, img_path = cursor.fetchone()

    cursor.execute(
        '''
        select PID, PName, FName, Place, PackDate, Info, OName,
            CName, ValidDate, OnP, Certificate
        from agrigood where PName like '%%%s%%'
        ''' % category_name)
    schema = ['product_id', 'product', 'farmer', 'place', 'package_date',
              'info', 'organization', 'certificate_company', 'valid_date',
              'update_date', 'is_certificated']
    result = []
    for product in cursor.fetchall():
        data = dict(zip(schema, product))
        data.update({'img_path': img_path})
        result.append(data)
    return json.dumps(result)


app.install(EnableCors())

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
