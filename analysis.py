import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def showmap(blockedmap, targetdata, title, color):

    BORDER_LINES = [
        [(3, 2), (5, 2), (5, 3), (9, 3), (9, 1)],  # 인천
        [(2, 5), (3, 5), (3, 4), (8, 4), (8, 7), (7, 7), (7, 9), (4, 9), (4, 7), (1, 7)],  # 서울
        [(1, 6), (1, 9), (3, 9), (3, 10), (8, 10), (8, 9),
         (9, 9), (9, 8), (10, 8), (10, 5), (9, 5), (9, 3)],  # 경기도
        [(9, 12), (9, 10), (8, 10)],  # 강원도
        [(10, 5), (11, 5), (11, 4), (12, 4), (12, 5), (13, 5),
         (13, 4), (14, 4), (14, 2)],  # 충청남도
        [(11, 5), (12, 5), (12, 6), (15, 6), (15, 7), (13, 7),
         (13, 8), (11, 8), (11, 9), (10, 9), (10, 8)],  # 충청북도
        [(14, 4), (15, 4), (15, 6)],  # 대전시
        [(14, 7), (14, 9), (13, 9), (13, 11), (13, 13)],  # 경상북도
        [(14, 8), (16, 8), (16, 10), (15, 10),
         (15, 11), (14, 11), (14, 12), (13, 12)],  # 대구시
        [(15, 11), (16, 11), (16, 13)],  # 울산시
        [(17, 1), (17, 3), (18, 3), (18, 6), (15, 6)],  # 전라북도
        [(19, 2), (19, 4), (21, 4), (21, 3), (22, 3), (22, 2), (19, 2)],  # 광주시
        [(18, 5), (20, 5), (20, 6)],  # 전라남도
        [(16, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10)],  # 부산시
    ]

    whitelabelmin = (max(blockedmap[targetdata]) - min(blockedmap[targetdata])) * 0.25 + min(blockedmap[targetdata])

    vmin = min(blockedmap[targetdata])
    vmax = max(blockedmap[targetdata])
    mapdata = blockedmap.pivot(index='y', columns='x', values=targetdata)
    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
    cmapname = color
    plt.figure(figsize=(8, 13))
    plt.title(title)
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname, edgecolor='#aaaaaa', linewidth=0.5)
    for idx, row in blockedmap.iterrows():
        annocolor = 'white' if row[targetdata] > whitelabelmin else 'black'
        dispname = row['shortName']

        # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 7.5, 1.5
        else:
            fontsize, linespacing = 11, 1.2

        plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                     fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)

    for path in BORDER_LINES:
        ys, xs = zip(*path)
        plt.plot(xs, ys, c='black', lw=4)

    plt.gca().invert_yaxis()
    plt.axis('off')

    cb = plt.colorbar(shrink=.1, aspect=10)
    cb.set_label(targetdata)
    plt.tight_layout()

#    plt.savefig('d:/temp/chicken_data/' + targetdata + '.png')

    plt.show()

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

# Nan 데이터의 삭제
chicken_merge = chicken_merge[ ~np.isnan(chicken_merge['면적'])]

# 총 매장의 수
# print(chicken_table.sum(axis=1))

chicken_merge['total'] = chicken_table.sum(axis=1)
chicken_merge = chicken_merge[ ~np.isnan(chicken_merge['total'])]
showmap(chicken_merge, 'total', '4개 치킨 프렌차이즈 전국 매장 분포', 'Greens')

# 인구 만명당 치킨 집 수
chicken_merge['total10k'] = chicken_merge['total'] / chicken_merge['인구수'] * 10000
showmap(chicken_merge, 'total10k', '인구 만명 당 치킨집 수', 'RdPu')

# 면적 당 치킨집 수
chicken_merge['area'] = chicken_merge['total'] / chicken_merge['면적']
showmap(chicken_merge, 'area', '면적 당 치킨집 수', 'Purples')

# 페리카나 매장 분포
showmap(chicken_merge, 'pelicana', '페리카나 매장 분포', 'Blues')

# 네네 매장 분포
showmap(chicken_merge, 'nene', '네네 매장 분포', 'Greys')

# 굽네 매장 분포
showmap(chicken_merge, 'goobne', '굽네 매장 분포', 'Reds')

# 교촌 매장 분포
showmap(chicken_merge, 'kyochon', '교촌 매장 분포', 'Oranges')