# encoding: utf-8
import requests
import json
import arrow
import os


def get_data(date):
    url_pattern = 'http://m.coa.gov.tw/OpenData/FarmTransData.aspx?$top=1000&$skip=%d&StartDate=%s'
    data = []
    n_skip = 0
    while True:
        r = requests.get(url_pattern % (n_skip, date))
        if r.status_code == 200:
            new_data = json.loads(r.content)
            if len(new_data) == 0:
                break
            else:
                data.extend(new_data)
                n_skip += 1000
        else:
            break
    return data


def convert_to_taiwan_year(date):
    year = date.year - 1911
    month = date.month
    day = date.day

    return '%d.%02d.%02d' % (year, month, day)


if __name__ == '__main__':
    now = arrow.utcnow()
    date = arrow.get('2015-01-01')
    while date < now:
        print 'getting data of %s...' % date.format('YYYY-MM-DD')
        filepath = 'data/%s.txt' % date.format('YYYY-MM-DD')
        if not os.path.exists(filepath):
            data = get_data(convert_to_taiwan_year(date))
            with open(filepath, 'w') as f:
                for d in data:
                    f.write('%s\n' % json.dumps(d))
            date = date.replace(days=+1)
# col = ['upper_price', 'lower_price', 'middle_price', 'date', 'amount', 'id', 'name', 'market_id', 'market_name', 'mean_price']
