#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by John R Milinovich on 2012-08-19.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import urllib2
import json
import pprint

def BuildConnectionSearch(keyword,page_num):
# this function opens the connection to the data from the api source
  # connect to the api and search for query in variable 'keyword'
  url = 'http://api.crunchbase.com/v/1/search.js?query=%s&page=%s' % (keyword,page_num)
  print url
  # convert the html source to string 'json_string'
  json_string = urllib2.urlopen(url).read()
  #print json_string
  #raw_input()
  # convert json data model to python model
  unpacked = json.loads(json_string.replace('\r\n', ''))
  num_results = unpacked['total']
  return unpacked, num_results

### THIS CODE DOES NOTHING #####
def ExtractData(keyword_search_list, company_data_points, request_data_points):
# this function extracts the data from the data source
  results_source, num_results = BuildConnectionSearch(keyword_search_list[0])
  # this prints the first data points for the first result
  return results_source[request_data_points[0]]
################################  

def CompanyConnector(permalink,namespace):
  company_url = 'http://api.crunchbase.com/v/1/%s/%s.js' % (namespace, permalink)
  json_string = urllib2.urlopen(company_url).read()
  #print json_string
  #raw_input()
  # convert json data model to python model
  unpacked_site = json.loads(json_string.replace('\r\n', ''))
  website = unpacked_site['homepage_url']
  blog_url = ''
  twitter_username = ''
  email_address = ''
  if 'blog_url' in unpacked_site:
    blog_url = unpacked_site['blog_url']
  if 'twitter_username' in unpacked_site:
    twitter_username = unpacked_site['twitter_username']
  if 'email_address' in unpacked_site:
    email_address = unpacked_site['email_address']
  return website, blog_url, twitter_username, email_address

def CSVWriter(tsv_file, company_list):
  tsv_file.write("%r\t%r\t%r\t%r\t%r\t%r\t%r\t%r\t%r\n" % (company_list[0],company_list[1],company_list[2],company_list[3],company_list[4],company_list[5],company_list[6],company_list[7],company_list[8]))
  
def LeadMaker(keyword_search_list,company_data_points,request_data_points,max_results_per_page,results_dict):
  tsv_file = open('tsv_file.tsv','w')
  tsv_file.write("company_name\tpermalink\tcrunchbase_url\tnamespace\tsearch_term\twebsite\tblog\ttwitter\temail\n")
  search_results = {}  
  for keyword in keyword_search_list:
    page_num=1
    r, num_res = BuildConnectionSearch(keyword,page_num)
    num_pages=(num_res/10)+2
    ### SET MAX PAGES FOR RESULTS, ONE MORE THAN YOU WANT IN PAGES  ###
    if num_pages>11:
      num_pages = 11
    for page_num in range(1,int(num_pages)):  
      results_source, num_results = BuildConnectionSearch(keyword,page_num)
      search_results[keyword] = num_results
      if max_results_per_page > num_results:
        num_range = num_results
      if max_results_per_page < num_results:
        num_range = max_results_per_page
      if page_num == (int(num_pages)-1):
        num_range = (num_res % max_results_per_page)
      for result_num in range(0,num_range):
        #if results_source['results'][result_num]['namespace'] <> 'person':
        if results_source['results'][result_num]['namespace'] is 'company' or 'product':  
          if 'name' in results_source['results'][result_num]:  
            company_list = []
            for company_point in company_data_points:
              company_list.append(results_source['results'][result_num][company_point])
            company_list.append(keyword)
            website, blog_url, twitter_username, email_address = CompanyConnector(results_source['results'][result_num]['permalink'],results_source['results'][result_num]['namespace'])
            company_list.append(website)
            company_list.append(blog_url)
            company_list.append(twitter_username)
            company_list.append(email_address)
            CSVWriter(tsv_file, company_list)
            results_dict[company_list[0]] = company_list[1:]
            print results_source['results'][result_num]['name']
            #print results_source['results'][result_num]
      print ''  
      print ''
  tsv_file.close()
  return results_dict, search_results

### THIS SENDS ALL OF THE VARIABLESS INTO THE PUZZLE - LEADMAKER
def LeadListMaker():
  keyword_search_list = ['data-management','social-analytics','website-optimization']
  company_data_points = ['name','permalink','crunchbase_url','namespace']
  #keyword_search_list = ['Business%20Intelligence','business-intelligence','E-Commerce','ecommerce','email-marketing','reporting-tools','Email%20Marketing','Phone%20Call%20Tracking','Reporting%20Tools','data%20visualization','data-visualization','google-analytics','google%20analytics','web-analytics','web%20analytics','omniture','webtrends','shopping-cart','shopping%20cart']
  company_data_points = ['name','permalink','crunchbase_url','namespace']
  request_data_points = ['total','page','crunchbase_url']
  max_results_per_page = 10
  results_dict = {}
  results_dict, search_results = LeadMaker(keyword_search_list,company_data_points,request_data_points,max_results_per_page,results_dict)
  return results_dict, search_results
  
def main():	
  
  results_dict, search_results = LeadListMaker()
  #print '( press any key )'
  #raw_input()
  #pprint.pprint(search_results)
  #print '( press any key )'
  #raw_input()
  #pprint.pprint(results_dict)
  
  #company_name,permalink,cb_url,namespace,search_term,website,blog,twitter,email_addr


  print 'done.  check tsv_file.csv'   
  

  
  """
  http://api.crunchbase.com/v/1/company/google.js
  """

if __name__ == '__main__':
	main()