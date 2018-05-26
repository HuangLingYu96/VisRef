from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import json
import re
import os
from crossref.restful import Works
from datetime import datetime
from PIL import Image
import urllib.request

from .form import rForm
from .form import lForm
from .models import File
from .models import Ref
from .models import Cit
from .models import Sum
from .models import Sea
from .models import Star
from .models import Profile
from .models import Pagination
from .models import Info
from .myScripts import refDo
from .myScripts import citDo
from .myScripts import summaryDo
from .myScripts import searchDo
from .myScripts import titleToDoi
from .myScripts import parseInfo
from .myScripts import searchDo2
from .myScripts import infoDo
from .myScripts import citDo2
from .myScripts import refDo2

# Create your views here.
#首页
def home(request):
    context={}
    return render(request,'home.html',context)

#search
def search(request):
    keyword = request.GET.get('search')
    if (keyword==None):
        return render(request, 'search.html', {})
    else:
        find_keyword = Sea.objects.filter(keyword__iexact=keyword)
        l=len(find_keyword)
        if(l!=0):
            print('数据库Sea中找到记录')
            return render(request, 'search.html', {'results': find_keyword, 'keyword': keyword})
        else:
            print('数据库Sea未中找到记录')
            works = Works()
            w1 = works.query(title=keyword)
            for index, item in enumerate(w1):
                if (index > 499):
                    break
                result=searchDo.parse_result(keyword,item)
                #存入数据库
                sea_record=Sea(**result)
                sea_record.save()
                print(str(index)+' record is ok')
            find_keyword = Sea.objects.filter(keyword__iexact=keyword)
            return render(request, 'search.html', {'results': find_keyword, 'keyword': keyword})

#搜索
def search2(request):
    keyword = request.GET.get('search')
    if (keyword == None):
        return render(request, 'search.html', {})
    else:
        find_keyword = Sea.objects.filter(keyword__iexact=keyword)
        l = len(find_keyword)
        if (l != 0):
            print('数据库Sea中找到记录')
            return render(request, 'search.html', {'results': find_keyword, 'keyword': keyword})
        else:
            print('数据库Sea未中找到记录')
            url = r'https://api.crossref.org/works?query='+keyword+'&sort=is-referenced-by-count&order=desc&rows=500'
            path=os.getcwd() + '\\media\\sea\\'+keyword+'.json'
            urllib.request.urlretrieve(url,path)
            print(keyword+'.json ok')
            with open(path, 'r') as f:
                data = json.load(f)
            items=data['message']['items']
            index=1
            for item in items:
                result=searchDo2.parse_info(item,keyword)
                sea_record = Sea(**result)
                sea_record.save()
                print(str(index) + ' record is ok')
                index+=1
            find_keyword = Sea.objects.filter(keyword__iexact=keyword)
            return render(request, 'search.html', {'results': find_keyword, 'keyword': keyword})


#可视化
def vis(request):
    return render(request,'visualization2.html',{'start':'yes'})

#ref可视化
def vis_ref(request):
    keyword = request.POST.get('keyword')
    ref_doi = doi_trans(keyword)
    if (ref_doi == None):
        signal = 'TitleError'
        return HttpResponse(signal)
    else:
        # 查找对应的文件名，如1,2,3
        ref_file_id = file_find(ref_doi)
        print(ref_file_id)
        # 查找ref数据库中记录
        ref_flag = ref_find(ref_doi)
        if (ref_flag== 'existed'):
            print("ref数据库中找到记录")
            return HttpResponse(ref_file_id)
        else:
            print("ref数据库中无记录")
            wk = Works()
            item = wk.doi(ref_doi)
            if (item == None):
                signal = 'DoiError'
            else:
                refDo2.refdo(ref_doi,ref_file_id)
                ref_record = Ref(ref_doi=ref_doi, create_rtime=datetime.now())
                ref_record.save()
            return HttpResponse(ref_file_id)

