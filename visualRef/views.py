from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import json
import re
from crossref.restful import Works
from datetime import datetime

from .form import rForm
from .form import lForm
from .models import Ref
from .models import Cit
from .models import Sum
from .models import Star
from .myScripts import refDo
from .myScripts import citDo
from .myScripts import summaryDo
from .myScripts import searchDo
from .myScripts import titleToDoi
from .myScripts import parseInfo

# Create your views here.
#首页
def home(request):
    context={}
    return render(request,'home.html',context)

#search
def search(request):
    keyword = request.GET.get('search')
    category = request.GET.get('cat')
    selector = request.GET.get('sel')
    if(str(keyword)=='None'):
        return render(request,'search.html',{})
    else:
        results = searchDo.searchdo(keyword)
        if (str(category) == 'None'):
            total = results['total']
            return render(request, 'search.html', {'all': results, 'results': total, 'keyword': keyword})
        else:
            # print(results[category][selector])
            if (category == 'year'):
                selector = int(selector)
            if (category == 'journal' and selector != 'Unknown'):
                selector = selector + ' '
            select = results[category][selector]
            return render(request, 'search.html', {'all': results, 'results': select, 'keyword': keyword})

#可视化
def vis(request):
    return render(request,'visualization.html',{'start':'yes'})

#ref可视化
def vis_ref(request):
    keyword = request.POST.get('keyword')
    p = r'^10\.[\w]+\/[\w]+'
    pattern = re.compile(p)
    signal = 'yes'
    if (pattern.match(keyword)):
        ref_doi = keyword
    else:
        ref_doi = titleToDoi.titletodoi(keyword)
    print(ref_doi)
    if (ref_doi == 'None'):
        signal = 'no'
        return HttpResponse(signal)
    else:
        wk = Works()
        item = wk.doi(ref_doi)
        if (item==None):
            signal = 'no'
            return HttpResponse(signal)
        else:
            try:
                find_doi = Ref.objects.get(ref_doi=ref_doi)
                print("ref数据库中找到记录")
            except:
                print("ref数据库中无记录")
                refDo.refdo(ref_doi)
                ref_record = Ref(ref_doi=ref_doi, create_rtime=datetime.now())
                ref_record.save()
                print("记录已存入ref数据库")
            print("ok")
            request.session['ref_doi'] = ref_doi
            print("ref session ok")
            #info=parseInfo.parse_info(ref_doi)
            #info = parseInfo.parse_info(ref_doi,item)
            #return HttpResponse(json.dumps(info))
            return HttpResponse(json.dumps(ref_doi))

#ref可视化详情页
def vis_ref_details(request,keyword):
    #info=parseInfo.parse_info(keyword)
    return render(request,'ref_details.html',{'ref_doi':json.dumps(keyword)})

#cit可視化
def vis_cit(request):
    keyword=request.POST.get('keyword')
    p = r'^10\.[\w]+\/[\w]+'
    pattern = re.compile(p)
    signal = 'yes'
    if (pattern.match(keyword)):
        cit_doi = keyword
    else:
        cit_doi = titleToDoi.titletodoi(keyword)
    print(cit_doi)
    if (cit_doi == 'None'):
        signal = 'no'
        return HttpResponse(signal)
    else:
        wk = Works()
        item = wk.doi(cit_doi)
        if (item==None):
            signal = 'no'
            return HttpResponse(signal)
        else:
            try:
                find_doi = Cit.objects.get(cit_doi=cit_doi)
                print("cit数据库中找到记录")
            except:
                print("cit数据库中无记录")
                citDo.citdo(cit_doi)
                cit_record = Cit(cit_doi=cit_doi, create_ctime=datetime.now())
                cit_record.save()
            # citDo.citdo(cit_doi)
            request.session['cit_doi'] = cit_doi
            print("cit session ok")
            return HttpResponse(cit_doi)

#cit可视化详情页
def vis_cit_details(request,keyword):
    #info = parseInfo.parse_info(keyword)
    print(keyword)
    return render(request,'cit_details.html',{'cit_doi':json.dumps(keyword)})

