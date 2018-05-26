from crossref.restful import Works

#解析详细信息
def parse_info(doi,item):
    link='https://doi.org/' + doi
    info={'doi':doi,
          'link':link}
    #wk=Works()
    #item=wk.doi(doi)
    #title
    try:
        title=''
        t=item['title']
        for i in t:
            title=title+i
        if(title==''):
            title='Unknown'
        info['title']=title
    except:
        print('Title is unknown: '+doi)
    #publisher
    try:
        publisher=''
        p=item['container-title']
        for i in p:
            publisher=publisher+i
        if(publisher==''):
            publisher='Unknown'
        info['publisher']=publisher
    except:
        print('Publisher is unknown: '+doi)
    #date
    try:
        date = item['created']['date-time'].replace('T', ' ')
        date = date.replace('Z', '')
        info['date']=date
    except:
        print("Date is unknown: " + doi)
    #cited
    try:
        info['cited']=str(item['is-referenced-by-count'])
    except:
        print("Citation is unknown: " + doi)
    #author
    try:
        author_list=''
        authors = item['author']
        for a in authors:
            author = ''
            try:
                author=author+a['given']+' '
            except:
                print('author given is lost: '+doi)
            try:
                author=author+a['family']
            except:
                print('author family is lost: '+doi)
            author_list=author_list+r','+author
        if(author_list==''):
            author_list='Unknown'
        author_list = author_list.replace(',', '', 1)
        if(author_list==''):
            author_list='Unknown'
        info['author']=author_list
    except:
        print("Author is unknown: " + doi)
    #subject
    try:
        subject_list = ''
        subjects = item['subject']
        for s in subjects:
            subject_list = subject_list + "," + s
        subject_list = subject_list.replace(',', '', 1)
        if(subject_list==''):
            subject_list='Unknown'
        info['subject']=subject_list
    except:
        print("Subject is unknown: " + doi)
    return info