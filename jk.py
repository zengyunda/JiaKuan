import  requests
import json
from datetime import datetime
import time
import pandas as pd

def post_page():#模拟登录
    url_post = 'http://120.198.245.80:3012/login'
    datas = {
    "authCode":"A4FD0F9F8CA735640137D5C9DDAC82D7",
    "sessionId":"0",
    "username":"wanghaifeng",
    'password':'Datacomm1',
    "verifyCode":"",
    "verifySMSVerifyCode":""
    }
    datas = json.dumps(datas)
    headers={
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Host':'120.198.245.80:3012',
    'content-type':'application/json',
    'Referer':'http://120.198.245.80:3012/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'}
    sessions = requests.Session()
    response_post = sessions.post(url = url_post,data=datas,headers=headers)
    #print(sessions.cookies.get_dict())
    #print(response_post.headers)
    #print(response_post.request)
    return sessions.cookies.get_dict()

def get_date():#设置GET的URL的开始及结束时间：
    now_time=datetime.now().strftime('%Y-%m-%d')#取当前时间转换为年-月-日格式
    start_time=int(time.mktime(time.strptime(now_time,'%Y-%m-%d'))-86400)#把当前年-月-日时间转换为时间戳，同时减去1天
    end_time=int(time.mktime(time.strptime(now_time,'%Y-%m-%d')))
    return start_time,end_time

def get_webdelays_page(cookie,start_time,end_time):#获取网页时延
    url_get = 'http://120.198.245.80:3012/getDataDetails?_dc=1523414887465&sort=reportTime&dir=DESC&testId=161&testType=11&sourceNodeId=0&destNodeId=0&locationId=0&hostIp=&start=0&limit=50&beginTime='+str(start_time)+'&endTime='+str(end_time)+'&twoWayMatch=false&needMobileStatus=false&useSourceNode=true&useDestNode=true&timeInterval=0&timeLength=86400&exType=none&exBeginTime=0&exEndTime=0&detailsFlag=true&conditions='
    sessions = requests.Session()
    response_get = sessions.get(url=url_get,cookies=cookie)
    if response_get.status_code == 200 and response_get.json() == {'errorCode': 1, 'errorDescription': 'Access Denied'}:
        print('该用户已登录家宽端到端质量监测平台，登录失败')
    else:
        print('获取网页时延数据成功')
    response_js = response_get.json()
    totalcount = response_js['totalCount']
    #totalcount = 100
    list_web_delays=[]
    for pages in range(0,int(totalcount),50):
        url_get = 'http://120.198.245.80:3012/getDataDetails?_dc=1523414887465&sort=reportTime&dir=DESC&testId=161&testType=11&sourceNodeId=0&destNodeId=0&locationId=0&hostIp=&start='+str(pages)+'&limit=50&beginTime='+str(start_time)+'&endTime='+str(end_time)+'&twoWayMatch=false&needMobileStatus=false&useSourceNode=true&useDestNode=true&timeInterval=0&timeLength=86400&exType=none&exBeginTime=0&exEndTime=0&detailsFlag=true&conditions='
        sessions = requests.Session()
        response_get = sessions.get(url=url_get,cookies=cookie)
        response_get = response_get.json()
        print('共'+str(int(totalcount/50))+'页，'+'正在爬取网页时延第'+str(int(pages/50))+'页')
        for rows in response_get['rows']:
            if rows['totalTime'] != None:
                list_web_delays.append(rows['totalTime'])
    web_delays=round(sum(list_web_delays)/len(list_web_delays)/1000/1000,2)
    print('爬取完毕，网页时延为：',web_delays)
    return web_delays

