
from requests import request
from bs4 import BeautifulSoup
import re
import pymysql
from demo40.db import *


def get_connection():
    conn = pymysql.Connect \
        (host=HOST, port=PORT, db=DATABASE,
         user=USER, passwd=PASSWORD, charset=CHARSET)
    return conn


def get_url(num):
    url = 'http://was.jl.gov.cn/was5/web/search?channelid=237687&page=1&prepage={0}&searchword=gtitle%3C%3E%27%27%20and%20gtitle%3C%3E%27null%27%20and%20tType=%27%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%27%20%20and%20iType=%27%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A%27%20%20&callback&callback=result&_=1573001701476'.format(
        num)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    res = request(url=url, headers=header, method='GET')
    res.encoding = 'utf-8'
    html = res.text.strip()[6:].strip('(').strip(');')
    html_dict = eval(html)
    html_list = html_dict['datas']
    print(html_list)
    urls = []
    for data in html_list:
        url = data['docpuburl']
        urls.append(url)
    return urls


def changeCodeToLink(code):
    codes = [["122201004232188615", "长春市政府采购中心"],
             ["12220000412759478T", "吉林省矿权中心"],
             ["1222010056393822XT", "长春市城乡土地交易中心"],
             ["73700954-4", "吉林省政府采购中心"],
             ["12220100423200207X", "吉林省产权中心"],
             ["12220200782609514F", "吉林市人民政府政务服务中心"],
             ["34004150-3", "辽源市公共资源交易中心"],
             ["112203007645929828", "四平市政务服务中心"],
             ["66011618-0", "松原市人民政府政务服务中心"],
             ["122200005740930828", "吉林省公共资源交易中心"],
             ["73256854-X", "延边朝鲜族自治州政府采购中心"],
             ["73256678-X", "通化市人民政府政务公开办公室"],
             ["66429601-9", "白城市人民政府政务服务中心"],
             ["12220600737041237Q", "白山市公共资源交易中心"],
             ["01382732-2", "长春市城乡建设委员会"],
             ["122030000105", "四平市政务服务中心"],
             ["41270618-1", "四平市政务服务中心"],
             ["112203000135292377", "四平市政务服务中心"],
             ["112203000135298353", "四平市政务服务中心"],
             ["11220300413126808N", "四平市政务服务中心"],
             ["12220100MB10780025", "长春市公共资源交易中心（新）"],
             ["12220800MB11528661", "白城市公共资源交易中心"],
             ["12220400412763282Y", "辽源市公共资源交易平台（新）"],
             ["12220500MB1143476B", "通化市公共资源交易中心 "],
             ["12220700MB1837064Y", "松原市公共资源交易中心"],
             ["12220300MB0125428T", "四平市公共资源交易平台"],
             ["11222400MB14602364", "延边州公共资源交易平台（新）"],
             ["112200007710693483", "长白山管委会"]]

    source = ''
    for data in codes:
        if code in data:
            source = data[1]
            break
    if len(source) == 0:
        source = "长春市政府采购中心"
    return source