#ref可视化详情页,keyword一定是doi形式
def vis_ref_details(request,keyword):
    print(keyword)
    ref_file_id=file_find(keyword)
    return render(request,'ref_details.html',{'ref_doi':json.dumps(keyword),'ref_file_id':json.dumps(ref_file_id)})

#ref可视化详情页，分页
def ref_pagination(request,doi_prefix,doi_suffix,subject):
    filename=doi_prefix+'_'+doi_suffix+'.json'
    ref_doi=doi_prefix+'/'+doi_suffix
    print(filename)
    file_path=os.path.join("media/ref",filename)
    print(file_path)
    f = open(file_path, encoding='utf-8')
    setting=json.load(f)
    temp_dict=setting['statistics']['subject'][subject]
    #temp_json=json.dumps(temp_dict)
    #temp=Pagination(**temp_dict)
    temp_list=[]
    for index,content in temp_dict.items():
        temp_list.append(content)
    return render(request,'ref_details.html',{'temp':temp_list,'ref_doi':json.dumps(ref_doi),'subject':subject})

#cit可視化
def vis_cit(request):
    keyword=request.POST.get('keyword')
    cit_doi=doi_trans(keyword)
    if (cit_doi == None):
        signal = 'TitleError'
        return HttpResponse(signal)
    else:
        # 查找对应的文件名，如1,2,3
        cit_file_id=file_find(cit_doi)
        print(cit_file_id)
        #查找cit数据库中记录
        cit_flag=cit_find(cit_doi)
        if(cit_flag=='existed'):
            print("cit数据库中找到记录")
            return HttpResponse(cit_file_id)
        else:
            print("cit数据库中无记录")
            wk = Works()
            item = wk.doi(cit_doi)
            if (item==None):
                signal = 'DoiError'
            else:
                citDo.citdo(cit_doi,cit_file_id)
                cit_record = Cit(cit_doi=cit_doi, create_ctime=datetime.now())
                cit_record.save()
            return HttpResponse(cit_file_id)

#citation可视化
def vis_cit2(request):
    keyword = request.POST.get('keyword')
    cit_doi = doi_trans(keyword)
    if (cit_doi == None):
        signal = 'TitleError'
        return HttpResponse(signal)
    else:
        # 查找对应的文件名，如1,2,3
        cit_file_id = file_find(cit_doi)
        print(cit_file_id)
        #查找info表中记录
        info_flag=info_find(cit_doi)
        if (info_flag == 'existed'):
            print('info表中存在记录')
        else:
            print('info表中不存在记录')
            info_wk = Works()
            item = info_wk.doi(cit_doi)
            result=infoDo.parse_info(item)
            info_record = Info(**result)
            info_record.save()
            print('info表已保存该记录')
            path = os.getcwd() + '\\media\\info\\' + str(cit_file_id) + '.json'
            with open(path,"w", encoding='utf-8')as f:
                f.write(json.dumps(result, ensure_ascii=False))
                print('info文件已保存')
        infos=Info.objects.get(doi=cit_doi)
        date=infos.time
        title=infos.title
        cited=infos.is_referenced_by_count
        # 查找cit数据库中记录
        cit_flag = cit_find(cit_doi)
        if (cit_flag == 'existed'):
            print("cit数据库中找到记录")
            return HttpResponse(cit_file_id)
        else:
            print("cit数据库中无记录")
            citDo2.citdo(date,title,cited,cit_file_id)
            cit_record = Cit(cit_doi=cit_doi, create_ctime=datetime.now())
            cit_record.save()
            return HttpResponse(cit_file_id)

#cit可视化详情页,keyword一定是doi形式
def vis_cit_details(request,keyword):
    print(keyword)
    cit_file_id=file_find(keyword)
    return render(request,'cit_details2.html',{'cit_doi':json.dumps(keyword),'cit_file_id':json.dumps(cit_file_id)})

