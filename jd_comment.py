#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import re
import time
import urllib
import urllib.request
import urllib.parse
import requests
import ssl

from spider_pretend import request_headers_comment

ssl._create_default_https_context = ssl._create_unverified_context
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from util import mysql_util
from util.mysql_util import MySQLUtil
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  ###禁止提醒SSL警告

class jd_comment:
    # 日志配置
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    def get_product_id(self):
        page = 1
        reg = []
        reg2 = []
        while(page<12):
            #店铺所有商品页
            html_url = "https://module-jshop.jd.com/module/allGoods/goods.html?callback=jQuery9393562&sortType=0&appId=1136039&pageInstanceId=121415250&searchWord=&pageNo={0}&direction=1&instanceId=129305331&modulePrototypeId=55555&moduleTemplateId=905542&refer=https%3A%2F%2Fmall.jd.com%2Fview_search-1136039-0-99-1-24-1.html&_=1541232930563".format(page)
            request = urllib.request.Request(html_url)
            response = urllib.request.urlopen(request)
            html = response.read()
            realhtml = html.decode('utf-8')

            #productid = re.search('^[^(]*?\((.*)\)[^)]*$',realhtml).group(1)
            #jsonpro = json.loads(productid)


            #第四家,5,6
            #reg += re.findall(r'sid=\\\"(.*?)\\\"',realhtml)

            #1,2,9,11
            #reg += re.findall(r'data-id=\\\"(.*?)\\\"',realhtml)

            #第七家
            #reg += re.findall(r'pid=(.*?)&',realhtml)
            #获取店铺id
            reg += re.findall(r'jdprice=\'(.*?)\'',realhtml)
            logging.info('获取店铺商品id：{}'.format(reg))
            #reg2 += re.search(r'html\\\" target=\\\"_blank\\\">(.*?)</a>\\r\\n',realhtml)
            #reg2 += re.findall(r'title=\\\"(.*?)\\\">',realhtml)
            #获取商品名称
            reg2 += re.findall(r'.html\\\" target=\\\"_blank\\\" title=\\\"(.*?)\\\">',realhtml)
            #reg2 += re.findall(r'alt=\\\"(.*?)\\\"', realhtml)
            logging.info('获取店铺商品名称信息：{}'.format(reg2))
            #print(reg)
            page+=1
        for dataid,dataname in zip(reg,reg2[1::2]):
            time.sleep(2)
            logging.info('看看商品id：{}'.format(dataid))
            logging.info('看看商品名称：{}'.format(dataname))
            # jc.jd_comment2(dataid)
            self.get_comment_count(dataid,dataname)
        #return reg

    def jd_comment2(self,productId):

        mysqldb = MySQLUtil(mysql_util.mysql_conf)
        index = 1
        while(index<10):
            logging.info('爬到第{}页了'.format(index))
            # 随机休眠
            #time.sleep(random.random())
            time.sleep(3)
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv&productId={0}&score=0&sortType=5&page={1}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(productId,index)
            print(url)
            jdcomm= requests.get(url,headers = request_headers_comment)
            #data=json.loads(jdcomm.text)
            try:
                data = json.loads(jdcomm.text.lstrip('fetchJSON_comment98vv(').rstrip(');'))
            except Exception as e:
                logging.info('进程死了{}'.format(e))
                time.sleep(3)
                #data = json.loads(jdcomm.text.lstrip('fetchJSON_comment98vv(').rstrip(');'))
            if data['comments']==[]:
                break
            logging.info('{}'.format(data))
            for i in data['comments']:
                logging.info('看看进来了吗')

                product_id = productId                #商品id
                product_type = i['referenceName']     #商品类型
                product_comment = i['content']        #商品评论
                product_comm_time = i['creationTime'] #商品评论时间
                logging.info('{0},{1},{2},{3}'.format(product_id,product_type,product_comment,product_comm_time))
                mysqldb.insertgoodscommentmsg(product_id,product_type,product_comment,product_comm_time)
            index += 1
                #content = i['content']
                #referenceName = i['referenceName']
                #creationTime = i['creationTime']
                #print("评论内容{}".format(content))
                #logging.info('{}'.format(referenceName))
                #logging.info('{}'.format(creationTime))
        mysqldb.curclose()
        mysqldb.close()
        print("finished")
    #获取商品名称
    # def get_goodsname(self,productId):
    #     url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv&productId={0}&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(
    #         productId)
    #     logging.info('{}'.format(url))
    #单品的评论总数
    def get_comment_count(self,productId,name):
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv&productId={0}&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(productId)
        print(url)
        jdcomm = requests.get(url,headers = request_headers_comment)
        product_url = "https://item.jd.com/"+productId+".html"
        # data=json.loads(jdcomm.text)
        try:
            data = json.loads(jdcomm.text.lstrip('fetchJSON_comment98vv(').rstrip(');'))
        except Exception as e:
            logging.info('进程死了{}'.format(e))
            time.sleep(3)
        mysqldb = MySQLUtil(mysql_util.mysql_conf)
        comm_sum = data['productCommentSummary']['goodCountStr']
        #mysqldb.insertcommsum(productId,name,product_url,comm_sum)
        #mysqldb.insertcommname()
        #mysqldb.insertcommsum()
        mysqldb.curclose()
        mysqldb.close()
        print(comm_sum)
if __name__ == '__main__':
    jc = jd_comment()
    jc.get_product_id()
    #logging.info('看看有没有拿到店铺所以商品的name：{}'.format(list))
    # for dataid in list:
    #     time.sleep(2)
    #     logging.info('看看商品id：{}'.format(dataid))
    #     #jc.jd_comment2(dataid)
    #     jc.get_comment_count(dataid)



    #单品的评论总数
    #jc.get_comment_count(10330243533)