def get_videodelays_page(cookie,start_time,end_time):#获取视频时延
    url_get = 'http://120.198.245.80:3012/getDataDetails?_dc=1523414887465&sort=reportTime&dir=DESC&testId=193&testType=19&sourceNodeId=0&destNodeId=0&locationId=0&hostIp=&start=0&limit=50&beginTime='+str(start_time)+'&endTime='+str(end_time)+'&twoWayMatch=false&needMobileStatus=false&useSourceNode=true&useDestNode=true&timeInterval=0&timeLength=86400&exType=none&exBeginTime=0&exEndTime=0&detailsFlag=true&conditions='
    sessions = requests.Session()
    response_get = sessions.get(url=url_get,cookies=cookie)
    if response_get.status_code == 200 and response_get.json() == {'errorCode': 1, 'errorDescription': 'Access Denied'}:
        print('用户已登录，获取数据失败')
    else:
        print('获取视频时延数据成功')
    response_js = response_get.json()
    #totalcount = 100
    totalcount = response_js['totalCount']
    list_video_delays=[]
    for pages in range(0,int(totalcount),50):
        url_get = 'http://120.198.245.80:3012/getDataDetails?_dc=1523414887465&sort=reportTime&dir=DESC&testId=193&testType=19&sourceNodeId=0&destNodeId=0&locationId=0&hostIp=&start='+str(pages)+'&limit=50&beginTime='+str(start_time)+'&endTime='+str(end_time)+'&twoWayMatch=false&needMobileStatus=false&useSourceNode=true&useDestNode=true&timeInterval=0&timeLength=86400&exType=none&exBeginTime=0&exEndTime=0&detailsFlag=true&conditions='
        sessions = requests.Session()
        response_get = sessions.get(url=url_get,cookies=cookie)
        response_get = response_get.json()
        print('共'+str(int(totalcount/50))+'页，'+'正在爬取视频时延第'+str(int(pages/50))+'页')
        for rows in response_get['rows']:
            if rows['firstFrameTime'] != None:
                list_video_delays.append(rows['firstFrameTime'])
    video_delays = round(sum(list_video_delays)/len(list_video_delays)/1000/1000,2)
    print('爬取完毕，视频时延为：',video_delays)
    return video_delays

def get_gamedelays_page(start_time,end_time):
    url_post = 'http://120.198.253.120:5012/'
    datas_post = {'username': 'wanghaifeng', 'password': 'Datacomm1'}
    headers_post = {'Referer': 'http://120.198.253.120:5012/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36' '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN,zh;q=0.8',}
    sessions = requests.Session()
    sessions.post(url=url_post, headers=headers_post, data=datas_post)#根据post的相关信息，模拟登录
    url_get = 'http://120.198.253.120:5012/getBusinessQualityDayWeekMonthReport?_dc=1521616451788&sort=summaryTime&dir=ASC&start=0&limit=&queryType=2&beginTime='+str(start_time)+'&endTime='+str(end_time)+'&timeInterval=86400&filterCityName=%E6%B8%85%E8%BF%9C&filterBusinessType='
    headers_get = {'Referer': 'http://120.198.253.120:5012/apps/bqm/?privilege=false&groupId=15&id=170',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'x-forward-url': 'http://localhost:5080/getBusinessQualityDayWeekMonthReport',
           'X-Requested-With': 'XMLHttpRequest'}
    response_get = sessions.get(url=url_get, headers = headers_get)#获取get的相关参数
    dict_to_list = list(response_get.json()['results'].values())[0][0]#json文件处理，取出字典results的所有vaules转换成列表，再取列表的值
    carlton_times = round(dict_to_list['stallTimes'],3)*12#卡顿次数
    game_delays=round(dict_to_list['avgDelay']/1000,2)#游戏时延
    avgBufferPercent=round(dict_to_list['avgBufferPercent']/100,4)
    reachPercentGroup=round(dict_to_list['reachPercentGroup']/100,4)
    lossPercent=round(dict_to_list['lossPercent']/100,4)
    print('卡顿次数：',carlton_times,'\n','游戏时延：',game_delays,'\n','视频总缓冲时长占比(%)：'
          ,avgBufferPercent,'\n','TOP100网站达标比例：',reachPercentGroup,'\n','游戏丢包率(%)',lossPercent)
    #游戏业务TOP10及探针数据统计
    url_get = 'http://120.198.253.120:5012/getBusinessQualityDataDetails?_dc=1523799108186&sort=reportTime&dir=ASC&start=0&limit=50&queryType=1&businessType=5&beginTime=' + str(
        start_time) + '&endTime=' + str(end_time) + '&timeInterval=86400&filterCityName=%E6%B8%85%E8%BF%9C'
    headers_get = {'Referer': 'http://120.198.253.120:5012/apps/bqm/?privilege=false&groupId=15&id=170',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                   'Accept': '*/*',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'x-forward-url': 'http://localhost:5080/getBusinessQualityDataDetails',
                   'X-Requested-With': 'XMLHttpRequest'}
    response_get = sessions.get(url=url_get, headers=headers_get)  # 获取get的相关参数
    #totalCount = 100
    totalCount = response_get.json()['totalCount']
    destName = []
    avgDelay = []
    areaName = []
    for pages in range(0, int(totalCount), 50):
        url_get_data = 'http://120.198.253.120:5012/getBusinessQualityDataDetails?_dc=1523799108186&sort=reportTime&dir=ASC&start=' + str(pages) + '&limit=50&queryType=1&businessType=5&beginTime=' + str(start_time) + '&endTime=' + str(end_time) + '&timeInterval=86400&filterCityName=%E6%B8%85%E8%BF%9C'
        response_get_data = sessions.get(url=url_get_data, headers=headers_get)
        print('共' + str(int(totalCount)/50) + '页，' + '正在爬取游戏时延清单第' + str(int(pages/50)) + '页')
        for i in response_get_data.json()['results']:
            destName.append(i['destName'].split('-')[0])
            avgDelay.append(i['avgDelay'] / 1000)
            areaName.append(i['areaName'])
    areaName = list(set(areaName))  # 转换为set，去重
    areaName_new = []
    for i in areaName:
        areaName_new.append((i[2:4]))  # 截取县区字段
    df_name = pd.DataFrame({'探针名称': areaName_new, '在线探针数量': 1})
    df_name = df_name.groupby('探针名称').count().reset_index().T#探针名称数据透视，取个数，然后转置
    df_games = pd.DataFrame({'游戏ping时延（ms)': avgDelay, '游戏名称': destName})
    # 将df数据按照游戏名称进行数据透视，然后取平均值，按照游戏ping时延（ms)降序排列，取TOP10，保留两位小数，并重置成默认索引（方便导出到Excel）
    df_games = df_games.groupby('游戏名称').mean().sort_values(by='游戏ping时延（ms)', ascending=False)[:10].round(2).reset_index()
    return carlton_times,game_delays,avgBufferPercent,reachPercentGroup,lossPercent,df_games,df_name

