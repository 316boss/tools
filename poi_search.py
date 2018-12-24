import requests
from urllib.parse import urlencode, quote_plus
import urllib
import sys
import getopt
import hashlib
import json
import time




def search(keyword, lng1, lat1, lng2, lat2):

    url_uncode = '/ws/place/v1/search?boundary=%s&key=%s&keyword=%s&page_size=1' % ('rectangle(%f,%f,%f,%f)' % (lng1, lat1, lng2, lat2), "WCCBZ-B54W5-WK3IW-Q2R3A-WNEZO-5SF7F", keyword)
    m = hashlib.md5()
    m.update(("%s%s" % (url_uncode, "D6iAb7fIjrJSzjGM5nnykxpYvDQNbAJ8")).encode('utf-8'))
    sig = m.hexdigest()

    r = requests.get('https://apis.map.qq.com/ws/place/v1/search',
                 {
                     "keyword": quote_plus(keyword),
                     "boundary": 'rectangle(%f,%f,%f,%f)' % (lng1, lat1, lng2, lat2),

                     "page_size": 1,
                     "key": "WCCBZ-B54W5-WK3IW-Q2R3A-WNEZO-5SF7F",
                     "sig": sig
                 })

    res = eval(r.content)

    return res

def go(lng1, lat1, lng2, lat2, simplify = False):

    with open('poi_type.json') as f:
        types = json.load(f)
        a = 1
        for key in types:
            search_res = search(key, lng1, lat1, lng2, lat2)
            print('> %s: %d' % (key, search_res['count']))
            if not simplify:
                for sec_key in types[key]:
                    sec_res = search(sec_key, lng1, lat1, lng2, lat2)
                    print('>>> %s: %d' % (sec_key, sec_res['count']))
                    time.sleep(0.2)



    return

# go(39.8072,116.3689,39.9149,116.3793)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hts', ['help', 'type=', 'lng1=', 'lat1=', 'lng2=', 'lat2=', 'simplify'])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    keyword = None
    lng1 = None
    lat1 = None
    lng2 = None
    lat2 = None
    simplify = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('-h --help\n'
                  '-s --simplify 只显示主分类\n'
                  '-t --type= 指定关键字\n'
                  '--lng1= <左下/西南>经度\n'
                  '--lat1= <左下/西南>纬度\n'
                  '--lng2= <右上/东北>经度\n'
                  '--lat2= <右上/东北>纬度\n')
            sys.exit(0)
        if opt in ('-t', '--type'):
            keyword = arg
        if opt in '--lng1':
            lng1 = float(arg)
        if opt in '--lng2':
            lng2 = float(arg)
        if opt in '--lat1':
            lat1 = float(arg)
        if opt in '--lat2':
            lat2 = float(arg)
        if opt in ('-s', '--simplify'):
            simplify = True

    if lng1 is None or lat1 is None or lng2 is None or lat2 is None:
        print("缺少经纬度参数")
        sys.exit(1)

    if keyword is not None:
        search_res = search(keyword, lng1, lat1, lng2, lat2)
        print('> %s: %d' % (keyword, search_res['count']))
    else:
        go(lng1, lat1, lng2, lat2, simplify)

    return


if __name__ == '__main__':
    main(sys.argv[1:])
