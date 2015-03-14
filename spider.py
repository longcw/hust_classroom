# coding: utf-8
__author__ = 'chenlong'

import time
import datetime
import logging

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models import ClassRoom, db

Buildings = {
    'd12': '1',
    'x5': '5',
    'd9': '7',
    'd5': '11',
    'x12': '13'
}


class ClassRoomSpider:
    base_url = 'http://202.114.5.131/'

    def __init__(self):
        self.driver = webdriver.PhantomJS(
            service_args=['--load-images=no'],
            service_log_path='/var/www/wwwlog/hust_ghostdriver.log',
            executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs'
        )
        self.wait = WebDriverWait(self.driver, 30)

    def get_classroom(self, date, building):
        self.driver.get(self.base_url)
        logging.info('spider init successful')

        logging.info('start getting %s on %s' % (building, date))
        # 设置时间
        date_input = self.driver.find_element_by_id('datepicker')
        date_input.clear()
        date_input.send_keys(date)  # 相当于从键盘输入
        logging.info('  set date ok')

        # 当目标教室与当前教室相同时,checkBoxAll 不选中,否则选中
        selected = self.driver.find_element_by_xpath('//select[@id="ddlBuild"]/option[@selected="selected"]')
        select_same = building == selected.get_attribute('value')
        checked = self.driver.find_element_by_id('checkBoxAll').is_selected()
        if (select_same and checked) or (not select_same and not checked):
            self.driver.find_element_by_id('checkBoxAll').click()

        # 换教学楼
        select = Select(self.driver.find_element_by_id('ddlBuild'))
        select.select_by_value(building)
        logging.info('  change building ok')

        # 改变select后页面会刷新, 需要重新选择复选框checkBoxAll
        self.wait.until(
            EC.element_located_selection_state_to_be((By.ID, 'checkBoxAll'), False)
        )
        self.driver.find_element_by_id('checkBoxAll').click()
        logging.info('  select all ok')
        self.wait.until(
            EC.text_to_be_present_in_element_value((By.ID, 'txtSelectedClass'), ';')
        )

        # 删除以前的数据
        if len(self.driver.find_elements_by_id('gvMain')) > 0:
            js = '''
                var element = document.getElementById("%s");
                element.parentNode.removeChild(element);
            ''' % 'gvMain'
            self.driver.execute_script(js)
        self.driver.find_element_by_id('btSearch').click()
        table = self.wait.until(
            EC.presence_of_element_located((By.ID, 'gvMain'))
        )
        data = unicode(table.get_attribute('innerHTML'))
        logging.info('get classroom ok')
        return data.replace('<td>&nbsp;</td>', u'<td style="background-color:#00CC66;">自习</td>')

    def get_and_save(self, date, building_key):
        try:
            item = ClassRoom.save_data(date, building_key, self.get_classroom(date, Buildings[building_key]))
            logging.info('get and save %s on %s' % (building_key, date))
            return item
        except Exception, e:
            logging.error(e)


    @staticmethod
    def get_date(after=0):
        """
        获取查询所需的合适的日期格式
        :param after: int 查询多少天后的教室情况, 例如 0 表示当天, -1 表示昨天
        :return: str 形如 2015/02/18 的字符串
        """
        date = datetime.datetime.now() + datetime.timedelta(days=after)
        return date.strftime('%Y/%m/%d')


if __name__ == '__main__':
    logging.info('starting')
    print('starting at %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    spider = ClassRoomSpider()
    print('spider init successfully at %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    try:
        for after in range(0, 2):
            for k, v in Buildings.iteritems():
                date = spider.get_date(after)
                data = spider.get_classroom(date, Buildings[k])
                try:
                    db.connect()
                    ClassRoom.save_data(date, k, data)
                finally:
                    db.close()
                print('save %s -> %s at %s' % (date, k, time.strftime('%Y-%m-%d %H:%M:%S')))
        logging.info('update successful')
        print('update completed at %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
    finally:
        spider.driver.quit()
