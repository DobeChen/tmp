import requests
import json
import time

COMIC_NAMES = ['海贼王', '银魂', '镖人', '怪物事变', '土气的我和奇怪的大叔', '町田君的世界', '官能先生', 'DOG END',
               '行星Closet', '人面', '一拳超人', '汤神君没有朋友', 'MY HOME HERO', '约定的梦幻岛', '五百年之箱',
               '恋情浪人', '致不灭的你', 'BLUE GIANT', '血之辙', '黑社会的超能力女儿', '卫府之七忍', '有害指定同级生',
               '高分少女', '新撰组镇魂歌', '不良出身', '白银之匙', '涩谷金鱼', '苏醒&沉睡']

SEARCH_COMIC_PATH = 'http://s.acg.dmzj.com/comicsum/search.php'
SEARCH_BASE_URL = 'http://v2.api.dmzj.com/'
SEARCH_CHAPTER_URL = SEARCH_BASE_URL + 'comic/'
PATH_PARAM = '.json?channel=Android&version=2.7.003'


def common_search(url, pars, has_header):
    if has_header:
        response = requests.request('GET', url, headers=pars)
    else:
        if len(pars):
            response = requests.get(url, pars)
        else:
            response = requests.get(url)

    status_code = response.status_code

    if 200 != status_code:
        return ''
    return response


def search_comic(url, pars, has_header):
    comic_names = ''

    response = common_search(url, pars, has_header)
    if response != '':
        try:
            content = response.text

            start_index = content.find('[')
            end_index = content.rfind(']')
            if (end_index - start_index) == 1:
                return ''

            data = content[start_index: end_index + 1]
            comic_names = data
        except Exception as error:
            print(error)

    return comic_names


def search_chapter(url, pars, has_header):
    chapters = ''

    response = common_search(url, pars, has_header)
    if response != '':
        try:
            content = response.text
            chapters = content
        except Exception as error:
            print(error)

    return chapters


def trans_comic_data(comic_data):
    return json.loads(comic_data)


def trans_chapter_data(chapter_data):
    data = json.loads(chapter_data)
    update_time = data['last_updatetime']
    return update_time


def cmp(data1, data2):
    return data1 > data2


def main():
    print('Length is ' + str(len(COMIC_NAMES)))
    try:
        comic_time = {}
        for name in COMIC_NAMES:
            params = {'s': name}
            comic_name = search_comic(SEARCH_COMIC_PATH, params, False)
            if comic_name == '':
                print('No this comic, place try again.')

            # comic find result
            data_list = trans_comic_data(comic_name)
            choose_num = 0
            for i in range(len(data_list)):
                data = data_list[i]
                if name == data['name']:
                    choose_num = i
                    break

            choose_comic = data_list[choose_num]
            comic_id = str(choose_comic['id'])
            search_chapter_path = SEARCH_CHAPTER_URL + comic_id + PATH_PARAM

            # chapters find result
            chapter_data = search_chapter(search_chapter_path, {}, False)
            update_time = trans_chapter_data(chapter_data)
            comic_time[name] = update_time

        sort_list = sorted(comic_time.items(), key=lambda d: d[1], reverse=True)
        for data in sort_list:
            date = time.localtime(data[1])
            date_format = time.strftime('%Y-%m-%d', date)
            print(data[0] + ' ---> ' + date_format)
        print('Sort list is ' + str(len(sort_list)))

    except Exception as error:
        print(error)
        print('try again')

main()