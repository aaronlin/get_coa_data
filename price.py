# encoding: utf-8
import requests
import json


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

#col = ['upper_price', 'lower_price', 'middle_price', 'date', 'amount', 'id', 'name', 'market_id', 'market_name', 'mean_price']
