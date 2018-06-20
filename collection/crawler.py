from urllib.request import Request, urlopen
from datetime import datetime

import sys

# def my_error(e):
#     print('my error : ', str(e))
# def error(e):
#     print('%s : %s' % (e, datetime.now()), file=sys.stdarr)

def crawling(
        url='',
        encoding='utf-8',
        # proc = None,
        proc = lambda html:html,
        store = lambda html:html,
        err=lambda e:print('%s : %s' % (e, datetime.now()), file=sys.stdarr)):
    try:
        request = Request(url)
        resp = urlopen(request)

        try:
            receive = resp.read()
            store = store(proc(receive.decode(encoding)))
            # result = receive.decode(encoding)
            # result = proc(result)

        except UnicodeDecodeError as uE:
            result = resp.read().decode(encoding, 'replace')

        return result
    except Exception as e:
        err(e)