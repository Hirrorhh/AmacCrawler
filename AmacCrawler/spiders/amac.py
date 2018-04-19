# -*- coding: utf-8 -*-
import re
import scrapy,sys,json,random,datetime,time
from bs4 import BeautifulSoup
from scrapy.http import Request

from AmacCrawler import settings
from AmacCrawler.items import AmacManagerItem,AmacManagerDetailItem,FundItem,FundAccountItem


reload(sys)
sys.setdefaultencoding('utf-8')


class Myspider(scrapy.Spider):
    name = 'amac'
    allowed_domains = ['amac.org.cn']
    bash_url = 'http://www.amac.org.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
    }

    def __init__(self, name=None, **kwargs):
        super(Myspider, self).__init__(name=None, **kwargs)
    #爬虫开始执行入口
    def start_requests(self):
        #爬取管理人信息(回调函数中爬取个人详情)
        yield self.get_manager(page=0)

        #爬取私募基金数据信息
        #yield self.get_fund(page=0)
        #爬取基金专户产品公示
        #yield self.get_fund_acount(page=0)

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
                    yield self.get_manager_detail(item);
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
                item['establishDate'] =  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(content['establishDate']/1000.0))
                item['putOnRecordDate'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(content['putOnRecordDate']/1000.0))
                item['lastQuarterUpdate'] = content['lastQuarterUpdate']
                item['containClassification'] = "分级" in content['fundName']
                item['containStructured'] = "结构化" in content['fundName']
                item['url'] = content['url']
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item

            yield self.get_fund(page=page + 1)

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
                item['createTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['updateTimestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #print item
                yield item

            yield self.get_fund_acount(page=page + 1)

    def trim_str(self):
        self

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
        else:
            return None