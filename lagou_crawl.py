import uuid
import requests
import time
import json
import pandas as pd
from lxml import etree
import re
import random


positionName_list, salary_list, city_list,district_list, companyShortName_list, education_list,workYear_list ,industryField_list,financeStage_list,companySize_list,job_desc_list= [], [], [],[], [], [],[],[],[],[],[]
def get_uuid():
    return str(uuid.uuid4())
def get_lagou(page,city,kd):
    url = "https://www.lagou.com/jobs/positionAjax.json"
    querystring = {"px": "new", "city": city, "needAddtionalResult": "false", "isSchoolJob": "0"}
    payload = "first=false&pn=" + str(page) + "&kd="+str(kd)
    cookie = "JSESSIONID=" + get_uuid() + ";"\
        "user_trace_token=" + get_uuid() + "; LGUID=" + get_uuid() + "; index_location_city=%E6%88%90%E9%83%BD; " \
        "SEARCH_ID=" + get_uuid() + '; _gid=GA1.2.717841549.1514043316; ' \
        '_ga=GA1.2.952298646.1514043316; ' \
        'LGSID=' + get_uuid() + "; " \
        "LGRID=" + get_uuid() + "; "
    headers = {'cookie': cookie,'origin': "https://www.lagou.com",'x-anit-forge-code': "0",'accept-encoding': "gzip, deflate, br",'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",'content-type': "application/x-www-form-urlencoded; charset=UTF-8",'accept': "application/json, text/javascript, */*; q=0.01",'referer': "https://www.lagou.com/jobs/list_Java?px=new&city=%E6%88%90%E9%83%BD",'x-requested-with': "XMLHttpRequest",'connection': "keep-alive",'x-anit-forge-token': "None",'cache-control': "no-cache",'postman-token': "91beb456-8dd9-0390-a3a5-64ff3936fa63"}
    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers, params=querystring)
    # print(response.text)
    hjson = json.loads(response.text)
    for i in range(15):
        positionName=hjson['content']['positionResult']['result'][i]['positionName']
        companyId = hjson['content']['positionResult']['result'][i]['companyId']
        positionId= hjson['content']['positionResult']['result'][i]['positionId']
        salary = hjson['content']['positionResult']['result'][i]['salary']
        city= hjson['content']['positionResult']['result'][i]['city']
        district= hjson['content']['positionResult']['result'][i]['district']
        companyShortName= hjson['content']['positionResult']['result'][i]['companyShortName']
        education= hjson['content']['positionResult']['result'][i]['education']
        workYear= hjson['content']['positionResult']['result'][i]['workYear']
        industryField= hjson['content']['positionResult']['result'][i]['industryField']
        financeStage= hjson['content']['positionResult']['result'][i]['financeStage']
        companySize= hjson['content']['positionResult']['result'][i]['companySize']
        job_desc = get_job_desc(positionId)
        positionName_list.append(positionName)
        salary_list.append(salary)
        city_list.append(city)
        district_list.append(district)
        companyShortName_list.append(companyShortName)
        education_list.append(education)
        workYear_list.append(workYear)
        industryField_list.append(industryField)
        financeStage_list.append(financeStage)
        companySize_list.append(companySize)
        #job_desc_list.append(job_desc)
        job_desc_list.append('')

        print("positionName:%s,companyId:%s,salary:%s,district:%s,companyShortName:%s,education:%s,workYear:%s"%(positionName,companyId,salary,district,companyShortName,education,workYear))
        #print("position:%s"%(job_desc))



def get_job_desc(id):
    url = "https://www.lagou.com/jobs/"+str(id)+".html"
    cookie = "JSESSIONID=" + get_uuid() + ";"\
        "user_trace_token=" + get_uuid() + "; LGUID=" + get_uuid() + "; index_location_city=%E6%88%90%E9%83%BD; " \
        "SEARCH_ID=" + get_uuid() + '; _gid=GA1.2.717841549.1514043316; ' \
        '_ga=GA1.2.952298646.1514043316; ' \
        'LGSID=' + get_uuid() + "; " \
        "LGRID=" + get_uuid() + "; "
    headers = {'cookie': cookie,'origin': "https://www.lagou.com",'x-anit-forge-code': "0",'accept-encoding': "gzip, deflate, br",'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",'content-type': "application/x-www-form-urlencoded; charset=UTF-8",'accept': "application/json, text/javascript, */*; q=0.01",'referer': "https://www.lagou.com/jobs/list_Java?px=new&city=%E6%88%90%E9%83%BD",'x-requested-with': "XMLHttpRequest",'connection': "keep-alive",'x-anit-forge-token': "None",'cache-control': "no-cache",'postman-token': "91beb456-8dd9-0390-a3a5-64ff3936fa63"}
    response = requests.request("GET", url, headers=headers)
    x = etree.HTML(response.text)
    data = x.xpath('//*[@id="job_detail"]/dd[2]/div/*/text()')
    return ''.join(data)

def write_to_csv(city,job):
    infos = {'positionName': positionName_list, 'salary': salary_list, 'city': city_list, 'district': district_list, 'companyShortName': companyShortName_list, 'education': education_list,'workYear':workYear_list,'industryField':industryField_list,'financeStage':financeStage_list,'companySize':companySize_list,'job_desc':job_desc_list}
    data = pd.DataFrame(infos, columns=['positionName', 'salary', 'city', 'district', 'companyShortName', 'education','workYear','industryField','financeStage','companySize','job_desc'])
    data.to_csv("lagou-"+city+"-"+job+".csv")

def main(pages,city,job):
    for n in range(1, pages+1):
        get_lagou(n,city,job)
        time.sleep(round(random.uniform(3, 5), 2))
    write_to_csv(city,job)


if __name__ == "__main__":
    main(30,'','Python')
    #main(30,"广州",'Python')
    #main(1, "广州", '测试')
