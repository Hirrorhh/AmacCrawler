# -*- coding: utf-8 -*-
import datetime
import time
from AmacCrawler.items import AmacManagerItem, AmacManagerDetailItem,FundItem,FundAccountItem,AmacManagerDetailItem,\
    FundDetailItem
from AmacCrawler.mysqlpipelines.databases import DataBases


class AmacPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AmacManagerItem):
            manager_id = item['id']
            manager_name_c = item['managerName']
            artificial_person_name = item['artificialPersonName']
            register_no = item['registerNo']
            establish_timestamp = item['establishDate'] / 1000
            establish_date = time.strftime("%Y-%m-%d", time.localtime(establish_timestamp))
            # item['managerHasProduct']
            url = item['url']
            register_timestamp = item['registerDate'] / 1000
            register_date = time.strftime("%Y-%m-%d", time.localtime(register_timestamp))
            # item['registerAddress']
            register_province = item['registerProvince']
            # item['registerCity']
            # item['regAdrAgg']
            fundCount = item['fundCount']
            fundScale = item['fundScale']
            # item['paidInCapital']
            # item['subscribedCapital']
            # item['hasSpecialTips']
            # item['inBlacklist']
            # item['hasCreditTips']
            # item['regCoordinate']
            # item['officeCoordinate']
            # item['officeAddress']
            # item['officeProvince']
            # item['officeCity']
            primary_invest_type = item['primaryInvestType']
            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            DataBases.insert_amac_manager(manager_id, manager_name_c, artificial_person_name,
                                          primary_invest_type, register_province, register_no,
                                          establish_date, register_date, url, fundScale,
                                          fundCount, otherStyleTime, otherStyleTime)

        if isinstance(item, AmacManagerDetailItem):
            DataBases.insert_amac_manager_detail(item)
        if isinstance(item, FundItem):
            DataBases.insert_amac_fund(item);
        if isinstance(item,FundAccountItem ):
            DataBases.insert_fund_account(item);
        if isinstance(item,FundDetailItem):
            DataBases.insert_fund_detail(item);

