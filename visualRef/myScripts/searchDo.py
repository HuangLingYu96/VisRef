from habanero import Crossref
from .sea import seaNode

#解析信息
def parseInfo(item):
    month_dict = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug',
                  '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    type_dict = {'journal-article': 'Journal Article', 'book-chapter': 'Chapter', 'standard': 'Standard',
                 'proceedings-article': 'Conference Paper', 'dataset': 'Dataset', 'report': 'Report',
                 'book': 'Book', 'component': 'Component', 'reference-entry': 'Entry',
                 'dissertation': 'Dissertation', 'other': 'Other', 'monograph': 'Monograph'}
    #doi
    try:
        tdoi=item['DOI']
        tlink=r'https://doi.org/'+tdoi
    except:
        tdoi='Unknown'
        tlink='Unknown'
    if(tdoi=='Unknown'):
        assert "doi unknown"
    tmp_node=seaNode(tdoi)
    try:
        tttype=item['type']
    except:
        tttype='Unknown'
    try:
        ttype=type_dict[tttype]
    except:
        ttype=tttype
    tmp_node.setType(ttype)
    try:
        time=item['created']['date-parts'][0]
        year=time[0]
        month=month_dict[str(time[1])]
        day=time[2]
        ttime=str(day)+' '+month+' '+str(year)
    except:
        ttime="Unknown"
    tmp_node.setYear(year)
    tmp_node.setTime(ttime)
    try:
        jouranls=item['short-container-title']
        tjournal=''
        for j in jouranls:
            tjournal=tjournal+j+' '
    except:
        tjournal='Unknown'
    tmp_node.setJournal(tjournal)
    try:
        tvolume=item['volume']
    except:
        tvolume='Unknown'
    tmp_node.setVolume(tvolume)
    try:
        tissue=item['issue']
    except:
        tissue='Unknown'
    tmp_node.setIssue(tissue)
    try:
        pages = item['page'].split('-')
        page_from=pages[0]
        page_to=pages[1]
    except:
        page_from = 'Unknown'
        page_to = 'Unknown'
    tmp_node.setPageFrom(page_from)
    tmp_node.setPageTo(page_to)
    try:
        titles=item['title']
        ttitle=''
        for t in titles:
            ttitle=ttitle+t+' '
    except:
        ttitle='Unknown'
    tmp_node.setTitle(ttitle)
    try:
        authors=item['author']
        tauhors='Authors: '
        for a in authors:
            tmp=','+a['given']+' '+a['family']
            tauhors=tauhors+tmp
        tauhors=tauhors.replace(',','',1)
    except:
        tauhors='Unknown'
    tmp_node.setAuthors(tauhors)
    return tmp_node

#写入字典
def writeInfo(tmp_node,target_dict):
    mark=r'"'+tmp_node.getDoi()+r'"'
    target_dict['mark']=mark
    target_dict['doi']=tmp_node.getDoi()
    target_dict['title']=tmp_node.getTitle()
    target_dict['type']=tmp_node.getType()
    target_dict['time']=tmp_node.getTime()
    target_dict['journal']=tmp_node.getJournal()
    target_dict['volume']=tmp_node.getVolume()
    target_dict['issue']=tmp_node.getIssue()
    target_dict['page_from']=tmp_node.getPageFrom()
    target_dict['page_to']=tmp_node.getPageTo()
    #target_dict['page_to'] = tmp_node.getPageTo()
    target_dict['author']=tmp_node.getAuthors()
    target_dict['link']=tmp_node.getLink()

def searchdo(keyword):
    cr=Crossref()
    result=cr.works(query=keyword)
    items = result['message']['items']
    results={'total':{},'year':{},'journal':{},'type':{}}
    for item in items:
        tmp_node=parseInfo(item)
        total_len=str(len(results['total']))
        results['total'][total_len]={}
        total_dict=results['total'][total_len]
        writeInfo(tmp_node,total_dict)
        tyear = tmp_node.getYear()
        tjournal = tmp_node.getJournal()
        ttype = tmp_node.getType()
        if(tyear not in results['year'].keys()):
            results['year'][tyear]={}
        year_len = str(len(results['year'][tyear]))
        results['year'][tyear][year_len] = {}
        year_dict = results['year'][tyear][year_len]
        writeInfo(tmp_node, year_dict)

        if(tjournal not in results['journal'].keys()):
            results['journal'][tjournal]={}
        journal_len=str(len(results['journal'][tjournal]))
        results['journal'][tjournal][journal_len]={}
        journal_dict=results['journal'][tjournal][journal_len]
        writeInfo(tmp_node,journal_dict)

        if(ttype not in results['type'].keys()):
            results['type'][ttype]={}
        type_len=str(len(results['type'][ttype]))
        results['type'][ttype][type_len]={}
        type_dict=results['type'][ttype][type_len]
        writeInfo(tmp_node,type_dict)

    #print(len(result_list))
    #print(len(year_dict))
    #print(len(journal_dict))
    return results