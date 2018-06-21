
# 함수 내 Exception 이 발생할 경우 try 구문만 전체가 수행되지 않는 것이 아니고
# Exception 발생 이후의 문장만 실행이 되지 않는 것이고
# pass 라는 문장은 제어문이나 구문내에 exception 자체만 pass 한다는 것이다.

def f():
    try:
        a = None
        a.string
        a = 40
        return a
    except AttributeError as aE:
        pass
    print(a)
    a = 30
    return a

b = f()

print(b)