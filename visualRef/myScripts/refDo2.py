from crossref.restful import Works
from queue import Queue
import threading
import os
import time
import json
import urllib.request
import urllib.parse
from datetime import datetime
from . import parseInfo
from . import infoDo

#解析引用
def parse_ref(item,cat,doi,ref_file,doi_queue):
    if ('reference' in item.keys()):
        references = item['reference']
        if(len(references)>50 & cat>0):
            print(doi+'参考信息大于50')
        else:
            for reference in references:
                if ('DOI' in reference.keys()):
                    ref_doi = reference['DOI']
                    edge={'source':doi,'target':ref_doi}
                    length=len(ref_file['edges'])
                    ref_file['edges'][length]=edge
                    pcd_doi=ref_doi+'+'+str(cat+1)
                    doi_queue.put(pcd_doi)
            print(doi + '参考信息解析成功')
    else:
        print(doi + '没有参考信息')

#爬取引用
class refCrawl(threading.Thread):
    def __init__(self,doi_queue,ref_file,file_lock):
        threading.Thread.__init__(self)
        self.doi_queue=doi_queue
        self.ref_file=ref_file
        self.lock=file_lock

    def run(self):
        while True:
            if(self.doi_queue.empty()==False):
                tmp=self.doi_queue.get()
                doi=tmp.split('+')[0]
                cat=int(tmp.split('+')[1])
                url = r'https://api.crossref.org/works/' + doi
                try:
                    html = urllib.request.urlopen(url)
                    hjson = json.loads(html.read())
                    item=hjson['message']
                except:
                    print('doi: '+doi+'输入错误')
                    item = 'doi-error'
                if(type(item)==dict):
                    #info=parseInfo.parse_info(doi=doi,item=item)
                    #info=infoDo.parse_info(item)
                    result=infoDo.parse_info(item)
                    info={
                        'doi':result['doi'],
                        'link':result['link'],
                        'title':result['title'],
                        'publisher':result['container_title'],
                        'date':result['time'],
                        'cited':result['is_referenced_by_count'],
                        'author':result['author'],
                        'subject':result['reference_count']
                    }
                    print(doi+'基本信息解析成功')
                    self.lock.acquire()
                    if(info['publisher']!='Unknown'):
                        s=info['publisher']
                        #记录和统计subject信息
                        #由于subject数据取消，改成journal统计
                        #subjectCount: 不同的journal数量
                        #count: 统计每一个journal有多少文献
                        #subject: 统计每一个journal下的文献
                        if(s in self.ref_file['statistics']['subject'].keys()):
                            self.ref_file['statistics']['count'][s]+=1
                            l=len(self.ref_file['statistics']['subject'][s])
                            self.ref_file['statistics']['subject'][s][l]=info
                        else:
                            self.ref_file['statistics']['subjectCount']+=1
                            self.ref_file['statistics']['count'][s]=1
                            self.ref_file['statistics']['subject'][s]={}
                            l = len(self.ref_file['statistics']['subject'][s])
                            self.ref_file['statistics']['subject'][s][l] = info
                    self.lock.release()
                    if(cat==0):
                        self.ref_file['info']=info
                    else:
                        length=len(self.ref_file['nodes'])
                        info['cat'] = cat
                        self.ref_file['nodes'][length]=info

                    if(cat<2):
                        parse_ref(item,cat,doi,self.ref_file,self.doi_queue)
                self.doi_queue.task_done()

def refdo(start_doi,file_id):
    ref_file = {'info': {},
                'nodes': {},
                'edges': {},
                'statistics':{'subjectCount':0,
                                'count':{},
                                'subject':{}}}
    start_cat = 0
    doi_queue = Queue()
    pcd_start_doi = start_doi + '+' + str(start_cat)
    doi_queue.put(pcd_start_doi)
    file_lock=threading.Lock()
    start_time=datetime.now()
    print('start')
    for i in range(10):
        t = refCrawl(doi_queue,ref_file,file_lock)
        t.setDaemon(True)
        t.start()
    doi_queue.join()
    print('ok')
    end_time=datetime.now()
    crawl_time=end_time-start_time
    print('crawl耗时: %s'%crawl_time)

    currentPath = os.getcwd() + '\\media\\ref\\'
    filename=str(file_id)
    json_output = currentPath + filename + ".json"
    with open(json_output, "w") as f:
        json.dump(ref_file, f)
    print("加载入文件完成...")


