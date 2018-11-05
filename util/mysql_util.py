#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : linjie
# @Des     : mysql工具类

import logging

import pymysql

mysql_conf = {
    'host': 'host',
    'user': '用户名',
    'password': '密码',
    'port': 端口,
    'database': 'jd_comment',
    'charset': 'utf8'
}
# mysql_conf = {
#     'host': 'cdb-60q89up0.cd.tencentcdb.com',
#     'user': 'root',
#     'password': 'eMb-dWk-Apa-2cR',
#     'port': 10023,
#     'database': 'jdcomm',
#     'charset': 'utf8'
# }
class MySQLUtil:
    def __init__(self, conf):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.conn = pymysql.connect(**conf)
        self.cursor = self.conn.cursor()

    # 获取游标
    def get_cur(self):
        return self.cursor

    # 事务提交
    def commit(self):
        self.conn.commit()

    # 关闭连接
    def close(self):
        self.conn.close()

    #关闭游标
    def curclose(self):
        self.cursor.close()

    # 回滚事务
    def rollback(self):
        self.conn.rollback()

    '''
        查询操作
    '''
    def queryOperation(self, sql):
        # 获取数据库游标
        cur = self.get_cur()
        #print("sdasds")
        # 执行查询
        dataList = []
        try:
            cur.execute(sql)
        # 查询结果条数
        # row = cur.rowcount
        # 查询结果集
            dataList = cur.fetchall()
        except Exception as e:
            logging.error('查询结果集异常{0}'.format(e))
        # 关闭游标
        #cur.close()
        # 关闭数据连接
        #self.close()
        #返回查询结果集
        logging.info('{}'.format(dataList))
        return dataList
    '''
        数据导入excel的查询操作
    '''
    def queryOperationExcel(self,sql,flag):
        # 获取数据库游标
        cur = self.get_cur()
        # print("sdasds")
        # 执行查询
        #dataList = []
        try:
            cur.execute(sql)
            #移动游标位置
            cur.scroll(0,mode="absolute")
            # 查询结果条数
            # row = cur.rowcount
            # 查询结果集
            #flag等于1：查询结果集
            #flag等于2：查询表结构描述
            if flag==1:
                dataList = cur.fetchall()
            elif flag==0:
                dataList = cur.description
        except Exception as e:
            logging.error('查询结果集异常{0}'.format(e))
        # 关闭游标
        # cur.close()
        # 关闭数据连接
        # self.close()
        # 返回查询结果集
        logging.info('{}'.format(dataList))
        return dataList
    def insertOperation(self,sql):
        cur = self.get_cur()
        try:
            cur.execute(sql)
            self.commit()
        except Exception as e:
            #print(e)
            logging.error('插入失败 {}'.format(e))
            self.rollback()

        #cur.close()
        #self.close()

    '''
    更新操作
    '''
    def updateOperation(self, sql):
        cur = self.get_cur()
        try:
            cur.execute(sql)
            self.commit()
        except Exception as e:
            logging.error('更新操作异常{0}'.format(e))
            self.rollback()
        #cur.close()
        #self.close()


    '''
    京东爬虫：插入信息
    '''
    def insertgoodscommentmsg(self,product_Id,product_type,product_comment,product_comm_time):
        sql = "insert into blwjxb_z(product_id,product_type,product_comment,product_comm_time) value ('{0}','{1}','{2}','{3}')".format(product_Id,product_type,product_comment,product_comm_time)
        try:
            logging.info('{}'.format(sql))
            self.insertOperation(sql)
        except Exception as e:
            logging.error('插入数据异常：{}'.format(e))
        else:
            logging.info('插入数据成功')

    '''
    京东商品评论总数
    '''
    def insertcommsum(self,product_Id,name,url,comm_sum):
        sql = "insert into prn_z_commsum(product_id,name,product_url,comm_sum) value ('{0}','{1}','{2}','{3}')".format(product_Id,name,url,comm_sum)
        try:
            logging.info('{}'.format(sql))
            self.insertOperation(sql)
        except Exception as e:
            logging.error('插入数据异常：{}'.format(e))
        else:
            logging.info('插入数据成功')

    '''
    查询mysql数据 将mysql表数据导入到excel
    '''
    def getmysqldata(self,tablename,flag):
        sql = "SELECT * FROM {0}".format(tablename)
        try:
            logging.info('{}'.format(sql))
            data = self.queryOperationExcel(sql,flag)
        except Exception as e:
            logging.error('{}'.format(e))
        else:
            logging.info('获取excel数据成功：{}'.format(data))
            return data


    # '''
    # 京东商品评论总数中插入名称
    # '''
    # def insertcommname(self,name):
    #     sql = "insert into blwjxb_commsum(name) value ('{0}')".format(name)
    #     try:
    #         logging.info('{}'.format(sql))
    #         self.insertOperation(sql)
    #     except Exception as e:
    #         logging.error('插入数据异常：{}'.format(e))
    #     else:
    #         logging.info('插入数据成功')
    # #获取所有总流程数据
    # #@staticmethod
    # def get_datalist(self,state):
    #     sql = "select t.id tid,ta.id taskid,t.sku_id skuid,u.formula_id formulaid,u.datasource_id datasourceid,u.collection_name collectionname,u.document_id documentid,ta.state state,t.data_time datatime from" \
    #           " sku u left join task t on t.sku_id=u.id left join task_allocation ta on ta.task_id=t.id where ta.state='{0}' limit 1".format(state)
    #     datalist = self.queryOperation(sql)
    #     return datalist
    #
    # #更新documentid的值
    # def updatedocumentid(self,data,skuid):
    #     try:
    #         update_documentid_sql = "UPDATE sku SET document_id = '{0}' where id ='{1}'".format(data,skuid)
    #         self.updateOperation(update_documentid_sql)
    #     except Exception as e:
    #         logging.error('更新documentid异常 {}'.format(e))
    #     else:
    #         logging.info('更新documentid成功')
    #
    # #更新任务状态
    # def updatestate(self,state,taskid):
    #     try:
    #         update_state_sql = "UPDATE task_allocation SET state = {0} where id ='{1}'".format(state,taskid)
    #         self.updateOperation(update_state_sql)
    #     except Exception as e:
    #         logging.error('更新任务状态异常 {}'.format(e))
    #     else:
    #         logging.info('更新状态成功')


if __name__ == '__main__':
    m = MySQLUtil(mysql_conf)
    # a = {"a": '1', "b": '2'}
    # b = {"b": '1', "c": '3'}
    # m.update("sss", a, b)
    # sets = {"a": 1, "b": 2}
    # conditions = [{"$or": [{"c": 3}, {"d": 4}]}]
    # sql = m.creat_update_sql("aa", sets, conditions)
    # print(sql)
    # sets = {"a": 1, "b": 2}
    # conditions = [{"aaa": 11}, {"$like%": {"c": 3}}]
    # sql = m.creat_update_sql("aa", sets, conditions)
    # print(sql)

