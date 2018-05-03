# -*- coding: utf-8 -*-

# Scrapy settings for AmacCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AmacCrawler'

SPIDER_MODULES = ['AmacCrawler.spiders']
NEWSPIDER_MODULE = 'AmacCrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AmacCrawler.middlewares.AmaccrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'AmacCrawler.middlewares.AmaccrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
        'AmacCrawler.mysqlpipelines.pipelines.AmacPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOSTS = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'amac'

# AMAC url
# 撤销登记
AMAC_CXDJ_URL = 'http://www.amac.org.cn/xxgs/cxdj/'
# 基金专户产品数据
AMAC_FUND_ACCOUNT_URL = 'http://gs.amac.org.cn/amac-infodisc/api/fund/account'
# 基金专户产品详情
AMAC_FUND_ACCOUNT_DETAIL_URL = 'http://gs.amac.org.cn/amac-infodisc/res/fund/account/'
# 私募基金数据
AMAC_FUND_URL = 'http://gs.amac.org.cn/amac-infodisc/api/pof/fund'
# 私募基金数据详情
AMAC_FUND_DETAIL_URL = 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/'
# 私募基金管理人从业黑名单
AMAC_HMD_URL = 'http://www.amac.org.cn/xxgs/hmd/'
# 私募基金管理人
AMAC_MANAGER_URL = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager'
# 私募基金管理人详情
AMAC_MANAGER_DETAIL_URL = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/'
# 证券
AMAC_ZQ_URL = 'http://ba.amac.org.cn/pages/amacWeb/user!list.action'
# 证券详情
AMAC_ZQ_DETAIL_URL = 'http://ba.amac.org.cn/pages/amacWeb/user!search.action'
# 期货
AMAC_QH_URL = 'http://ba.amac.org.cn/pages/amacWeb/user!list.action'
#期货详情页
AMAC_QH_DETAIL_URL = 'http://ba.amac.org.cn/pages/amacWeb/user!search.action'


