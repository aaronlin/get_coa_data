from bottle import route, run


@route('/resume/<pid>')
def get_resume(pid):
    return ''


if __name__ == '__main__':
    run(host='localhost', port=8080)
