# -*- coding: utf-8 -*-
import mysql.connector,logging
import traceback
from AmacCrawler import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

mysql_connector = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
mysql_cursor = mysql_connector.cursor()


class DataBases:
    @classmethod
    def insert_amac_manager(cls, manager_id, manager_name_c, artificial_person_name,
                            primary_invest_type, register_province, register_no,
                            establish_date, register_date, url, fundScale,
                            fundCount, create_timestamp, update_timestamp):
        sql = 'INSERT INTO manager (`manager_id`, `manager_name_c`, `artificial_person_name`, `primary_invest_type`, `register_province`, `register_no`, `establish_date`, `register_date`, `url`, `fundScale`, `fundCount`, `create_timestamp`, `update_timestamp`) VALUES ' \
              '(%(manager_id)s, %(manager_name_c)s, %(artificial_person_name)s, %(primary_invest_type)s, %(register_province)s, %(register_no)s, %(establish_date)s, %(register_date)s, %(url)s, %(fundScale)s, %(fundCount)s, %(create_timestamp)s, %(update_timestamp)s)'

        value = {
            'manager_id': manager_id,
            'manager_name_c': manager_name_c,
            'artificial_person_name': artificial_person_name,
            'primary_invest_type': primary_invest_type,
            'register_province': register_province,
            'register_no': register_no,
            'establish_date': establish_date,
            'register_date': register_date,
            'url': url,
            'fundScale': fundScale,
            'fundCount': fundCount,
            'create_timestamp': create_timestamp,
            'update_timestamp': update_timestamp
        }
        mysql_cursor.execute(sql, value)
        mysql_connector.commit()

    @classmethod
    def insert_amac_manager_detail(cls, item):

        insert_sql ='INSERT INTO manager_detail (manager_id, manager_name_c, manager_name_e, ' \
                    'org_code, register_address, office_address, register_capital, paid_capital, register_' \
                    'capital_usd, paid_capital_usd, paid_capital_ratio, enterprise_nature, primary_invest_type,' \
                    ' other_business_applications, employees_number, org_url, member, member_type, join_time,' \
                    ' legal_opinion, law_office, lawyer, manage_scala_zero, one_year_manage_scala_zero,' \
                    ' hand_in_under_register_25p, hand_in_le_100w, fund_scale_1, fund_scale_2, fund_scale_3,' \
                    ' fund_scale_4, fund_scale_5, faith_info_1, faith_info_2, faith_info_3, faith_info_4,' \
                    ' faith_info_5, faith_info_6, no_qualifications, legal_representative, general_manager, ' \
                    'risk_control_manager, create_timestamp, update_timestamp) ' \
                    'VALUES ' \
                    '(%(manager_id)s, %(manager_name_c)s, %(manager_name_e)s, %(org_code)s, ' \
                    '%(register_address)s, %(office_address)s, %(register_capital)s, %(paid_capital)s, ' \
                    '%(register_capital_usd)s, %(paid_capital_usd)s, %(paid_capital_ratio)s, %(enterprise_nature)s, ' \
                    '%(primary_invest_type)s, %(other_business_applications)s, %(employees_number)s, %(org_url)s,' \
                    ' %(member)s, %(member_type)s, %(join_time)s, %(legal_opinion)s, %(law_office)s, %(lawyer)s, ' \
                    '%(manage_scala_zero)s, %(one_year_manage_scala_zero)s, %(hand_in_under_register_25p)s, ' \
                    '%(hand_in_le_100w)s, %(fund_scale_1)s, %(fund_scale_2)s, %(fund_scale_3)s, %(fund_scale_4)s, ' \
                    '%(fund_scale_5)s, %(faith_info_1)s, %(faith_info_2)s, %(faith_info_3)s, %(faith_info_4)s, ' \
                    '%(faith_info_5)s, %(faith_info_6)s, %(no_qualifications)s, %(legal_representative)s, ' \
                    '%(general_manager)s, %(risk_control_manager)s, %(create_timestamp)s, %(update_timestamp)s);'
        value = {
            'manager_id': item['managerId'],
            'manager_name_c': item['managerNameC'],
            'manager_name_e': item['managerNameE'],
            'org_code': item['orgCode'],
            'register_address': item['registerAddress'],
            'office_address': item['officeAddress'],
            'register_capital': item['registerCapital'],
            'paid_capital': item['paidCapital'],
            'register_capital_usd': item['registerCapitalUsd'],
            'paid_capital_usd': item['paidCapitalUsd'],
            'paid_capital_ratio': item['paidCapitalRatio'],
            'enterprise_nature': item['enterpriseNature'],
            'primary_invest_type': item['primaryInvestType'],
            'other_business_applications': item['otherBusinessApplications'],
            'employees_number': item['employeesNumbe'],
            'org_url': item['orgUrl'],
            'member': item['member'],
            'member_type': item['memberType'],
            'join_time': item['joinTime'],
            'legal_opinion': item['legalOpinion'],
            'law_office': item['lawOffice'],
            'lawyer': item['lawyer'],
            'manage_scala_zero': item['manageScalaZero'],
            'one_year_manage_scala_zero': item['oneYearManageScalaZero'],
            'hand_in_under_register_25p': item['handInUnderRegister25'],
            'hand_in_le_100w': item['handInLe100w'],
            'fund_scale_1': item['fundScale1'],
            'fund_scale_2': item['fundScale2'],
            'fund_scale_3': item['fundScale3'],
            'fund_scale_4': item['fundScale4'],
            'fund_scale_5': item['fundScale5'],
            'faith_info_1': item['faithInfo1'],
            'faith_info_2': item['faithInfo2'],
            'faith_info_3': item['faithInfo3'],
            'faith_info_4': item['faithInfo4'],
            'faith_info_5': item['faithInfo5'],
            'faith_info_6': item['faithInfo6'],
            'no_qualifications': item['noQualifications'],
            'legal_representative': item['legalRepresentative'],
            'general_manager': item['generalManager'],
            'risk_control_manager': item['riskControlManaer'],
            'create_timestamp': item['createTimestamp'],
            'update_timestamp':	item['updateTimestamp']
        }
        try:
            mysql_cursor.execute(insert_sql, value)
            mysql_connector.commit()
        except Exception, e:
            logging.info('insert_amac_manager_detail: 爬取个人详情页出错')
            logging.info('str(e):\t\t', str(e))
            logging.info('traceback.print_exc():', traceback.print_exc())

    @classmethod
    def insert_amac_fund(cls, item):

        insert_sql ='INSERT INTO fund ' \
                    '(fund_id, fund_name, manager_name, establish_date, put_on_record_date, last_quarter_update, ' \
                    'contain_classification, contain_structured, url, create_timestamp, update_timestamp) ' \
                    'VALUES (%(fund_id)s, %(fund_name)s, %(manager_name)s, %(establish_date)s, ' \
                    '%(put_on_record_date)s, %(last_quarter_update)s, %(contain_classification)s, ' \
                    '%(contain_structured)s, %(url)s, %(create_timestamp)s, %(update_timestamp)s)'
        value = {
            'fund_id' : item['fundId'],
            'fund_name' : item['fundName'],
            'manager_name' : item['managerName'],
            'establish_date' : item['establishDate'],
            'put_on_record_date' : item['putOnRecordDate'],
            'last_quarter_update' : item['lastQuarterUpdate'],
            'contain_classification' : item['containClassification'],
            'contain_structured' : item['containStructured'],
            'url' : item['url'],
            'create_timestamp' : item['createTimestamp'],
            'update_timestamp' : item['updateTimestamp']

        }
        try:
            mysql_cursor.execute(insert_sql, value)
            mysql_connector.commit()
        except Exception, e:
            logging.info('insert_amac_fund: 插入基金出错')
            logging.info('str(e):\t\t', str(e))
            logging.info('traceback.print_exc():', traceback.print_exc())

    @classmethod
    def insert_fund_account(cls, item):

        insert_sql = 'INSERT INTO fund_account (fund_account_id, name, manager, type, register_code, register_date, url,' \
                     ' create_timestamp, update_timestamp) ' \
                     'VALUES ' \
                     '(%(fund_account_id)s, %(name)s, %(manager)s, %(type)s, %(register_code)s, %(register_date)s, ' \
                     '%(url)s, %(create_timestamp)s, %(update_timestamp)s)'
        value = {
            'fund_account_id': item['fundAccountId'],
            'name': item['name'],
            'manager': item['manager'],
            'type': item['type'],
            'register_code': item['registerCode'],
            'register_date': item['registerDate'],
            'url': item['url'],
            'create_timestamp': item['createTimestamp'],
            'update_timestamp' : item['updateTimestamp']

        }
        try:
            mysql_cursor.execute(insert_sql, value)
            mysql_connector.commit()
        except Exception, e:
            logging.info('insert_amac_fund: 爬取-插入基金账户出错')
            logging.info('str(e):\t\t', str(e))
            logging.info('traceback.print_exc():', traceback.print_exc())

    @classmethod
    def insert_fund_detail(cls, item):
        insert_sql='INSERT INTO fund_detail (fund_id, fund_no, establish_date, put_on_record_date, ' \
                   'put_on_record_phase, fund_type, currency, manager_type, trustee_name, main_investment, ' \
                   'working_state, last_updated, special_note, information_disclosure, create_timestamp, update_timestamp) ' \
                   'VALUES ' \
                   '(%(fund_id)s, %(fund_no)s, %(establish_date)s, %(put_on_record_date)s, %(put_on_record_phase)s, ' \
                   '%(fund_type)s, %(currency)s, %(manager_type)s, %(trustee_name)s, %(main_investment)s, ' \
                   '%(working_state)s, %(last_updated)s, %(special_note)s, %(information_disclosure)s, ' \
                   '%(create_timestamp)s, %(update_timestamp)s)'
        value = {
            'fund_id': item['fundId'],
            'fund_no': item['fundNo'],
            'establish_date': item['establishDate'],
            'put_on_record_date': item['putOnRecordDate'],
            'put_on_record_phase': item['putOnRecordPhase'],
            'fund_type': item['fundType'],
            'currency': item['currency'],
            'manager_type': item['managerType'],
            'trustee_name': item['trusteeName'],
            'main_investment': item['mainInvestment'],
            'working_state': item['workingState'],
            'last_updated': item['lastUpdated'],
            'special_note': item['specialNote'],
            'information_disclosure': item['informationDisclosure'],
            'create_timestamp': item['createTimestamp'],
            'update_timestamp': item['updateTimestamp']
         }
        try:
            mysql_cursor.execute(insert_sql, value)
            mysql_connector.commit()
        except Exception, e:
            logging.info('insert_amac_fund: 爬取-插入基金详情页面出错')
            logging.info('str(e):\t\t', str(e))
            logging.info('traceback.print_exc():', traceback.print_exc())

    @classmethod
    def insert_fund_account_detail(cls, item):
        insert_sql = 'INSERT INTO fund_account_detail (fund_account_id, register_code, manager, trustee_name, ' \
                     'register_date, contract_period, initial_scale, classification, investors_number, ' \
                     'other_product_type, create_timestamp, update_timestamp) ' \
                     'VALUES ' \
                     '(%(fund_account_id)s, %(register_code)s, %(manager)s, %(trustee_name)s, %(register_date)s, ' \
                     '%(contract_period)s, %(initial_scale)s, %(classification)s, %(investors_number)s, ' \
                     '%(other_product_type)s, %(create_timestamp)s, %(update_timestamp)s)'
        value = {
            'fund_account_id': item['fundAccountId'],
            'register_code': item['registerCode'],
            'manager': item['manager'],
            'trustee_name': item['trusteeName'],
            'register_date': item['registerDate'],
            'contract_period': item['contractPeriod'],
            'initial_scale': item['initialScale'],
            'classification': item['classification'],
            'investors_number': item['investorsNumber'],
            'other_product_type': item['otherProductType'],
            'create_timestamp': item['createTimestamp'],
            'update_timestamp': item['updateTimestamp']
        }
        try:
            mysql_cursor.execute(insert_sql, value)
            mysql_connector.commit()
        except Exception, e:
            logging.info('insert_fund_account_detail: 爬取-插入基金账户详情页面出错')
            logging.info('str(e):\t\t', str(e))
            logging.info('traceback.print_exc():', traceback.print_exc())

    @classmethod
    def insert_hmd_item(cls, item):
        insert_sql = 'INSERT INTO hmd ( name, organization, disciplinary, revocation_time, create_timestamp, update_timestamp) ' \
                     'VALUES ( %(name)s, %(organization)s, %(disciplinary)s, %(revocation_time)s, ' \
                     '%(create_timestamp)s, %(update_timestamp)s)'
        value = {
            'name' : item['name'],
            'organization' : item['organization'],
            'disciplinary' : item['disciplinary'],
            'revocation_time' : item['revocationTime'],
            'create_timestamp' : item['createTimestamp'],
            'update_timestamp' : item['updateTimestamp']

        }
        try:
            mysql_cursor.execute(insert_sql, value)
            mysql_connector.commit()
        except Exception, e:
            logging.info('insert_hmd_item: 爬取-黑名单出错')
            logging.info('str(e):\t\t', str(e))
            logging.info('traceback.print_exc():', traceback.print_exc())
