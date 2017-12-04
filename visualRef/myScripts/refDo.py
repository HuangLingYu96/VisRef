from crossref.restful import Works
from queue import Queue
import threading
import os
import time
import json
from datetime import datetime
from .import parseInfo

#解析引用
def parse_ref(item,cat,doi,ref_file,doi_queue):
    if ('reference' in item.keys()):
        references = item['reference']
        for reference in references:
            if ('DOI' in reference.keys()):
                ref_doi = reference['DOI']
                edge={'source':doi,'target':ref_doi}
                length=len(ref_file['edges'])
                ref_file['edges'][length]=edge
                pcd_doi=ref_doi+'+'+str(cat+1)
                doi_queue.put(pcd_doi)
    else:
        print(doi + '没有引用信息')

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
                #node=refNode(doi,cat)
                try:
                    wk = Works()
                    item = wk.doi(doi)
                except:
                    print('网络状态不良好' + doi + '请求失败')
                    item = 'network-error'
                if(item==None):
                    print(doi+'crossref未收录该doi')
                    item='doi-error'
                if(item!='network-error' and item!='doi-error'):
                    info=parseInfo.parse_info(doi=doi,item=item)
                    #subject_list=info['subject'].split(',')
                    self.lock.acquire()
                    if('subject' in info.keys()):
                        subject_list = info['subject'].split(',')
                        for s in subject_list:
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

def refdo(start_doi):
    '''
    ref_file = {'info': {},
                'nodes': {},
                'edges': {},
                'subjectCount':0,
                'count': {},
                'subject': {}}
    '''
    ref_file = {'info': {},
                'nodes': {},
                'edges': {},
                'statistics':{'subjectCount':0,
                                'count':{},
                                'subject':{}}}
    #start_doi = '10.1007/s10495-016-1250-5'
    start_cat = 0
    doi_queue = Queue()
    # node_queue=Queue()
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
    json_output = currentPath + start_doi.replace("/", "_") + ".json"
    with open(json_output, "w") as f:
        json.dump(ref_file, f)
    print("加载入文件完成...")