def get_html(num):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }
    urls = get_url(num)
    for url in urls:
        try:
            res = request(url=url, headers=header, method='GET')
            res.encoding = 'utf-8'
            html = res.text
            soup = BeautifulSoup(html, 'lxml')
            print('---------------------------------------------')
            # ====================================
            s1 = soup.find(text=re.compile('\d*text\(changeCodeToLink\d*')).split('\'')[1]
            print('===:', s1)
            source = changeCodeToLink(s1)
            print(source)
            html = html.split('相关链接')[0]
            soup = BeautifulSoup(html, 'lxml')
            # =====================================
            print('url: {0}'.format(url))
            project = soup.select('h3[class="ewb-article-tt"]')
            v1 = project[0].text
            time1 = soup.select_one('div[class="ewb-article-sources"]')
            v2 = time1.text
            print("1、项目名称=============")
            print(v1)
            print("2、公告时间=============")  # 调整时间格式
            v2 = get_strtime(v2)
            print(v2)
            print("3、招标地区=============")  # 根据来源URL判决地区
            print(v2)

            print("4、招标时间=============")
            data1 = soup.find_all(text=re.compile('\d年\d'))
            try:
                print(get_strtime(data1[0]))
            except:
                pass

            print("5、招标单位=============")  # 清理源文件相关链接
            data2 = soup.find_all(text=re.compile('\w*局\w*'))

            vv = ['省地税局', '省工商局', '省质监局', '省安监局', '省新闻出版广电局', '省体育局', '省统计局', '省粮食局',
                  '省经合局', '省管局', '省能源局', '省物价局', '省监狱管理局', '省公务员局', '省畜牧局', '省食品药品监管局',
                  '省中医药管理局', '省地矿局', '省测绘地信局', '省国税局', '省气象局', '省邮政管理局', '省广播电视局', '省体育局',
                  '省统计局', '省医疗保障局', '省机关事务管理局', '省粮食和物资储备局', '省地方金融监督管理局',
                  '省林业和草原局', '省能源局', '省监狱管理局', '省畜牧业管理局', '省中医药管理局', '省药品监督管理局',
                  '国家税务总局吉林省税务局', '国家外国专家局', '国家航天局', '国家海洋局', '国家核安全局', '国家税务总局',
                  '国家市场监督管理总局', '国家广播电视总局', '体育总局', '统计局', '国家医疗保障局', '国家机关事务管理局',
                  '国家新闻出版署（国家版权局）', '国家宗教事务局', '中国气象局', '国家信访局', '国家粮食和物资储备局', '国家能源局',
                  '国家国防科技工业局', '国家烟草专卖局', '国家移民管理局', '国家林业和草原局', '国家铁路局', '中国民用航空局',
                  '国家邮政局', '国家文物局', '国家中医药管理局', '国家煤矿安全监察局', '国家外汇管理局', '国家药品监督管理局',
                  '国家知识产权局', '出入境管理局', '国家公园管理局', '国家公务员局', '国家档案局', '国家保密局', '国家密码管理局',
                  '中共吉林省委吉林省人民政府信访局', '吉林省地矿局', '吉林省气象局', '吉林省地震局', '吉林省邮政管理局', '吉林省烟草专卖局']

            for data in vv:
                if data in data2:
                    data2.remove(data)
            print(data2)

            try:
                data2 = soup.find_all(text=re.compile('采购单位名称$')).find_parent().find_next().text  # 采购单位名称|
                if len(data2) == 0:
                    data2 = soup.find(text=re.compile('\w*馆\w*'))
                    # data2 = soup.find(text=re.compile('\w*馆\w*'))

                    if len(data1) == 0:
                        data1 = soup.find_all(text=re.compile('\w*吉林省\w*中心\w*'))
                        print(data1)
                    if len(data1) == 0:
                        data1 = soup.find_all(text=re.compile('\w*学\w*'))
                        print(data1)
                    if len(data1) == 0:
                        data1 = soup.find_all(text=re.compile('\w*队\*'))
                print(data2)
            except:
                pass

            print("6、中标金额=============")
            data3 = soup.find_all(text=re.compile('^\d*,\d*,\d*,\d*\.\d\d'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('\d元'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('^\d*,\d*,\d*\.\d\d'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('^\d*,\d*\.\d\d'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('^\d*\.\d\d'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('^\d*(0)$'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('\w*万'))
            if len(data3) == 0:
                data3 = soup.find_all(text=re.compile('\w*整'))
            print(data3)

            print("7、中标单位=============")  # 比对出第一公司为中标单位，第二为招标代理公司
            data4 = soup.find_all(text=re.compile('\w*公司\w*'))
            vv2 = ['长客公司', '德大公司']

            for data in vv2:
                if data in data4:
                    data4.remove(data)
            print(data4)

            v_data5 = ''
            print("8、评标组=============")
            data5 = soup.find_all(text=re.compile('[\u4E00-\u9FA5]{2,4}、[\u4E00-\u9FA5]{2,4}$'))
            if len(data5) == 0:
                data5 = soup.find(text=re.compile('[\u4E00-\u9FA5]{2,4}\s[\u4E00-\u9FA5]{2,4}\s'))
            # if type(data5) == 'list':
            #     data5 = '|'.join(data5)
            print(data5)

            print("9、招标编码=============")
            data6 = soup.find(text=re.compile('\w*J\w*'))
            print(data6)

            print("10、比对招标类型========")
            data7 = soup.find_all(text=re.compile('公开招标$'))
            if len(data7) == 0:
                data7 = soup.find_all(text=re.compile('\w*性谈判\w$'))
            if len(data7) == 0:
                data7 = soup.find_all(text=re.compile('\w*性磋商\w$'))
            if len(data7) == 0:
                data7 = soup.find_all(text=re.compile('\w*单一来源\w$'))
            if len(data7) == 0:
                data7 = soup.find_all(text=re.compile('\w*询价\w$'))
            print(data7)

            # data8 = soup.find_all(text=re.compile('招标代理$')).find_parent().find_next().text#采购单位名称|find_parent().
            print('-------------------------------------------------------------')
            conn = get_connection()
            c1 = conn.cursor()
            # ====================================================
            try:
                query_sql = \
                '''
                select 1 from projects where 项目名称 = {0}
                '''.format(v1)
                row_count = c1.execute()
                if row_count > 0:
                    continue
            except Exception as e:
                print(e)
            # =====================================================

            sql = '''
                insert into project1 (项目名称, 公告时间,  招标时间,
                   中标金额, 中标单位, 评标组,  url, source) values (
                   '{0}', '{1}',  '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')
            '''.format(v1, v2, v2, data3[0], '|'.join(data4), data5[0],  url, source)

            # sql = print(sql)
            print(sql)
            c1.execute(sql)
            conn.commit()
            # break
        except:
            continue



def get_strtime(text):
    text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
    text = re.sub("\s+", " ", text)
    t = ""
    regex_list = [
        "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",
        # "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})",
        "(\d{4}-\d{1,2}-\d{1,2})",
        # "(\d{4}-\d{1,2})",
    ]
    for regex in regex_list:
        t = re.search(regex, text)
    if t:
        t = t.group(1)
        return t
    else:
        print("没有获取到有效日期")

    return t


if __name__ == '__main__':
        get_html(100)


