from habanero import Crossref
import re

def titletodoi(keyword):
    cr = Crossref()
    result = cr.works(query=keyword)
    items = result['message']['items']
    item_title = items[0]['title']
    tmp = ''
    for it in item_title:
        tmp += it
    title = keyword.replace(' ', '').lower()
    title = re.sub(r'\W', '', title)
    # print('title: ' + title)
    tmp = tmp.replace(' ', '').lower()
    tmp = re.sub(r'\W', '', tmp)
    # print('tmp: ' + tmp)
    flag='no'
    if (title == tmp):
        flag='yes'
    else:
        if (title in tmp):
            flag = 'yes'
        elif (tmp in title):
            flag = 'yes'
        else:
            flag = 'no'
    if(flag=='yes'):
        doi=items[0]['DOI']
        return doi
    else:
        return 'None'