def save_to_execl(video_delays,web_delays,carlton_times,game_delays,avgBufferPercent,reachPercentGroup,lossPercent,df_games,df_name):
    kpi = [video_delays,carlton_times, avgBufferPercent,web_delays, reachPercentGroup,game_delays, lossPercent]
    heads = ['视频播放时延（s）','视频平均播放卡顿次数', '视频总缓冲时长占比(%)','网页首屏时延（s）',
             'TOP100网站达标比例','游戏ping时延(ms)','游戏丢包率(%)']
    df = pd.DataFrame({'指标值':kpi,'名称':heads})
    writer = pd.ExcelWriter('D://家宽探针指标.xls')
    df.to_excel(writer, '指标情况')
    df_name.to_excel(writer, '在线探针数量')
    df_games.to_excel(writer, '游戏业务时延TOP10')
    writer.save()

def get_cell_page(start_time,end_time):
    url_post = 'http://120.198.253.120:5012/login'
    datas_post = {'username': 'wanghaifeng', 'password': 'Datacomm1'}
    headers_post = {'Referer': 'http://120.198.253.120:5012/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36' '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'Accept': '*/*',
           'Accept-Language': 'zh-CN,zh;q=0.8',}
    sessions = requests.Session()
    response_post = sessions.post(url=url_post, headers=headers_post, data=datas_post)#根据post的相关信息，模拟登录
    #print(response_post.cookies.get_dict())
    cookie = response_post.cookies.get_dict()
    start_time =start_time -172800
    url_get_cell = 'http://120.198.253.120:5012/getBusinessQualityBadQualityArea?_dc=1524209886673&sort=businessScore&dir=ASC&start=0&limit=50&queryType=1&beginTime=' + str(start_time) + '&endTime=' + str(end_time) + '&timeInterval=259200&filterCityName=%E6%B8%85%E8%BF%9C&filterAreaName=&filterBusinessType='
    headers_get = {
        'Referer': 'http://120.198.253.120:5012/apps/bqm/?privilege=false&groupId=15&id=170',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'x-forward-url': 'http://localhost:5080/getBusinessQualityBadQualityArea'
        }
    response_cell = sessions.get(url=url_get_cell,headers=headers_get)
    totalCount = response_cell.json()['totalCount']
    result = []
    for pages in range(0,int(totalCount),50):
        url_get_cell = 'http://120.198.253.120:5012/getBusinessQualityBadQualityArea?_dc=1524209886673&sort=businessScore&dir=ASC&start='+str(pages)+'&limit=50&queryType=1&beginTime=' + str(start_time) + '&endTime=' + str(end_time) + '&timeInterval=259200&filterCityName=%E6%B8%85%E8%BF%9C&filterAreaName=&filterBusinessType='
        response_cell = sessions.get(url=url_get_cell,headers=headers_get)
        for i in response_cell.json()['results'][str(start_time)]:
            result.append(i)
    columns=['areaName', 'avgBufferPercent', 'avgDelay', 'businessScore', 'cityName', 'flvScore', 'gameScore', 'lossPercent', 'reachPercentBank', 'reachPercentGroup', 'reachPercentProvince', 'stallTimes', 'summaryTime', 'throughPutBank', 'throughPutGroup', 'throughPutProvince', 'webpageScore', 'webpageScoreBank', 'webpageScoreGroup', 'webpageScoreProvince']
    pf = pd.concat([pd.DataFrame([i], columns=columns) for i in result],ignore_index=True)#把list转换为数据框
    pf['summaryTime'] = pd.to_datetime(pf['summaryTime']+28800000000, unit='us')#把unix时间进行转换，加上28800是因为转换的时间是16：00
    pf['avgDelay'] = pf['avgDelay']/1000#单位转换
    pf['throughPutGroup'] = pf['throughPutGroup']/1024#单位转换
    pf.rename(columns = {'summaryTime':'时间','cityName':'地市','stallTimes':'视频卡顿次数','areaName':'小区名称',
                         'avgBufferPercent':'视频平均缓冲比(%)','flvScore':'视频得分(10分)',
                         'reachPercentGroup':'Top100网站首屏达标比(%)','throughPutGroup':'Top100网站吞吐率(KB/s)',
                         'webpageScore':'网页得分(15分)','avgDelay':'游戏时延(ms)',
                         'lossPercent':'游戏丢包率(%)','gameScore':'游戏得分(15分)','businessScore':'总分'},inplace = True)
    pf = pf[['时间','地市','小区名称','视频卡顿次数','视频平均缓冲比(%)','视频得分(10分)',
             'Top100网站首屏达标比(%)','Top100网站吞吐率(KB/s)',
             '网页得分(15分)','游戏时延(ms)','游戏丢包率(%)','游戏得分(15分)','总分']]
    #pd.set_option('display.precision', 3)#设置输出到屏幕的精度
    #pd.set_option('display.width', 7000)
    #print(pf)
    start_time = time.strftime('%m%d',time.localtime(start_time))
    end_time = time.strftime('%m%d',time.localtime(end_time-86400))
    pf.to_excel('D://质差小区'+str(start_time)+'-'+str(end_time)+'.xlsx',float_format='%11.3f',na_rep='-')
    print('质差小区获取完毕')
def logout(cookie):#模拟退出登录
    sessions = requests.Session()
    url= 'http://120.198.245.80:3012/logout'
    response=sessions.post(url=url,cookies=cookie)
    if response.status_code == 200:
        print('退出登录！')

def main():
    starttime = time.time()
    start_time,end_time = get_date()
    carlton_times,game_delays,avgBufferPercent,reachPercentGroup,lossPercent,df_games,df_name = get_gamedelays_page(start_time,end_time)
    get_cell_page(start_time,end_time)
    cookie = post_page()
    try:
        web_delays = get_webdelays_page(cookie,start_time,end_time)
        video_delays = get_videodelays_page(cookie,start_time,end_time)
        save_to_execl(video_delays,web_delays,carlton_times,game_delays,avgBufferPercent,reachPercentGroup,lossPercent,df_games,df_name)
        endtime = time.time()
        dtime = endtime - starttime
        print('数据提取完毕，已保存至本地,共耗时'+str(round(dtime))+'秒！')
    except Exception as e:
        print('发生错误'+str(e))
    logout(cookie)

if __name__ == '__main__':
    main()
