#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : linjie
# @Des     : py将MySQL数据导出到excel
import logging
import util as mysql_util
import xlwt
from util import mysql_util
from util.mysql_util import MySQLUtil
class ExcelUtils:
# 日志配置
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    '''
    mysql数据导入excel
    sheet_name:excel excel名称
    dbname:数据库名
    tablename:表名
    out_path:文件存放路径
    flag1:数据表结果集查询标志
    flag2:数据表描述查询标志
    '''
    def mysql_to_excel(self,sheet_name,tablename,out_path,flag1=1,flag2=0):
        mysqldb = MySQLUtil(mysql_util.mysql_conf)
        #结果集
        datalist = mysqldb.getmysqldata(tablename,flag1)
        logging.info('结果集：{}'.format(datalist))
        #表描述
        tabledesc = mysqldb.getmysqldata(tablename,flag2)
        logging.info('表描述：{}'.format(tabledesc))
        #创建excel
        workbook = xlwt.Workbook()
        #创建excel中的sheet
        sheet = workbook.add_sheet(sheet_name,cell_overwrite_ok=True)

        #插入表描述到excel
        for desc in range(0,len(tabledesc)):
            sheet.write(0,desc,tabledesc[desc][0])
        row = 1
        col = 0
        #插入数据到excel
        for row in range(1,len(datalist)+1):
            for col in range(0,len(tabledesc)):
                sheet.write(row,col,u'%s'%datalist[row-1][col])
        try:
            #保存excel
            workbook.save(out_path)
        except Exception as e:
            logging.error('导出数据到excel失败：{}'.format(e))
        else:
            logging.info('导出成功')
            #数据库连接关闭二连
            mysqldb.curclose()
            mysqldb.close()

if __name__ == '__main__':
    mysql_excel = ExcelUtils()
    mysql_excel.mysql_to_excel('build','ms_commsum','test.xls')