#summary
def summary(request):
    keyword=request.GET.get('summary')
    if(keyword==None):
        return render(request,'summary.html',{'doi':json.dumps('no')})
    else:
        p = r'^10\.[\w]+\/[\w]+'
        pattern = re.compile(p)
        if (pattern.match(keyword)):
            doi = keyword
        else:
            doi=titleToDoi.titletodoi(keyword)
        if(doi!='None'):
            try:
                find_doi=Sum.objects.get(sum_doi=doi)
                print("数据库Sum中找到记录")
                return render(request, 'summary.html', {'doi': json.dumps(doi), 'keyword': keyword})
            except:
                print("数据库Sum中未找到记录")
                wk = Works()
                item = wk.doi(doi)
                if(item!=None):
                    try:
                        find_cit_doi = Cit.objects.get(cit_doi=doi)
                        print("cit数据库中有记录")
                    except:
                        print("cit数据库中无记录")
                        citDo.citdo(doi)
                        cit_record = Cit(cit_doi=doi, create_ctime=datetime.now())
                        cit_record.save()
                        print("已存入cit数据库")
                    try:
                        find_ref_doi = Ref.objects.get(ref_doi=doi)
                        print("ref数据库中有记录")
                    except:
                        print("ref数据库中无记录")
                        refDo.refdo(doi)
                        ref_record = Ref(ref_doi=doi,create_rtime=datetime.now())
                        ref_record.save()
                        print("已存入ref数据库")
                    #summaryDo.summarydo(doi)
                    sum_record=Sum(sum_doi=doi,create_stime=datetime.now())
                    sum_record.save()
                    print("此条记录已存入Sum数据库")
                    return render(request,'summary.html',{'doi':json.dumps(doi),'keyword':keyword})
                else:
                    print("输入doi不合法")
                    return render(request, 'summary.html', {'doi': 'Uncorrect'})
        else:
            return render(request,'summary.html',{'doi':json.dumps('yes')})


#登录
def mylogin(request):
    if request.method=='POST':
        form=lForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print(name)
            print(password)
            user=authenticate(username=name,password=password)
            #print(request.session['login_from'])
            url=request.session['login_from']
            print(url)
            if user is not None:
                login(request,user)
            return HttpResponseRedirect(url)
    else:
        form=lForm()
        if('register' not in request.META.get('HTTP_REFERER', '/')):
            request.session['login_from']=request.META.get('HTTP_REFERER', '/')
    try:
        reg_name=request.session['reg_name']
        reg_password = request.session['reg_password']
        return  render(request,'login.html',{'name':reg_name,'password':reg_password})
    except:
        return render(request, 'login.html', {})

#登出
def mylogout(request):
    #url= request.META.get('HTTP_REFERER', '/')
    logout(request)
    #return HttpResponseRedirect(url)
    return render(request,'home.html',{})

#注册
def register(request):
    if request.method=='POST':
        form=rForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            #print(name)
            #print(password)
            try:
                find_usr=User.objects.get(username=name)
                flag='existed'
                return render(request, 'register.html', {'info':json.dumps(flag)})
            except:
                new_user=User.objects.create_user(name, email, password)
                new_user.save()
                request.session['reg_name']=name
                request.session['reg_password']=password
                return HttpResponseRedirect('/login')
        else:
            return render(request, 'register.html', {'info': 'error'})
    else:
        form=rForm()
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request,'register.html',{})

#个人中心
def indiv(request,username,cat):
    print(cat)
    star_json={'total':{},
               'Summary':{},
               'Search':{},
               'Ref':{},
               'Cit':{},
               'Unknown':{}}
    results=Star.objects.filter(username=username)
    for result in results:
        tmp = {}
        doi=result.star_doi
        title=result.star_title
        time=result.star_time
        source=result.star_source
        tmp['doi']=doi
        tmp['title']=title
        tmp['time']=str(time)
        tmp['source']=source
        star_json['total'][len(star_json['total'])]=tmp
        star_json[source][len(star_json[source])]=tmp
    if(cat!=''):
        return render(request,'indiv.html',{'results':star_json,'cat':json.dumps(cat)})
    else:
        return render(request,'indiv.html',{'results':star_json})

#收藏
def star(request):
    doi=request.POST.get('doi')
    source=request.POST.get('source')
    name=request.user.username
    print(name)
    try:
        find_star=Star.objects.get(username=name,star_doi=doi,star_source=source)
        print('该用户已经收藏过此记录')
        flag='existed'
    except:
        print('Star数据库中无记录')
        works=Works()
        try:
            star_item=works.doi(doi)
            star_title = ''
            t = star_item['title']
            for i in t:
                star_title = star_title + i
            if (star_title == ''):
                star_title = 'Unknown'
        except:
            star_title='Unknown'
        star_record=Star(star_doi=doi,username=name,star_title=star_title,star_time=datetime.now(),star_source=source)
        star_record.save()
        print('已收藏该记录')
        flag='collected'
    return HttpResponse(flag)

#帮助
def help(request):
    return render(request,'help.html',{})



