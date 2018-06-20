from collection.crawler import crawling

def proc(html):
    print('Processing...' + html)

def store(result):
    pass

# result = crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
#                   encoding='cp949',
#                   proc=proc(),
#                   store=store())
result = crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
                  encoding='cp949')
proc(result)