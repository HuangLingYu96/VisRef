from crossref.restful import Works

def parse_result(keyword,item):
    month_dict = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug',
                  '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    type_dict = {'journal-article': 'Journal Article', 'book-chapter': 'Chapter', 'standard': 'Standard',
                 'proceedings-article': 'Conference Paper', 'dataset': 'Dataset', 'report': 'Report',
                 'book': 'Book', 'component': 'Component', 'reference-entry': 'Entry',
                 'dissertation': 'Dissertation', 'other': 'Other', 'monograph': 'Monograph'}
    result={}
    # doi
    try:
        doi = item['DOI']
        link = r'https://doi.org/' + doi
    except:
        doi = 'Unknown'
        link = 'Unknown'
    if(doi==''):
        doi='Unknown'
        link = 'Unknown'
    result['doi']=doi
    result['link']=link
    #type
    try:
        j_type=item['type']
    except:
        j_type='Unknown'
    try:
        journal_type=type_dict[j_type]
    except:
        journal_type='Other'
    result['sea_type']=journal_type
    #time
    try:
        time = item['indexed']['date-parts'][0]
        year = str(time[0])
        if(len(time)==3):
            month = month_dict[str(time[1])]
            day = str(time[2])
            time_info = str(day) + ' ' + month + ' ' + str(year)
        elif(len(time)==2):
            month = month_dict[str(time[1])]
            time_info = month + ' ' + str(year)
        else:
            time_info=str(year)
    except:
        time_info = "Unknown"
    result['time']=time_info
    #publisher
    try:
        jouranls=item['short-container-title']
        publisher=''
        for j in jouranls:
            publisher=publisher+j+' '
    except:
        publisher='Unknown'
    result['publisher']=publisher
    #volume
    try:
        volume=str(item['volume'])
    except:
        volume='Unknown'
    result['volume']=volume
    #issue
    try:
        issue=item['issue']
    except:
        issue='Unknown'
    result['issue']=issue
    #page
    try:
        pages = item['page'].split('-')
        page_from=pages[0]
        page_to=pages[1]
    except:
        page_from = 'Unknown'
        page_to = 'Unknown'
    result['page_from']=page_from
    result['page_to']=page_to
    #title
    try:
        titles=item['title']
        title=''
        for t in titles:
            title=title+t+' '
    except:
        title='Unknown'
    result['title']=title
    #author
    try:
        authors=item['author']
        authors=''
        for a in authors:
            tmp=','+a['given']+' '+a['family']
            authors=authors+tmp
        authors=authors.replace(',','',1)
    except:
        authors='Unknown'
    result['author']=authors
    result['keyword']=keyword
    return result

'''
def searchdo(keyword):
    works = Works()
    w1 = works.query(title=keyword)
    results={}

    for index,item in enumerate(w1):
        if(index>0):
            break
        result=parse_result(item)
        l=len(results)
        results[l]=result
        #print(result)
        #print(item)
    return results
'''