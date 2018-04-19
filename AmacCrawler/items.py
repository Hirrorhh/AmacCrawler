# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmaccrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AmacManagerItem(scrapy.Item):
    id = scrapy.Field()
    managerName = scrapy.Field()
    artificialPersonName = scrapy.Field()
    registerNo = scrapy.Field()
    establishDate = scrapy.Field()
    managerHasProduct = scrapy.Field()
    url = scrapy.Field()
    registerDate = scrapy.Field()
    registerAddress = scrapy.Field()
    registerProvince = scrapy.Field()
    registerCity = scrapy.Field()
    regAdrAgg = scrapy.Field()
    fundCount = scrapy.Field()
    fundScale = scrapy.Field()
    paidInCapital = scrapy.Field()
    subscribedCapital = scrapy.Field()
    hasSpecialTips = scrapy.Field()
    inBlacklist = scrapy.Field()
    hasCreditTips = scrapy.Field()
    regCoordinate = scrapy.Field()
    officeCoordinate = scrapy.Field()
    officeAddress = scrapy.Field()
    officeProvince = scrapy.Field()
    officeCity = scrapy.Field()
    primaryInvestType = scrapy.Field()

class AmacManagerDetailItem(scrapy.Item):
    id = scrapy.Field()
    managerId = scrapy.Field()
    managerNameC = scrapy.Field()
    managerNameE = scrapy.Field()
    orgCode = scrapy.Field()
    registerAddress = scrapy.Field()
    officeAddress = scrapy.Field()
    registerCapital = scrapy.Field()
    paidCapital = scrapy.Field()
    registerCapitalUsd = scrapy.Field()
    paidCapitalUsd = scrapy.Field()
    paidCapitalRatio = scrapy.Field()
    enterpriseNature = scrapy.Field()
    primaryInvestType = scrapy.Field()
    otherBusinessApplications = scrapy.Field()
    employeesNumbe = scrapy.Field()
    orgUrl = scrapy.Field()
    member = scrapy.Field()
    memberType = scrapy.Field()
    joinTime = scrapy.Field()
    legalOpinion = scrapy.Field()
    lawOffice = scrapy.Field()
    lawyer = scrapy.Field()
    manageScalaZero = scrapy.Field()
    oneYearManageScalaZero = scrapy.Field()
    handInUnderRegister25 = scrapy.Field()
    handInLe100w = scrapy.Field()
    fundScale1 = scrapy.Field()
    fundScale2 = scrapy.Field()
    fundScale3 = scrapy.Field()
    fundScale4 = scrapy.Field()
    fundScale5 = scrapy.Field()
    faithInfo1 = scrapy.Field()
    faithInfo2 = scrapy.Field()
    faithInfo3 = scrapy.Field()
    faithInfo4 = scrapy.Field()
    faithInfo5 = scrapy.Field()
    faithInfo6 = scrapy.Field()
    noQualifications = scrapy.Field()
    legalRepresentative = scrapy.Field()
    generalManager = scrapy.Field()
    riskControlManaer = scrapy.Field()
    createTimestamp = scrapy.Field()
    updateTimestamp = scrapy.Field()
class FundItem(scrapy.Item):
    id = scrapy.Field()
    fundId = scrapy.Field()
    fundName = scrapy.Field()
    managerName = scrapy.Field()
    establishDate = scrapy.Field()
    putOnRecordDate = scrapy.Field()
    lastQuarterUpdate = scrapy.Field()
    containClassification = scrapy.Field()
    containStructured = scrapy.Field()
    url = scrapy.Field()
    createTimestamp = scrapy.Field()
    updateTimestamp = scrapy.Field()

class FundAccountItem(scrapy.Item):
    id = scrapy.Field()
    fundAccountId = scrapy.Field()
    name = scrapy.Field()
    manager = scrapy.Field()
    type = scrapy.Field()
    registerCode = scrapy.Field()
    registerDate = scrapy.Field()
    url = scrapy.Field()
    createTimestamp = scrapy.Field()
    updateTimestamp = scrapy.Field()