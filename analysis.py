import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def showmap(blockedmap, targetdata, title, color):
    pass

# pelicana
# pelicana_table = pd.DataFrame.from_csv('__result__/pelicana_table.csv',
#                                        encoding='utf-8',
#                                        index_col=0,
#                                        header=0).fillna('')
pelicana_table = pd.read_csv('__result__/pelicana_table.csv',
                                       encoding='utf-8',
                                       index_col=1,
                                       header=0).fillna('')


# print(pelicana_table)
pelicana_table = pelicana_table[pelicana_table.sido != '']
pelicana_table = pelicana_table[pelicana_table.gungu != '']
# print(pelicana_table)
# pelicana_table.apply(lambda v:print(v), axis=1)

# # 시리즈로 생성
# series1 = pelicana_table.apply(lambda r:r['sido'] + ' ' + r['gungu'], axis=1)
# print(series1)
#
# # 생성된 시리즈로 값을 카운트 하기 위한 과정
# series2 = series1.value_counts()
# print(series2)

# 위의 두 과정을 코드 한줄로 요약해서 사용하자.
# 시군구 별 매장의 수
pelicana_count = pelicana_table.apply(lambda r:str(r['sido']) + ' ' + str(r['gungu']), axis=1).value_counts()
# print(pelicana_count)

# print(pelicana_table)

# nene
nene_table = pd.read_csv('__result__/nene_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('')
nene_table = nene_table[nene_table.sido != '']
nene_table = nene_table[nene_table.gungu != '']

# 시군구 별 매장의 수
nene_count = nene_table.apply(lambda r:str(r['sido']) + ' ' + str(r['gungu']), axis=1).value_counts()
# print(nene_count)

# kyochon
kyochon_table = pd.read_csv('__result__/kyochon_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('')
kyochon_table = kyochon_table[kyochon_table.sido != '']
kyochon_table = kyochon_table[kyochon_table.gungu != '']

# 시군구 별 매장의 수
kyochon_count = kyochon_table.apply(lambda r:str(r['sido']) + ' ' + str(r['gungu']), axis=1).value_counts()
# print(kyochon_count)

# goobne
goobne_table = pd.read_csv('__result__/goobne_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('')
goobne_table = goobne_table[goobne_table.sido != '']
goobne_table = goobne_table[goobne_table.gungu != '']

# 시군구 별 매장의 수
goobne_count = goobne_table.apply(lambda r:str(r['sido']) + ' ' + str(r['gungu']), axis=1).value_counts()
# print(goobne_count)


# merge_dict = {'pelicana' : pelicana_count, 'nene' : nene_count, 'kyochon': kyochon_count, 'goobne' : goobne_count}
# chicken_table = pd.DataFrame(merge_dict)
chicken_table = pd.DataFrame({'pelicana' : pelicana_count, 'nene' : nene_count, 'kyochon': kyochon_count, 'goobne' : goobne_count}).fillna(0)
# print(chicken_table[chicken_table.index == '00 18'].index)
chicken_table = chicken_table.drop(chicken_table[chicken_table.index == '00 18'].index)
chicken_table = chicken_table.drop(chicken_table[chicken_table.index == '테스트 테스트구'].index)

# print(chicken_table)

chicken_sum_table = chicken_table.sum(axis=0)

'''
plt.figure()
chicken_sum_table.plot(kind='bar')
plt.show()

print(chicken_sum_table, type(chicken_sum_table))
'''

data_draw_korea = pd.read_csv('data_draw_korea.csv', index_col=0, encoding='utf-8')
# print(data_draw_korea)
data_draw_korea.index = data_draw_korea.apply(lambda r:r['광역시도'] + ' ' +  r['행정구역'], axis=1)

chicken_merge = pd.merge(data_draw_korea, chicken_table, how='outer', left_index=True, right_index=True)

chicken_merge['total'] = chicken_table.sum(axis=1)
# print(data_draw_korea)

showmap(chicken_merge, 'pelicana', '페리카나 매장 분포', 'Blues')
print(chicken_merge)