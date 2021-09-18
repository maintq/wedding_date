#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 23:57:13 2021

@author: maintq      
@ author's email id:       maintq710@gmail.com


"""
#%% Import library

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np

import datetime
import time

import streamlit as st


st.write("""
# Find the best date for the best day of your life

""")

st.subheader('Enter your info:')

def user_input_features():
    m_bd = st.date_input("Enter the groom's birthday")
    f_bd = st.date_input("Enter the bride's birthday")
    sd = st.date_input("Enter the soonest date you plan to get married")
    ed = st.date_input("Enter the latest date you plan to get married")
    
    return m_bd,f_bd,sd,ed


m_bd, f_bd, sd, ed = user_input_features()


input_date = []
for n in range(int((ed - sd).days)):
    input_date.append(sd + datetime.timedelta(n))

#%%
def run_date(m_bd, f_bd, sd, ed):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    driver.get('http://www.chonngaytotxau.com/vn/xem-ngay-cuoi-hoi.htm')
    print("Running the first website...")
    res1 = {}
    m_bd_str = m_bd.strftime('%d/%m/%yyyy')
    f_bd_str = f_bd.strftime('%d/%m/%yyyy')
    
    for date in input_date:
        date = date.strftime("%d/%m/%Y")
        m_bd_box = driver.find_element_by_css_selector('#nsChuRe')
        m_bd_box.clear()
        m_bd_box.send_keys(m_bd_str)
    
        f_bd_box = driver.find_element_by_css_selector('#nsCoDau')
        f_bd_box.clear()
        f_bd_box.send_keys(f_bd_str)
    
    
        w_date = driver.find_element_by_css_selector('#ngayCuoi')
        w_date.clear()
        w_date.send_keys(date)
        check_button = driver.find_element_by_css_selector('#clsbutton')
        check_button.click()
        time.sleep(10)
        try:
            result = driver.find_elements_by_xpath("//*[contains(text(), 'Tổng điểm')]")
            res1[date] = result[0].text
        except IndexError:
            result = driver.find_elements_by_xpath("//*[contains(text(), 'Ngày xem')]")
            res1[date] = result[0].text
    print(res1)
    df_res1 = pd.DataFrame(res1.items(), columns=['Date', 'Result'])
    df_res1['Point1'] = np.nan
    
    for i in range(len(df_res1)):
        idx = df_res1.Result[i].index('/')
        df_res1['Point1'][i] = df_res1.Result[i][idx-2:idx]
    df_res1.Date = pd.to_datetime(df_res1.Date)
    df1 = df_res1[['Date','Point1']]
    
    
    driver.get('https://xemboi.com.vn/xem-ngay-cuoi-hoi/')
    print("Running the second website...")
    res2 = {}
    
    #Ngày sinh cô dâu
    f_date = str(f_bd.day).zfill(2)
    f_month = str(f_bd.month).zfill(2)
    f_year = str(f_bd.year)
        
    f_d = Select(driver.find_element_by_class_name('ngayv'))
    f_d.select_by_value(f_date)
        
    f_m = Select(driver.find_element_by_class_name('thangv'))
    f_m.select_by_value(f_month)
        
    f_y = Select(driver.find_element_by_class_name('namv'))
    f_y.select_by_value(f_year)
    
            
    #Ngày sinh chú rể
        
    m_date = str(m_bd.day).zfill(2)
    m_month = str(m_bd.month).zfill(2)
    m_year = str(m_bd.year)
        
    m_d = Select(driver.find_element_by_class_name('ngayc'))
    m_d.select_by_value(m_date)
        
    m_m = Select(driver.find_element_by_class_name('thangc'))
    m_m.select_by_value(m_month)
        
    m_y = Select(driver.find_element_by_class_name('namc'))
    m_y.select_by_value(m_year)
    
    for date in input_date:  
        #Ngày cưới
        w_date = str(date.day).zfill(2)
        w_month = str(date.month).zfill(2)
        w_year = str(date.year)
        
        w_d = Select(driver.find_element_by_class_name('ngayl'))
        w_d.select_by_value(w_date)
        
        w_m = Select(driver.find_element_by_class_name('thangl'))
        w_m.select_by_value(w_month)
        
        w_y = Select(driver.find_element_by_class_name('naml'))
        w_y.select_by_value(w_year)
    
       
        check_button = driver.find_element_by_class_name('xemkq')
        check_button.click()
        time.sleep(10)
        result = driver.find_element_by_class_name('diemso')
        res2[date] = result.text
    
    print(res2)
            
    df_res2 = pd.DataFrame(res2.items(), columns=['Date', 'Result'])
    df_res2['Point2'] = [float(e[:2]) for e in df_res2.Result]
    df_res2.Date = pd.to_datetime(df_res2.Date)
    df2 = df_res2[['Date','Point2']]
    
    fnl = pd.merge(df1,df2,on = 'Date')
    fnl['Avg'] = (fnl.Point1 + fnl.Point2)/2
    fnl['weekday'] = [e.weekday()+2 for e in fnl.Date]
    
    driver.close()
    return fnl.sort_values(by = 'Avg', ascending = False)    

#%%
if st.button('Run'):
    st.write(run_date(m_bd, f_bd, sd, ed))
else:
    st.write('No data yet')

st.footer('''
 Created by Mai Nguyen
 Facebook: https://www.facebook.com/maintq710
 Email: maintq710@gmail.com
 Source code: https://github.com/maintq/wedding_date
 Youtube: https://www.youtube.com/channel/UC98WbIwqUTRwwTHI3zfT1Fg
 ''')          
       
