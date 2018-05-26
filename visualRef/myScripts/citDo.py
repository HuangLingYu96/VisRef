from selenium import webdriver
import time
import json
import os
import re
from datetime import datetime
from . import parseInfo
from . import titleToDoi
from crossref.restful import Works
import urllib.request

#判断元素是否存在于html中
def is_element_exist(element,container):
    try:
        container.find_element_by_class_name(element)
        return True
    except:
        return False

def citdo(start_doi,file_id):
    start_time=datetime.now()
    # 存入json文件
    cit_file = {'info': {},
                 'summary':{},
                 'details':{}
                 }
    #记录百度是否收录信息的flag,收藏为1，未收藏为0
    flag=1
    wk=Works()
    item=wk.doi(start_doi)
    info=parseInfo.parse_info(start_doi,item)
    cit_file['info']=info
    print('info is ok')

    web_url = r'http://xueshu.baidu.com/s?wd=' + start_doi \
              + r'&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=2'

    res = urllib.request.urlopen(web_url)
    html = res.read().decode('utf-8')
    matchObj = re.findall('lineMapCitedData = \[(.*)\]', html, re.M | re.I)
    try:
        cited = re.findall('"cited":([^,]+)', matchObj[0], re.M | re.I)
        year = re.findall('"year":([^\}]+)', matchObj[0], re.M | re.I)
        total = re.findall('"total":([^,]+)', matchObj[0], re.M | re.I)
        length = len(cited)
        for i in range(0, length):
            ctmp = cited[i].replace('"', '')
            ctmp = int(ctmp)
            ttmp = total[i].replace('"', '')
            ttmp = int(ttmp)
            cit_file['summary'][year[i]] = {'cited': ctmp, 'total': ttmp}
        print('sum-cit is ok')
    except:
        flag=0
        print('baidu未收录cit信息')

    if(flag==1):
        path = r'D:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe'
        driver = webdriver.PhantomJS(executable_path=path)
        driver.get(web_url)
        print('ok')
        click_count=0
        start = datetime.now()
        # 获得引用，先全部加载，再爬取信息
        morebtn = r'dl_more'  # 加载更多的按钮
        container = driver.find_element_by_class_name('con_citation')
        # 全部加载
        while (is_element_exist(morebtn, container) and click_count<4):
            container = driver.find_element_by_class_name('con_citation')
            getMorebtn = container.find_element_by_class_name(morebtn)
            try:
                getMorebtn.click()
                click_count+=1
                time.sleep(5)
            except:
                break
        print('加载完成')
        #print("2耗时%s : " % (datetime.now() - start))

        # 获取信息
        if (is_element_exist('citation_lists', container)):
            citation_list = driver.find_element_by_class_name('citation_lists')
            citation_terms = citation_list.find_elements_by_tag_name('li')

            for term in citation_terms:
                # title
                try:
                    title = term.find_element_by_class_name('relative_title').text
                except:
                    title = 'Unknown'
                if(title!='Unknown'):
                    doi=titleToDoi.titletodoi(title)
                # year
                try:
                    year = term.find_element_by_class_name('sc_year').text
                except:
                    year = 'Unknown'
                if (year == ' '):
                    year = 'Unknown'
                # 被引量，cited
                try:
                    cited = term.find_element_by_class_name('sc_cited').text
                    cited = cited.split(': ')
                    ncited = cited[1]
                except:
                    ncited = 'Unknown'
                # info
                try:
                    sc_info = term.find_element_by_class_name('sc_info')
                    tmp_info = sc_info.find_element_by_tag_name('p')
                    info = tmp_info.text
                except:
                    info = 'Unknown'
                d_info={'title':title,'year':year,'cited':ncited,'info':info}
                if(doi!='None'):
                    d_info['doi']=doi
                l=len(cit_file['details'])
                cit_file['details'][l]=d_info

    currentPath = os.getcwd() + '\\media\\cit\\'
    filename=str(file_id)
    json_output = currentPath + filename + ".json"
    #json_output = r'E://graduation_test//' + start_doi.replace("/", "+") + ".json"
    with open(json_output, "w", encoding='utf-8') as f:
        f.write(json.dumps(cit_file, ensure_ascii=False))
        # json.dump(json_file, f)
    print("加载入json文件完成...")
    end_time=datetime.now()
    print("总耗时 %s"%(end_time-start_time))
    if(flag==1):
        driver.close()