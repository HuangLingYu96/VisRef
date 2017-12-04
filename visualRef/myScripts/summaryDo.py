from habanero import Crossref
from crossref.restful import Works
import re
import os
import json
import time
import urllib.request
from selenium import webdriver
from .parseInfo import parse_info
#from .citDo import is_element_exist

def summarydo(doi):
    summary_file={
        'info':{},
        'cit':{},
        'ref':{}
    }
    wk=Works()
    item=wk.doi(doi)
    info=parse_info(doi,item)
    summary_file['info']=info
    print('info is ok')

    works=Works()
    item=works.doi(doi)
    if ('reference' in item.keys()):
        references = item['reference']
        for reference in references:
            if ('DOI' in reference.keys()):
                ref_doi = reference['DOI']
                summary_file['ref'][ref_doi]={}
                wk=Works()
                ref_item=wk.doi(ref_doi)
                ref_info=parse_info(ref_doi,ref_item)
                summary_file['ref'][ref_doi]=ref_info
    else:
        print("无引用信息"+doi)
    print('ref is ok')

    web_url = r'http://xueshu.baidu.com/s?wd=' + doi \
              + r'&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2'

    res = urllib.request.urlopen(web_url)
    html = res.read().decode('utf-8')
    matchObj = re.findall('lineMapCitedData = \[(.*)\]', html, re.M | re.I)
    try:
        cited = re.findall('"cited":([^,]+)', matchObj[0], re.M | re.I)
        year = re.findall('"year":([^\}]+)', matchObj[0], re.M | re.I)
        total = re.findall('"total":([^,]+)', matchObj[0], re.M | re.I)
        length=len(cited)
        for i in range(0,length):
            ctmp=cited[i].replace('"','')
            ctmp=int(ctmp)
            ttmp=total[i].replace('"','')
            ttmp=int(ttmp)
            summary_file['cit'][year[i]]={'cited':ctmp,'total':ttmp}
        print('cit is ok')
    except:
        print('baidu未收录cit信息')

    currentPath = os.getcwd() + '\\media\\sum\\'
    json_output = currentPath + doi.replace("/", "_") + ".json"
    with open(json_output, "w", encoding='utf-8') as f:
        f.write(json.dumps(summary_file, ensure_ascii=False))
        # json.dump(json_file, f)
    print("加载入json文件完成...")
    #driver.close()