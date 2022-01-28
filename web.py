import requests, lxml
from lxml import etree, html
from selenium import webdriver

async def get_Facs():
    resp = requests.get("https://rgsu.net/for-students/timetable/"
                        "timetable.html?template=&action=index&"
                        "admin_mode=&f_Faculty=18&group=%D0%9F%D0%9C%D0%98-%D0%91-01-%D0%94-2019-1")
    return [(id_f,f) for id_f,f in zip(html.fromstring(resp.text).xpath('//select[@name="f_Faculty"]/option/@value'),html.fromstring(resp.text).xpath('//select[@name="f_Faculty"]/option/text()'))]

async def get_Groups(f_id):
    params = (
        ('isNaked', '1'),
        ('nc_ctpl', '758'),
        ('gr', ''),
        ('id', f_id),
    )
    resp = requests.get('https://rgsu.net/for-students/timetable/timetable.html', params=params)
    if resp.text:
        return [gr_name for gr_name in html.fromstring(resp.text).xpath('//option/text()')]
    else:
        print('+'+f_id+'+')
        return ['Для этого выбора нет вывода ']

async def get_Table(f_id,gr):
    resp = requests.get(f'https://rgsu.net/for-students/timetable/timetable.html?template=&action=index&admin_mode=&f_Faculty={f_id}&group={gr}')
    table = html.fromstring(resp.text)
    lessons = []
    for week in table.xpath('//table'):
        w = week.xpath('./thead/tr/th/p/span/text()')[0]
        for day in week.xpath('./tbody'):
            d = day.xpath('./tr/td[@class="name"]/text()')[0]
            for l in day.xpath('./tr/td/span[@class="time-start"]/../..'):
                t = l.xpath('./td/span[@class="time-start"]/text()')[0]
                r = l.xpath('./td[2]/text()')[0]
                n = l.xpath('./td[3]/text()')[0]
                tn=l.xpath('./td[4]/text()')[0]
                lessons.append(f'{w} {d} {t} {r} {n} {tn}')
    return lessons