#summary
def summary(request):
    keyword=request.GET.get('summary')
    if(keyword==None):
        return render(request,'summary.html',{})
    else:
        doi=doi_trans(keyword)
        #doi为None（字符串），说明title转换doi失败
        if(doi!=None):
            #查找对应的文件名，如1,2,3
            file_id=file_find(doi)
            print(file_id)
            #查找sum数据库中是否有记录
            sum_flag=sum_find(doi)
            if(sum_flag=='existed'):
                print("数据库Sum中找到记录")
                return render(request, 'summary.html', {'doi': json.dumps(doi), 'keyword': keyword, 'file_id': file_id})
            else:
                print("数据库Sum中未找到记录")
                #测试doi是否在crossref数据库中，不在的话item为None
                wk = Works()
                item = wk.doi(doi)
                if(item!=None):
                    #查找ref信息
                    ref_flag=ref_find(doi)
                    if(ref_flag=='existed'):
                        print("ref数据库中找到记录")
                    else:
                        print("ref数据库未找到记录")
                        #refDo.refdo(doi, file_id)
                        refDo2.refdo(doi, file_id)
                        ref_record = Ref(ref_doi=doi, create_rtime=datetime.now())
                        ref_record.save()
                        print("已存入ref数据库")
                    #查找cit信息
                    cit_flag=cit_find(doi)
                    if(cit_flag=='existed'):
                        print("cit数据库中找到记录")
                    else:
                        print("cit数据库中未找到记录")
                        # 查找info表中记录
                        info_flag = info_find(doi)
                        if (info_flag == 'existed'):
                            print('info表中存在记录')
                        else:
                            print('info表中不存在记录')
                            result = infoDo.parse_info(item)
                            info_record = Info(**result)
                            info_record.save()
                            print('info表已保存该记录')
                            path = os.getcwd() + '\\media\\info\\' + str(file_id) + '.json'
                            with open(path, "w", encoding='utf-8')as f:
                                f.write(json.dumps(result, ensure_ascii=False))
                                print('info文件已保存')
                        infos = Info.objects.get(doi=doi)
                        date = infos.time
                        title = infos.title
                        cited = infos.is_referenced_by_count
                        citDo2.citdo(date, title, cited, file_id)
                        #citDo.citdo(doi, file_id)
                        cit_record = Cit(cit_doi=doi, create_ctime=datetime.now())
                        cit_record.save()
                        print("已存入cit数据库")
                    #记录存入sum数据库
                    sum_record = Sum(sum_doi=doi, create_stime=datetime.now())
                    sum_record.save()
                    print("此条记录已存入Sum数据库")
                    return render(request, 'summary.html',{'doi': json.dumps(doi), 'keyword': keyword, 'file_id': file_id})
                else:
                    print("输入doi不合法")
                    return render(request, 'summary.html', {'doi': 'DoiError'})
        else:
            return render(request,'summary.html',{'doi':json.dumps('TitleError')})

#登录
def mylogin(request):
    if request.method=='POST':
        form=lForm(request.POST)
        #表单输入合法
        if form.is_valid():
            name=form.cleaned_data['username']#获取用户名
            password=form.cleaned_data['password']#获取密码
            user=authenticate(username=name,password=password)
            url=request.session['login_from']#获取原操作界面
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(url)
            else:
                return render(request, 'login.html', {'error':'error'})
    else:
        form=lForm()
        url_flag=url_check(request.META.get('HTTP_REFERER', '/'))
        if url_flag=='no':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')#记录原操作界面
        return render(request, 'login.html', {})

