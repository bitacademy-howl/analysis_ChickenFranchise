gungu_alias = '''
금남면:세종시 부강면:세종시 연서면:세종시 장군면:세종시
전동면:세종시
'''

gungu_dict = dict()
for aliasset in gungu_alias.split():
    s = aliasset.split(':')
    gungu_dict.update({s[0]: s[1]})

print(gungu_dict)

b = '금남면'
c = '신라면'

# dict 셀프를 명시해주면 key가 존재할때는 값을 반환하고
# 키가 존재하지않으면 그냥 자기자신을 반환하도록 한다.
a = gungu_dict.get(b, b)
print(a)

a = gungu_dict.get(c, c)
print(a)

# table['sido'] = table.sido.apply()
# [['안녕', '하이', '010-1111-1111'], ['안녕', '하이', '010-1111-1111'], ('안녕1', '하이1', '010-1111-1111')]