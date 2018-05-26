from crossref.restful import Works
import json

#解析文献原始信息
def parse_info(item):
    result={}
    # doi
    try:doi = item['DOI']
    except:doi = 'Unknown'
    result['doi'] = doi
    # link
    try:link = item['URL']
    except:link = 'Unknown'
    result['link'] = link
    # publisher
    try:
        container_title = item['container-title'][0]
    except:
        container_title = 'Unknown'
    result['container_title'] = container_title
    # type
    try:d_type = item['type']
    except:d_type = 'Unknown'
    result['type'] = d_type
    # title
    try:title = item['title'][0]
    except: title = 'Unknown'
    result['title'] = title
    # time
    try:
        times = item['published-print']['date-parts'][0]
        d_time = ''
        for t in times:
            d_time += '-' + str(t)
        d_time = d_time.replace('-', '', 1)
    except:
        d_time = 'Unknown'
    result['time'] = d_time
    # page
    try:page = item['page']
    except:page = 'Unknown'
    result['page'] = page
    # author
    try:
        authors = item['author']
        author = ''
        if (len(authors) > 3):
            m = 3
        else:
            m = len(authors)
        for i in range(m):
            temp = ''
            if ('given' in authors[i].keys()):
                temp += authors[i]['given']
                temp += ' '
            if ('family' in authors[i].keys()): temp += authors[i]['family']
            author += ', '
            author += temp
        author = author.replace(' ', '', 1)
        author = author.replace(',', '', 1)
    except:
        author = 'Unknown'
    result['author'] = author
    # is-referenced-by-count
    try:
        cited = str(item['is-referenced-by-count'])
    except:
        cited = 'Unknown'
    result['is_referenced_by_count'] = cited
    #reference_count
    try:reference_count=str(item['reference-count'])
    except:reference_count='Unknown'
    result['reference_count']=reference_count
    return result