#登出
def mylogout(request):
    url_flag=url_check(request.META.get('HTTP_REFERER', '/'))
    #如果http_referer包含'login','logout','indiv','register'
    if (url_flag=='yes'):
       # url=request.session['login_from']
        url='/help'
    else:
        url=request.META.get('HTTP_REFERER', '/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    logout(request)
    return HttpResponseRedirect(url)

#注册
def register(request):
    if request.method=='POST':
        form=rForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            try:
                find_usr=User.objects.get(username=name)
                return render(request, 'register.html', {'info':'existed'})
            except:
                new_user=User.objects.create_user(name, email, password)
                new_user.save()
                user = authenticate(username=name, password=password)
                url = request.session['login_from']
                if user is not None:
                    login(request, user)
                return HttpResponseRedirect(url)
        else:
            return render(request, 'register.html', {'info': 'error'})
    else:
        form=rForm()
        url_flag=url_check(request.META.get('HTTP_REFERER', '/'))
        if url_flag=='no':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        print(request.session['login_from'])
        return render(request,'register.html',{})

#检查用户名占用
def check_username(request):
    username=request.POST.get('username')
    try:
        find_username=User.objects.get(username=username)
        flag="existed"
    except:
        flag="inexisted"
    return HttpResponse(flag)

#检查邮箱占用
def check_email(request):
    email=request.POST.get('email')
    try:
        find_email=User.objects.get(email=email)
        flag="existed"
    except:
        flag="inexisted"
    return HttpResponse(flag)

#忘记密码页面
def password_reset(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        new_password=request.POST.get('password')
        find_user=User.objects.get(username=username,email=email)#验证身份
        find_user.set_password(new_password)#重置密码
        find_user.save()
        return HttpResponse('success')
    else:
        if ('login' not in request.META.get('HTTP_REFERER', '/')):
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request,'password_reset.html',{})

#验证用户，用户名+ 邮箱
def check_user(request):
    username=request.POST.get('username')
    email=request.POST.get('email')
    try:
        find_usr=User.objects.get(username=username,email=email)
        usr_flag='ok'
    except:
        usr_flag='error'
    return HttpResponse(usr_flag)

#个人收藏
def view_stars(request,username,cat):
    total_results=Star.objects.filter(username=username)
    sum_results=Star.objects.filter(username=username,star_source='Summary')
    ref_results = Star.objects.filter(username=username, star_source='Reference')
    cit_results = Star.objects.filter(username=username, star_source='Citation')
    results={'cat':cat,
             'len_total':len(total_results),
             'len_sum':len(sum_results),
             'len_ref':len(ref_results),
             'len_cit':len(cit_results)}
    if(cat==''):
        ids='id_star'
        results['results']=total_results
        results['length']=len(total_results)
    elif(cat=='summary'):
        ids='id_star_summary'
        results['results'] = sum_results
        results['length'] = len(sum_results)
    elif(cat=='reference'):
        ids='id_star_ref'
        results['results'] = ref_results
        results['length'] = len(ref_results)
    elif(cat=='citation'):
        ids='id_star_cit'
        results['results'] = cit_results
        results['length'] = len(cit_results)
    else:
        ids='Unknown'
        results['results'] = total_results
        results['length'] = len(total_results)
    results['ids']=json.dumps(ids)
    url_flag = url_check(request.META.get('HTTP_REFERER', '/'))
    if url_flag == 'no':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')  # 记录原操作界面
    return render(request,'stars.html',results)

#个人信息
def view_profile(request,username):
    url_flag = url_check(request.META.get('HTTP_REFERER', '/'))
    if url_flag == 'no':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')  # 记录原操作界面
    return render(request,'profile.html',{})

#修改个人信息
def profile_modify(request):
    old_username=request.POST.get('old_username')
    old_email=request.POST.get('old_email')
    name=request.POST.get('name')
    email=request.POST.get('email')
    birth=request.POST.get('birth')
    bio=request.POST.get('bio')
    company=request.POST.get('company')
    location=request.POST.get('location')
    #birth为string，转为date
    birth_date=datetime.strptime(birth,"%Y-%m-%d")
    #更新个人信息
    user=User.objects.get(username=old_username,email=old_email)
    user.profile.bio=bio
    user.profile.company=company
    user.profile.loaction=location
    user.profile.birth_date=birth_date
    user.username=name
    user.email=email
    user.save()
    #更新个人收藏
    Star.objects.filter(username=old_username).update(username=name)
    return HttpResponse('yes')

#修改密码页面
def password_setting(request,username):
    return render(request,'password_setting.html',{})

#检查用户密码是否对应
def check_password(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    try:
        user = authenticate(username=username, password=password)
        if user is not None:
            pwd_flag='ok'
        else:
            pwd_flag='error'
    except:
        pwd_flag='error'
    return HttpResponse(pwd_flag)

#修改密码
def password_modify(request):
    logout(request)
    username = request.POST.get('username')
    email = request.POST.get('email')
    new_password = request.POST.get('password')
    find_user = User.objects.get(username=username, email=email)
    find_user.set_password(new_password)
    find_user.save()
    user = authenticate(username=username, password=new_password)
    if user is not None:
        login(request, user)
    return HttpResponse('ok')

#收藏
def star(request):
    doi=request.POST.get('doi')
    source=request.POST.get('source')
    name=request.user.username
    filename=File.objects.get(doi=doi)
    file=str(filename.id)+'.json'
    try:
        find_star=Star.objects.get(username=name,star_doi=doi,
                                   star_source=source,star_file=file)
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
        star_record=Star(star_doi=doi,username=name,
                         star_title=star_title,star_time=datetime.now(),
                         star_source=source,star_file=file)
        star_record.save()
        print('已收藏该记录')
        flag='collected'
    return HttpResponse(flag)

#取消收藏
def dislike(request):
    name=request.POST.get('name')
    doi=request.POST.get('doi')
    source=request.POST.get('source')
    star_record=Star.objects.get(username=name,star_doi=doi,star_source=source)
    star_record.delete()
    return HttpResponse('ok')

#帮助
def help(request):
    return render(request,'help.html',{})

#上传头像
def avatar(request):
    im_obj = request.FILES.get('img')
    name=im_obj.name
    im_suffix=name.split('.')[1]
    pic_name=str(request.user.id)+'.'+im_suffix
    pic_path=os.path.join("media/usr", pic_name)
    if(os.path.exists(pic_path)):
        os.remove(pic_path)
    print(pic_name)
    print(pic_path)
    if im_obj:
        #pic_path = os.getcwd() + '\\media\\usr\\'+ im_obj.name
        f = open(pic_path, "wb")
        for chunck in im_obj.chunks():
            f.write(chunck)
        f.close()
        return HttpResponse("ok")

# 辅助函数，用于检测url包含关系，包含则返回yes，不包含返回no
def url_check(url):
    url_list = ['login', 'register', 'logout', 'indiv','password_reset']
    # url_flag = 'no'
    for u in url_list:
        if (u in url):
            return 'yes'
    return 'no'

#辅助函数，用于查找doi对应的文件名
def file_find(doi):
    # 查找对应的文件名，如1,2,3
    try:
        find_file = File.objects.get(doi=doi)
        file_id = find_file.id
    except:
        file_record = File(doi=doi)
        file_record.save()
        file_id = file_record.id
    return file_id

#辅助函数，判断doi还是title，如果是title转成doi
#keyword是get到的参数
def doi_trans(keyword):
    # p = r'^10\.[\w]+\/[\w]+'
    p = r'10\.[\w]+\/[^/]+'
    pattern = re.compile(p)
    if (pattern.match(keyword)):
        doi = keyword
    else:
        doi = titleToDoi.titletodoi(keyword)
    return doi

#辅助函数，用于查找sum数据库记录
def sum_find(doi):
    try:
        find_sum=Sum.objects.get(sum_doi=doi)
        return "existed"
    except:
        return "unexisted"

#辅助函数，用于查找ref数据库记录
def ref_find(doi):
    try:
        find_ref=Ref.objects.get(ref_doi=doi)
        return "existed"
    except:
        return "unexisted"

#辅助函数，用于查找cit数据库记录
def cit_find(doi):
    try:
        find_cit=Cit.objects.get(cit_doi=doi)
        return "existed"
    except:
        return "unexisted"

#辅助函数，用于查找info数据库记录
def info_find(doi):
    try:
        find_info=Info.objects.get(doi=doi)
        return "existed"
    except:
        return "unexisted"