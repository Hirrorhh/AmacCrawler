/*
Navicat MySQL Data Transfer

Source Server         : local_root
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : amac

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2018-05-03 13:51:18
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cxdj
-- ----------------------------
DROP TABLE IF EXISTS `cxdj`;
CREATE TABLE `cxdj` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `organization` varchar(45) DEFAULT NULL,
  `disciplinary` varchar(45) DEFAULT NULL,
  `revocation_date` date DEFAULT NULL,
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fund
-- ----------------------------
DROP TABLE IF EXISTS `fund`;
CREATE TABLE `fund` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fund_id` bigint(20) DEFAULT NULL,
  `fund_name` varchar(255) DEFAULT NULL COMMENT '基金名称',
  `manager_name` varchar(45) DEFAULT NULL COMMENT '私募基金管理人名称',
  `establish_date` date DEFAULT NULL COMMENT '成立时间',
  `put_on_record_date` date DEFAULT NULL COMMENT '备案时间',
  `last_quarter_update` tinyint(1) DEFAULT NULL COMMENT '存在未进行的季度更新',
  `contain_classification` tinyint(1) DEFAULT NULL COMMENT '基金名称中是否有“分级”',
  `contain_structured` tinyint(1) DEFAULT NULL COMMENT '基金名称中是否有“结构化”',
  `url` varchar(45) DEFAULT NULL,
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1842 DEFAULT CHARSET=utf8 COMMENT='http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html';

-- ----------------------------
-- Table structure for fund_account
-- ----------------------------
DROP TABLE IF EXISTS `fund_account`;
CREATE TABLE `fund_account` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fund_account_id` varchar(45) DEFAULT NULL COMMENT '专户ID',
  `name` varchar(255) DEFAULT NULL COMMENT '专户名称',
  `manager` varchar(45) DEFAULT NULL COMMENT '管理人名称',
  `type` varchar(45) DEFAULT NULL COMMENT '专户类型',
  `register_code` varchar(45) DEFAULT NULL COMMENT '备案编码',
  `register_date` date DEFAULT NULL COMMENT '备案日期',
  `url` varchar(45) DEFAULT NULL COMMENT '“一对多”的基金专户产品链接',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1843 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fund_account_detail
-- ----------------------------
DROP TABLE IF EXISTS `fund_account_detail`;
CREATE TABLE `fund_account_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fund_account_id` varchar(45) DEFAULT NULL COMMENT '专户ID',
  `register_code` varchar(45) DEFAULT NULL COMMENT '备案编码',
  `manager` varchar(45) DEFAULT NULL COMMENT '管理人名称',
  `trustee_name` varchar(45) DEFAULT NULL COMMENT '托管人名称',
  `register_date` date DEFAULT NULL COMMENT '备案日期',
  `contract_period` varchar(450) DEFAULT NULL COMMENT '合同期限（月）',
  `initial_scale` double DEFAULT NULL COMMENT '起始规模（亿元）',
  `classification` tinyint(1) DEFAULT NULL COMMENT '是否分级',
  `investors_number` int(11) DEFAULT NULL COMMENT '成立时投资者数量',
  `other_product_type` varchar(45) DEFAULT NULL COMMENT '非专项资产管理计划产品类型',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1833 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for fund_detail
-- ----------------------------
DROP TABLE IF EXISTS `fund_detail`;
CREATE TABLE `fund_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fund_id` bigint(20) DEFAULT NULL,
  `fund_no` varchar(45) DEFAULT NULL COMMENT '基金编号',
  `establish_date` date DEFAULT NULL COMMENT '成立时间',
  `put_on_record_date` date DEFAULT NULL COMMENT '备案时间',
  `put_on_record_phase` tinyint(1) DEFAULT NULL COMMENT '基金备案阶段\n暂行办法实施前成立的基金 0、暂行办法实施后成立的基金 1',
  `fund_type` varchar(45) DEFAULT NULL COMMENT '基金类型',
  `currency` varchar(45) DEFAULT NULL COMMENT '币种',
  `manager_type` int(11) DEFAULT NULL COMMENT '管理类型\n受托管理 1、自我管理 2、顾问管理 3',
  `trustee_name` varchar(255) DEFAULT NULL COMMENT '托管人名称',
  `main_investment` varchar(2048) DEFAULT NULL COMMENT '主要投资领域',
  `working_state` int(11) DEFAULT NULL COMMENT '运作状态\n正在运作 1、延期清盘 2、提前清盘 3、正常清盘 4、非正常清盘 5',
  `last_updated` date DEFAULT NULL COMMENT '基金信息最后更新时间',
  `special_note` varchar(255) DEFAULT NULL COMMENT '基金协会特别提示（针对基金）',
  `information_disclosure` varchar(255) DEFAULT NULL COMMENT '信息披露情况',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1833 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hmd
-- ----------------------------
DROP TABLE IF EXISTS `hmd`;
CREATE TABLE `hmd` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL COMMENT '姓名',
  `organization` varchar(45) DEFAULT NULL COMMENT '任职机构及其职务',
  `disciplinary` varchar(45) DEFAULT NULL COMMENT '纪律处分',
  `revocation_time` date DEFAULT NULL COMMENT '处分日期',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for manager
-- ----------------------------
DROP TABLE IF EXISTS `manager`;
CREATE TABLE `manager` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `manager_id` bigint(20) unsigned NOT NULL,
  `manager_name_c` varchar(45) NOT NULL COMMENT '私募基金管理人名称（中文）',
  `artificial_person_name` varchar(45) DEFAULT NULL COMMENT '法定代表人/执行事务合伙人',
  `primary_invest_type` varchar(45) DEFAULT NULL COMMENT '基金主要类别',
  `register_province` varchar(45) DEFAULT NULL COMMENT '注册地',
  `register_no` varchar(45) DEFAULT NULL COMMENT '登记编号',
  `establish_date` date DEFAULT NULL COMMENT '成立时间',
  `register_date` date DEFAULT NULL COMMENT '登记时间',
  `url` varchar(255) DEFAULT NULL COMMENT '详细页面链接',
  `fundScale` double DEFAULT NULL COMMENT '资金规模（万元）',
  `fundCount` int(11) DEFAULT NULL COMMENT '正在运作的基金数量',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1823 DEFAULT CHARSET=utf8 COMMENT='http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html';

-- ----------------------------
-- Table structure for manager_detail
-- ----------------------------
DROP TABLE IF EXISTS `manager_detail`;
CREATE TABLE `manager_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `manager_id` bigint(20) DEFAULT NULL,
  `manager_name_c` varchar(45) DEFAULT NULL,
  `manager_name_e` varchar(255) DEFAULT NULL COMMENT '私募基金管理人名称（英文）',
  `org_code` varchar(45) DEFAULT NULL COMMENT '组织机构代码',
  `register_address` varchar(255) DEFAULT NULL COMMENT '注册地址',
  `office_address` varchar(255) DEFAULT NULL COMMENT '办公地址',
  `register_capital` double(55,0) DEFAULT NULL COMMENT '注册资本（万元）',
  `paid_capital` double(55,0) DEFAULT NULL COMMENT '实缴资本（万元）',
  `register_capital_usd` double DEFAULT NULL,
  `paid_capital_usd` double DEFAULT NULL,
  `paid_capital_ratio` double DEFAULT NULL COMMENT '注册资本实缴比例',
  `enterprise_nature` varchar(45) DEFAULT NULL COMMENT '企业性质',
  `primary_invest_type` varchar(45) DEFAULT NULL COMMENT '管理基金主要类别',
  `other_business_applications` varchar(255) DEFAULT NULL COMMENT '申请的其他业务类型',
  `employees_number` int(11) DEFAULT NULL COMMENT '员工人数',
  `org_url` varchar(255) DEFAULT NULL COMMENT '机构网址',
  `member` tinyint(1) DEFAULT NULL COMMENT '是否为会员',
  `member_type` varchar(45) DEFAULT NULL COMMENT '当前会员类型',
  `join_time` date DEFAULT NULL COMMENT '入会时间',
  `legal_opinion` varchar(45) DEFAULT NULL COMMENT '法律意见书状态',
  `law_office` varchar(45) DEFAULT NULL COMMENT '律师事务所',
  `lawyer` varchar(45) DEFAULT NULL COMMENT '律师',
  `manage_scala_zero` tinyint(1) DEFAULT NULL COMMENT '管理规模为零',
  `one_year_manage_scala_zero` tinyint(1) DEFAULT NULL COMMENT '登记一年以上管理规模为零',
  `hand_in_under_register_25p` tinyint(1) DEFAULT NULL COMMENT '管理人实缴资本低于注册资本25%',
  `hand_in_le_100w` tinyint(1) DEFAULT NULL COMMENT '管理人实缴资本低于100万',
  `fund_scale_1` int(11) DEFAULT NULL COMMENT '私募证券基金(自主发行)\n50亿以上 1、20-50亿 2、10-20亿 3、1-10亿 4、0-1亿 5',
  `fund_scale_2` int(11) DEFAULT NULL COMMENT '私募证券投资基金（顾问管理）\n50亿以上 1、20-50亿 2、10-20亿 3、1-10亿 4、0-1亿 5',
  `fund_scale_3` int(11) DEFAULT NULL COMMENT '私募股权基金\n100亿以上 1、50-100亿 2、20-50亿 3、0-20亿 4',
  `fund_scale_4` int(11) DEFAULT NULL COMMENT '创业投资基金\n10亿以上 1、5-10亿 2、2-5亿 3、0-2亿 4',
  `fund_scale_5` int(11) DEFAULT NULL COMMENT '其他私募基金\n10亿以上 1、5-10亿 2、2-5亿 3、0-2亿 4',
  `faith_info_1` tinyint(1) DEFAULT NULL COMMENT '失联机构',
  `faith_info_2` tinyint(1) DEFAULT NULL COMMENT '异常机构',
  `faith_info_3` tinyint(1) DEFAULT NULL COMMENT '虚假填报',
  `faith_info_4` tinyint(1) DEFAULT NULL COMMENT '重大遗漏',
  `faith_info_5` tinyint(1) DEFAULT NULL COMMENT '违反八条底线',
  `faith_info_6` tinyint(1) DEFAULT NULL COMMENT '相关主体存在不良诚信记录',
  `no_qualifications` tinyint(1) DEFAULT NULL COMMENT '高管人员无证券投资基金从业资格',
  `legal_representative` varchar(450) DEFAULT NULL COMMENT '法人',
  `general_manager` varchar(450) DEFAULT NULL COMMENT '总经理',
  `risk_control_manager` varchar(450) DEFAULT NULL COMMENT '合规风控',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1814 DEFAULT CHARSET=utf8 COMMENT='http://gs.amac.org.cn/amac-infodisc/res/pof/manager/138.html';

-- ----------------------------
-- Table structure for qh
-- ----------------------------
DROP TABLE IF EXISTS `qh`;
CREATE TABLE `qh` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mpi_id` bigint(20) DEFAULT NULL,
  `mpi_product_code` varchar(45) DEFAULT NULL COMMENT '产品编码',
  `mpi_name` varchar(45) DEFAULT NULL COMMENT '产品名称',
  `aoi_name` varchar(45) DEFAULT NULL COMMENT '管理机构',
  `mpi_create_date` date DEFAULT NULL COMMENT '设立日期',
  `contain_classification` tinyint(1) DEFAULT NULL COMMENT '产品名称中是否有 “分级”',
  `contain_structured` tinyint(1) DEFAULT NULL COMMENT '产品名称中是否有“结构化”',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=324 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for qh_detail
-- ----------------------------
DROP TABLE IF EXISTS `qh_detail`;
CREATE TABLE `qh_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mpi_id` bigint(20) DEFAULT NULL,
  `mpi_product_code` varchar(45) DEFAULT NULL COMMENT '产品编码',
  `aoi_name` varchar(45) DEFAULT NULL COMMENT '管理机构',
  `trustee_name` varchar(45) DEFAULT NULL COMMENT '托管人名称',
  `mpi_create_date` date DEFAULT NULL COMMENT '设立日期',
  `investment_type` varchar(45) DEFAULT NULL COMMENT '投资类型',
  `raise_scale` double DEFAULT NULL COMMENT '募集规模（万元）',
  `structured` tinyint(1) DEFAULT NULL COMMENT '是否结构化',
  `principals_number` int(11) DEFAULT NULL COMMENT '初始委托人数量',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=320 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for zq
-- ----------------------------
DROP TABLE IF EXISTS `zq`;
CREATE TABLE `zq` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mpi_id` bigint(20) DEFAULT NULL,
  `product_code` varchar(45) DEFAULT NULL COMMENT '产品编码',
  `product_name` varchar(255) DEFAULT NULL COMMENT '产品名称',
  `manager_name` varchar(45) DEFAULT NULL COMMENT '管理机构',
  `create_date` date DEFAULT NULL COMMENT '设立日期',
  `contain_classification` tinyint(1) DEFAULT NULL COMMENT '产品名称中是否有 “分级”',
  `contain_structured` tinyint(1) DEFAULT NULL COMMENT '产品名称中是否有“结构化”',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1825 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for zq_detail
-- ----------------------------
DROP TABLE IF EXISTS `zq_detail`;
CREATE TABLE `zq_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mpi_id` bigint(20) DEFAULT NULL,
  `product_code` varchar(45) DEFAULT NULL COMMENT '产品编码',
  `manager_name` varchar(45) DEFAULT NULL COMMENT '管理机构',
  `create_date` date DEFAULT NULL COMMENT '设立日期',
  `expiry_date` varchar(45) DEFAULT NULL COMMENT '到期日',
  `investmentType` varchar(45) DEFAULT NULL COMMENT '投资类型',
  `classification` tinyint(1) DEFAULT NULL COMMENT '是否分级',
  `management` varchar(45) DEFAULT NULL COMMENT '管理方式',
  `establish_scale` double DEFAULT NULL COMMENT '成立规模',
  `households_number` int(11) DEFAULT NULL COMMENT '成立时参与户数',
  `trusteeship` varchar(255) DEFAULT NULL COMMENT '托管机构',
  `sra` varchar(45) DEFAULT NULL COMMENT '份额登记机构',
  `create_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1613 DEFAULT CHARSET=utf8;
