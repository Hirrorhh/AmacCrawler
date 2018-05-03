# -*- coding: utf-8 -*-
import re
import scrapy,sys,json,random,datetime,time
from bs4 import BeautifulSoup
from scrapy.http import Request

from AmacCrawler import settings
from AmacCrawler.items import AmacManagerItem,AmacManagerDetailItem,FundItem,FundAccountItem,FundDetailItem,\
    FundAccountDetailItem,HmdItem,CXDJItem,ZQ,ZQDetailItem,QHItem,QHItemdetail


reload(sys)
sys.setdefaultencoding('utf-8')


class Myspider(scrapy.Spider):
    name = 'amac'
    allowed_domains = ['amac.org.cn']
    bash_url = 'http://www.amac.org.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json',
    }
    headers_user = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def __init__(self, name=None, **kwargs):
        super(Myspider, self).__init__(name=None, **kwargs)
    #爬虫开始执行入口
    def start_requests(self):
        #爬取管理人信息(回调函数中爬取个人详情)
        yield self.get_manager(page=0)
        #爬取私募基金数据信息(回调函数中爬取基金详情)
        yield self.get_fund(page=0)
        #爬取基金专户产品公示
        yield self.get_fund_acount(page=0)
        #私募基金管理人从业黑名单
        yield self.get_hmd()
        #管理人撤销登记
        yield self.get_cxdj()
        yield self.get_zq_item(page=0)
        yield self.get_qh_item(page=0)

    def get_province(self):
        url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager/register-address-agg/province'
        return Request(url, headers=self.headers, callback=self.cb_get_province)

    def cb_get_province(self, response):
        datas = json.loads(response.body)
        if datas:
            pass

    def get_manager(self, page):
        url = settings.AMAC_MANAGER_URL + '?rand=' + str(random.random()) + '&page=' + str(page) + '&size=100';
        value = {}
        return scrapy.FormRequest(url=url, headers=self.headers, method='POST', body=json.dumps(value), callback=self.cb_get_manager, meta={'page':page})

    def cb_get_manager(self, response):
        datas = json.loads(response.body)
        page = response.meta['page']
        print("now page = %s" % page)
        if datas:
            if page >= datas['totalPages']:
                return
            for content in datas['content']:
                item = AmacManagerItem()
                item['id'] = content['id']
                item['managerName'] = content['managerName']
                item['artificialPersonName'] = content['artificialPersonName']
                item['registerNo'] = content['registerNo']
                item['establishDate'] = content['establishDate']
                item['managerHasProduct'] = content['managerHasProduct']
                item['url'] = content['url']
                item['registerDate'] = content['registerDate']
                item['registerAddress'] = content['registerAddress']
                item['registerProvince'] = content['registerProvince']
                item['registerCity'] = content['registerCity']
                item['regAdrAgg'] = content['regAdrAgg']
                item['fundCount'] = content['fundCount']
                item['fundScale'] = content['fundScale']
                item['paidInCapital'] = content['paidInCapital']
                item['subscribedCapital'] = content['subscribedCapital']
                item['hasSpecialTips'] = content['hasSpecialTips']
                item['inBlacklist'] = content['inBlacklist']
                item['hasCreditTips'] = content['hasCreditTips']
                item['regCoordinate'] = content['regCoordinate']
                item['officeCoordinate'] = content['officeCoordinate']
                item['officeAddress'] = content['officeAddress']
                item['officeProvince'] = content['officeProvince']
                item['officeCity'] = content['officeCity']
                item['primaryInvestType'] = content['primaryInvestType']
                if item['id'] is not None:
                    yield self.get_manager_detail(item)
                yield item

            yield self.get_manager(page=page+1)

    def get_manager_detail(self, item):
        url = settings.AMAC_MANAGER_DETAIL_URL +  item['id'] + '.html';

        #url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000001709.html';
        value = {}
        return scrapy.FormRequest(url=url,meta={'manager':item}, callback=self.cb_get_manager_detail)

    def cb_get_manager_detail(self, response):

        item = AmacManagerDetailItem()

        td_table = response.xpath("//div[@class='g-container']/div[@class='g-body']/div[@class='m-manager-list m-list-details']/table[@class='table table-center table-info']/tbody/tr").extract()
        for td in  td_table:
            re.sub("</?a[^>]*>","",td)
        result = ",".join(td_table).replace("\r", "").replace("%", "").replace("\n","")


        manager = response.meta['manager']
        # item['id'] =  content['id']
        item['managerId'] = manager['id']
        item['managerNameC'] =  manager['managerName']
        item['managerNameE'] = self.getData(u'基金管理人全称\(英文\)',result)
        item['orgCode'] = self.getData(u'组织机构代码', result)
        item['registerAddress'] = self.getData(u'注册地址', result)
        item['officeAddress'] = self.getData(u'办公地址', result)

        item['registerCapital'] = self.getData(u'注册资本\(万元\)\(人民币\)', result).replace(',','') if self.getData(u'注册资本\(万元\)\(人民币\)', result) != None else None
        item['paidCapital'] = self.getData(u'实缴资本\(万元\)\(人民币\)', result).replace(',','') if self.getData(u'实缴资本\(万元\)\(人民币\)', result) != None else None
        item['registerCapitalUsd'] = self.getData(u'实缴资本\(万元\)\(美元\)', result).replace(',','') if self.getData(u'实缴资本\(万元\)\(美元\)', result) != None else None
        item['paidCapitalUsd'] = self.getData(u'实缴资本\(万元\)\(美元\)', result).replace(',','') if self.getData(u'实缴资本\(万元\)\(美元\)', result) != None else None

        item['paidCapitalRatio'] =self.getData(u'注册资本实缴比例', result).replace(' ','')
        item['enterpriseNature'] =self.getData(u'企业性质', result)
        item['primaryInvestType'] =self.getData(u'机构类型', result)
        item['otherBusinessApplications'] = self.getData(u'申请的其他业务类型', result)
        item['employeesNumbe'] = self.getData(u'员工人数', result)
        item['orgUrl'] = self.getData(u'机构网址', result)
        item['member'] =1 if self.getData(u'是否为会员', result)==u'是' else 0
        item['memberType'] = self.getData(u'当前会员类型', result)
        item['joinTime'] = self.getData(u'入会时间', result)
        item['legalOpinion']= self.getData(u'法律意见书状态', result)
        item['lawOffice']= self.getData(u'律师事务所名称', result)
        item['lawyer']= self.getData(u'律师姓名', result)
        item['manageScalaZero'] = manager['fundScale'] == 0

        item['oneYearManageScalaZero'] = 0 if item['manageScalaZero'] and (
                (time.time() - manager['establishDate'] / 1000) / (60 * 60 * 24)) > 365 else 1
        item['handInUnderRegister25'] = item['paidCapital'] != None and item['paidCapital'] < 25
        item['handInLe100w'] = item['paidCapital'] != None and item['paidCapital'] < 100
        #item['legalOpinion']= self.getData(u'法律意见书状态', result)
        item['riskControlManaer'] = ''
        item['generalManager'] = ''
        item['legalRepresentative'] =''
        bs = BeautifulSoup(self.getManageData(u'高管情况', result),'lxml')
        ggxx= bs.select('tr td')
        for index in range(len(ggxx)):
            if u'法定代表人' in ggxx[index].get_text():
                item['legalRepresentative'] = ggxx[index - 1].get_text()
            elif u"合规风控" in ggxx[index].get_text():
                item['riskControlManaer'] = ggxx[index - 1].get_text()
            elif u'总经理' in ggxx[index].get_text():
                item['generalManager'] = item['generalManager'] + ggxx[index - 1].get_text()

        #未匹配的的字段初始化
        item['fundScale1'] = 0
        item['fundScale2'] = 0
        item['fundScale3'] = 0
        item['fundScale4'] = 0
        item['fundScale5'] = 0
        item['faithInfo1'] = u'确认该机构处于失联(异常)状态' in result
        item['faithInfo2'] = u'异常原因：' in result
        item['faithInfo3'] = u'虚假填报：' in result
        item['faithInfo4'] = u'重大遗漏：' in result
        item['faithInfo5'] = u'违反八条底线内容：' in result
        item['faithInfo6'] = u'相关主体存在的不良诚信记录：' in result
        item['noQualifications'] = 'namesStr.push' in result
        item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield item

    def get_fund(self,page):
        url = settings.AMAC_FUND_URL + '?rand=' + str(random.random()) + '&page=' + str(page) + '&size=100';
        value = {}
        return scrapy.FormRequest(url=url, headers=self.headers, method='POST', body=json.dumps(value),
                                  callback=self.cb_get_fund, meta={'page': page})

    def cb_get_fund(self,response):
        datas = json.loads(response.body)
        page = response.meta['page']
        print("now page = %s" % page)
        if datas:
            if page >= datas['totalPages']:
                return
            for content in datas['content']:
                item = FundItem()
                item['fundId'] = content['id']
                item['fundName'] = content['fundName']
                item['managerName'] = content['managerName']
                establishDate= content['establishDate']
                if establishDate==None or establishDate=='':
                    item['establishDate']=None
                else:
                    item['establishDate'] =  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(establishDate/1000.0))
                item['putOnRecordDate'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(content['putOnRecordDate']/1000.0))
                item['lastQuarterUpdate'] = content['lastQuarterUpdate']
                item['containClassification'] = "分级" in content['fundName']
                item['containStructured'] = "结构化" in content['fundName']
                item['url'] = content['url']
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if item['fundId'] is not None:
                    yield self.get_fund_detail(item)
                yield item

            yield self.get_fund(page=page + 1)

    def get_fund_detail(self,item):
        url = settings.AMAC_FUND_DETAIL_URL + item['url']

        # url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000001709.html';
        value = {}
        return scrapy.FormRequest(url=url, meta={'fund': item}, callback=self.cb_get_fund_detail)

    def cb_get_fund_detail(self,response):

        bs = BeautifulSoup(response.body,'lxml',from_encoding='utf-8')
        item = FundDetailItem()
        fund = response.meta['fund']
        contents = bs.find_all('td', class_="td-content")
        item['fundId']=fund['fundId']
        item['fundNo']=contents[1].get_text()
        item['establishDate']=fund['establishDate']
        item['putOnRecordDate']=fund['putOnRecordDate']
        item['putOnRecordPhase']=contents[4].get_text() == u'暂行办法实施后成立的基金'
        item['fundType']=contents[5].get_text()
        item['currency']=contents[6].get_text()

        mType = contents[8].get_text()
        if mType ==u'受托管理':
            item['managerType'] = 1
        elif mType ==u'自我管理':
            item['managerType'] = 2
        elif mType ==u'顾问管理':
            item['managerType'] = 3

        item['trusteeName']=contents[7].get_text()
        item['mainInvestment']=None
        workingState=contents[11].get_text()
        print workingState
        if workingState ==u'正在运作':
            item['workingState'] = 1
        elif workingState ==u'正常清算':
            item['workingState'] = 2
        elif workingState ==u'提前清算':
            item['workingState'] = 3
        elif workingState ==u'延期清算':
            item['workingState'] = 4
        elif workingState ==u'投顾协议已终止':
            item['workingState'] = 5

        item['lastUpdated']=contents[12].get_text() if contents[11].get_text()!='' else None
        item['specialNote']=contents[12].get_text()
        item['informationDisclosure']=contents[13].get_text()+contents[14].get_text()+contents[15].get_text()+contents[16].get_text()
        item['createTimestamp']= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['updateTimestamp']= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield item

    def get_fund_acount(self, page):
        url = settings.AMAC_FUND_ACCOUNT_URL + '?rand=' + str(random.random()) + '&page=' + str(page) + '&size=100';
        value = {}
        return scrapy.FormRequest(url=url, headers=self.headers, method='POST', body=json.dumps(value),
                                  callback=self.cb_get_fund_acount, meta={'page': page})

    def cb_get_fund_acount(self,response):
        datas = json.loads(response.body)
        page = response.meta['page']
        print("now page = %s" % page)
        if datas:
            if page >= datas['totalPages']:
                return
            for content in datas['content']:
                item = FundAccountItem()
                item['fundAccountId'] = content['id']
                item['name'] = content['name']
                item['manager'] = content['manager']
                item['type'] = content['type']
                item['registerCode'] = content['registerCode']
                item['registerDate'] =time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime(content['registerDate'] / 1000.0))
                if content['type'] is None or content['type'] == "一对多":
                    item['url'] = content['id']+".html"
                    yield self.get_fund_account_detail(item)

                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #print item
                yield item

            yield self.get_fund_acount(page=page + 1)

    def get_fund_account_detail(self, item):
        url = settings.AMAC_FUND_ACCOUNT_DETAIL_URL + item['url']

        # url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000001709.html';
        value = {}
        return scrapy.FormRequest(url=url, meta={'fund_account': item}, callback=self.cb_get_fund_account_detail)

    def cb_get_fund_account_detail(self,response):
        bs = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        contents = bs.find_all('td', class_="td-content")
        item = FundAccountDetailItem()
        fund_account = response.meta['fund_account']
        item['fundAccountId'] = fund_account['fundAccountId']
        item['registerCode']= fund_account['registerCode']
        item['manager']= fund_account['manager']
        item['trusteeName']=contents[2].get_text()
        item['registerDate']= fund_account['registerDate']
        item['contractPeriod']=contents[5].get_text()
        item['initialScale']=self.formatDate(contents[6].get_text())
        item['classification']=contents[6].get_text() ==u'是'
        item['investorsNumber']=contents[8].get_text()
        item['otherProductType']=self.getData(u'非专项资产管理计划产品类型',response.body) if self.getData(u'非专项资产管理计划产品类型',response.body) != None else None
        item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield item

    def get_hmd(self):
        url = settings.AMAC_HMD_URL

        # url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000001709.html';
        value = {}
        return scrapy.FormRequest(url=url,  callback=self.cb_get_hmd)

    def get_hmd_detail(self,item):
        url = settings.AMAC_HMD_URL + item

        # url = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000001709.html';
        #value = {}
        return scrapy.FormRequest(url=url, callback=self.cb_get_hmd_detail)

    def cb_get_hmd(self,response):
        bs = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        contents = bs.select('div[class="newsName"] a')
        for content in contents:
            url = content['href'].split('/')[-1]
            if url is not None:
                yield self.get_hmd_detail(url)

    def cb_get_hmd_detail(self,response):
        bs = BeautifulSoup(response.body, 'html.parser', from_encoding='utf-8')
        item = HmdItem()
        contents_tr = bs.select('tbody tr td')
        contents_td = bs.select('tbody tr')
        if contents_td is not None and contents_tr is not None:
            length = len(contents_tr)/len(contents_td)
            #print(contents_td)
            t = length
            if length == 3:
                for index in range(len(contents_td)-1):
                    if t < len(contents_tr):
                        item['organization'] =None
                        item['name'] = self.formatDate(contents_tr[t+1].get_text())
                        item['disciplinary'] =self.formatDate( contents_tr[t+2].get_text())
                        time_str = self.formatDate(contents_tr[t].get_text()).replace("\t", "")
                        time_str = "".join(time_str.split())
                        time_1 = time.strptime(time_str, '%Y/%m/%d')
                        time_2 = time.strftime("%Y-%m-%d", time_1)
                        item['revocationTime'] = time_2
                        item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        yield item
                        t= (index+2)*length
            elif length == 4:
                for index in range(len(contents_td)-1):
                    if t < len(contents_tr):
                        item['name'] = self.formatDate(contents_tr[t+1].get_text()).replace("\t","")
                        item['disciplinary'] =self.formatDate( contents_tr[t+3].get_text()).replace("\t","")
                        item['organization'] =self.formatDate( contents_tr[t+2].get_text()).replace("\t","")
                        time_str =(self.formatDate(contents_tr[t].get_text()).replace("\t", ""))
                        #print time_str
                        time_str1="".join(time_str.split())
                        #print time_str1
                        time_1 =time.strptime(time_str1, '%Y/%m/%d')
                        time_2 = time.strftime("%Y-%m-%d",time_1)
                        item['revocationTime'] = time_2
                        item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        yield item
                        t= (index+2)*length

    def get_cxdj(self):
        url = settings.AMAC_CXDJ_URL
        value = {}
        return scrapy.FormRequest(url=url,  callback=self.cb_get_cxdj)

    def cb_get_cxdj(self,response):
        bs = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        contents = bs.select('div[class="newsName"] a')
        for content in contents:
            url = content['href'].split('/')[-1]
            if url is not None:
                yield self.get_cxdj_detail(url)

    def get_cxdj_detail(self,item):
        url = settings.AMAC_CXDJ_URL + item

        return scrapy.FormRequest(url=url, callback=self.cb_get_cxdj_detail)

    def cb_get_cxdj_detail(self,response):
        bs = BeautifulSoup(response.body, 'html.parser', from_encoding='utf-8')
        item = CXDJItem()
        contents_tr = bs.select('tbody tr td')
        contents_td = bs.select('tbody tr')
        if contents_td is not None and contents_tr is not None:
            length = len(contents_tr) / len(contents_td)
            # print(contents_td)
            t = length
            if length == 3:
                for index in range(len(contents_td) - 1):
                    if t < len(contents_tr):
                        item['organization'] = self.formatDate(contents_tr[t + 1].get_text())
                        item['disciplinary'] = self.formatDate(contents_tr[t + 2].get_text())
                        time_str = self.formatDate(contents_tr[t].get_text()).replace("\t", "")
                        time_str = "".join(time_str.split())
                        time_1 = time.strptime(time_str, '%Y/%m/%d')
                        time_2 = time.strftime("%Y-%m-%d", time_1)
                        item['revocationTime'] = time_2
                        item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        yield item
                        t = (index + 2) * length

    def get_zq_item(self,page):
        url = settings.AMAC_ZQ_URL + '?page.pageNo=' + str(page) + '&page.pageSize=200&filter_LIKES_CPMC=' \
                                                                   '&filter_LIKES_GLJG=&filter_LIKES_CPBM=' \
                                                                   '&filter_GES_SLRQ=&filter_LES_SLRQ=' \
                                                                   '&page.searchFileName=publicity_web' \
                                                                   '&page.sqlKey=PAGE_PUBLICITY_WEB' \
                                                                   '&page.sqlCKey=SIZE_PUBLICITY_WEB' \
                                                                   '&_search=false' \
                                                                   '&nd=&page.orderBy=SLRQ&page.order=desc';

        return scrapy.FormRequest(url=url, headers=self.headers_user, method='POST',
                                  callback=self.cb_zq_item, meta={'page': page})

    def get_qh_item(self,page):
        url = settings.AMAC_QH_URL + '?page.pageNo=' + str(page) + '&page.pageSize=200' \
                                                                   '&filter_LIKES_MPI_NAME=' \
                                                                   '&filter_LIKES_AOI_NAME' \
                                                                   '&filter_LIKES_MPI_PRODUCT_CODE=' \
                                                                   '&filter_GES_MPI_CREATE_DATE=' \
                                                                   '&filter_LES_MPI_CREATE_DATE=' \
                                                                   '&page.searchFileName=publicity_web' \
                                                                   '&page.sqlKey=PAGE_QH_PUBLICITY_WEB' \
                                                                   '&page.sqlCKey=SIZE_QH_PUBLICITY_WEB' \
                                                                   '&_search=false&nd=1525249057557' \
                                                                   '&page.orderBy=MPI_CREATE_DATE&page.order=desc'

        return scrapy.FormRequest(url=url, headers=self.headers_user, method='POST',
                                  callback=self.cb_qh_item, meta={'page': page})

    def cb_zq_item(self,response):
        datas = json.loads(response.body)
        page = response.meta['page']
        print("now page = %s" % page)
        if datas:
            if 'false' == datas['hasNext']:
                return
            for content in datas['result']:
                item = ZQ()
                item['mpiId'] = content['MPI_ID']
                item['productCode'] = content['CPBM']
                item['productName'] = content['CPMC']
                item['managerName'] = content['GLJG']
                item['createDate'] = content['SLRQ']
                item['containClassification'] = u'分级' in item['productName']
                item['containStructured'] = u'结构化' in item['productName']
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if item['mpiId'] is not None:
                    yield self.get_zq_detail(item)
                yield item

            yield self.get_zq_item(page=page + 1)

    def cb_qh_item(self,response):
        datas = json.loads(response.body)
        page = response.meta['page']
        print("now page = %s" % page)
        if datas:
            if 'false' == datas['hasNext']:
                return
            for content in datas['result']:
                item = QHItem()
                item['mpiId'] = content['MPI_ID']
                item['mpiProductCode'] = content['MPI_PRODUCT_CODE']
                item['mpiName'] = content['MPI_NAME']
                item['aoiName'] = content['AOI_NAME']
                item['mpiCreateDate'] = content['MPI_CREATE_DATE']
                item['containClassification'] = u'分级' in item['mpiName']
                item['containStructured'] = u'结构化' in item['mpiName']
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if item['mpiId'] is not None:
                    yield self.get_qh_detail(item)
                yield item

            yield self.get_zq_item(page=page + 1)

    def get_zq_detail(self,item):
        url = settings.AMAC_ZQ_DETAIL_URL + '?filter_EQS_MPI_ID=' + item['mpiId']+'&sqlkey=publicity_web&sqlval=GET_PUBLICITY_WEB_BY_MPI_ID'

        return scrapy.FormRequest(url=url, headers=self.headers_user, method='POST',
                                  callback=self.cb_get_zq_detail)

    def get_qh_detail(self,item):
        url = settings.AMAC_QH_DETAIL_URL + '?filter_EQS_MPI_ID=' + item['mpiId']+'&sqlkey=publicity_web&sqlval=GET_QH_WEB_BY_MPI_ID'

        return scrapy.FormRequest(url=url, headers=self.headers_user, method='POST', meta={'qh': item},
                                  callback=self.cb_get_qh_detail)

    def cb_get_zq_detail(self,response):
        datas = json.loads(response.body)
        if datas:
            for content in datas:
                item = ZQDetailItem()
                item['mpiId'] = content['MPI_ID']
                item['productCode'] = content['CPBM']
                item['managerName'] = content['GLJG']
                item['createDate'] = content['SLRQ']
                item['expiryDate'] = content['DQR']
                item['investmentType'] = content['TZLX']
                item['classification'] = 1 if content['SFFJ'] == u'是' else 0
                item['management'] = content['GLFS']
                item['establishScale'] = content['CLGM']
                item['householdsNumber'] = content['CLSCYHS']
                item['trusteeship'] = content['TGJG']
                item['sra'] = content['FEDJJG']
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                yield item

    def cb_get_qh_detail(self,response):
        datas = json.loads(response.body)
        if datas:
            qh_1 = response.meta['qh']
            for content in datas:
                item = QHItemdetail()
                item['mpiId'] = qh_1['mpiId']
                item['mpiProductCode'] = content['MPI_PRODUCT_CODE']
                item['aoiName'] = content['AOI_NAME']
                item['trusteeName'] = content['MPI_TRUSTEE']
                item['mpiCreateDate'] = content['MPI_CREATE_DATE']
                item['investmentType'] = content['TZLX']
                item['raiseScale'] = content['MPI_TOTAL_MONEY']
                item['structured'] = 1 if content['SFJGH'] == u'是' else 0
                item['principalsNumber'] = content['MPI_PARTICIPATION_USER']
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                yield item

    def getData(self,key,result):
        pattern = re.compile(key + ":?</t[dr]>[^>]*>([^<]+)")
        m = pattern.findall(result)
        if len(m):
            return m[0]
        else:
            return None

    def getManageData(self,key,result):
        pattern = re.compile(key + ':?</td>([\\s\\S]*?)(?=</table>)')
        m = pattern.findall(result)
        if len(m):
            return m[0]
            return None
        else:
            pass

    def formatDate(self,data):
        return data.replace("\r", "").replace(" ", "").replace("\n","")





