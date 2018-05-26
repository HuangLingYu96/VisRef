import urllib.request
import urllib.parse
import json
import os
from datetime import datetime
from . import infoDo

def citdo(date,title,cited,cit_file_id):
    time1=datetime.now()
    cit_result={'summary':{},
                'details':{}}
    cited_count=int(cited)
    params={'query.bibliographic':title,
            'rows':min(500,cited_count),
            'sort':'is-referenced-by-count',
            'order':'desc'}
    url_params=urllib.parse.urlencode(params)
    #url=r'https://api.crossref.org/works?filter=has-references:true,from-pub-date:'+date+'&'+url_params
    #处理date，必须是yyyy-mm-dd格式
    date_array=date.split('-')

    d_year=int(date_array[0])
    for i in range(d_year,2019):
        cit_result['summary'][str(i)]={'cited':0,'total':0}

    if(len(date_array)>=2):
        m=len(date_array)
        for i in range(1,m):
            temp=int(date_array[i])
            if(int(temp/10)==0):date_array[i]='0'+str(temp)
    date=''
    for j in date_array:
        date+='-'+j
    date=date.replace('-','',1)
    url = r'https://api.crossref.org/works?filter=has-references:true,from-pub-date:' + date + '&' + url_params
    html=urllib.request.urlopen(url)
    hjson=json.loads(html.read())
    print('数据源连接成功')
    items=hjson['message']['items']
    for item in items:
        result=infoDo.parse_info(item)
        time=result['time']
        info=result['author']+' - '+result['container_title']
        year=time.split('-')[0]
        d_info = {'doi':result['doi'],'title': result['title'], 'year': year, 'cited': result['is_referenced_by_count'], 'info': info,
                  'author':result['author'],'journal':result['container_title']}
        cit_result['details'][len(cit_result['details'])]=d_info
        if(year!='Unknown'):
            cit_result['summary'][year]['cited']+=1
    for i in range(d_year, 2019):
        if(i==d_year):
            cit_result['summary'][str(i)]['total']=cit_result['summary'][str(i)]['cited']
        else:
            cit_result['summary'][str(i)]['total']=cit_result['summary'][str(i-1)]['total']+cit_result['summary'][str(i)]['cited']

    path=os.getcwd() + '\\media\\cit\\' + str(cit_file_id) + '.json'
    with open(path, "w", encoding='utf-8')as f:
        f.write(json.dumps(cit_result, ensure_ascii=False))
        print('cit文件保存成功')
        time2=datetime.now()
        print('cit综合耗时 %s'%(time2-time1))
