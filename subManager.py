import requests
import re
from lxml import html
import send_attachment as sa
import sqlite3
import time

if __name__=='__main__': main()

def main():
  dbfile = '/var/www/html/tables/database.db'
  conn = sqlite3.connect(dbfile)
  c = conn.cursor()
  # for every row, look at the timenext
  t = (time.time(),)
  for row in c.execute('select * from SubID where timenext < ?;',t):
    #(userid, name,email,pswd)
    (subid,userid,website,regex,conditions,timenext,period) = row
    sendmail = check_sub(sub_id=subid,url=website,attr_patterns=regex,conditions=conditions)
    if sendmail: sa.send_attachment('tmp/'+str(sub_id)+'.html')
    print('incrementing timenext')
    c.execute('update SubID set timenext = timenext + period;')
    c.commit()

class NoMatchesWarning(Exception):
  pass

def get_page_content(url=None,headers=None):
  if headers is None: 
    headers = {
      # ':authority':'vmware.rolepoint.com',
      # ':method':'GET',
      # ':path':'/?shorturl=USrAd&jobapp=ahBzfnJvbGVwb2ludC1wcm9kchsLEg5Kb2JBcHBsaWNhdGlvbhiAgND8yNzDCgw',
      # ':scheme':'https',
      'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'accept-encoding':'gzip, deflate, br',
      'accept-language':'en-US,en;q=0.9,es;q=0.8',
      'cache-control':'max-age=0',
      #'cookie':'__utmz=1.1518205321.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.412395225.1518205321; _gid=GA1.2.1597170782.1518205321; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%2200e67512-fb8b-4e0f-aef0-0666c2061458%22; SHORTURL_KEY=ahBzfnJvbGVwb2ludC1wcm9kchMLEghTaG9ydFVybCIFVVNyQWQM; session=8f7b9a382da4f063_5a7f1809.t7-ru5tG9m3mduS4cmSTilU_51o; mp_a5ab085af9f943f97370d386d78907f2_mixpanel=%7B%22distinct_id%22%3A%20%221617c16beef8aa-0c118111bdabe9-3a7f0e5a-100200-1617c16bef0533%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; __utma=1.412395225.1518205321.1518235981.1518278667.3; __utmc=1; mp_mixpanel__c=0',
      'dnt':'1',
      'upgrade-insecure-requests':'1',
      'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
  if url is None: url = 'https://www.amazon.com/s/ref=sr_st_price-asc-rank?keywords=gaming+gloves&rh=n%3A468642%2Ck%3Agaming+gloves&qid=1518230048&sort=price-asc-rank'
  r=requests.get(url,headers=headers)
  #tree = html.fromstring(r.content)
  return r.content
##############################
#EBAY
#free shipping
# //*[@id="s5-c13-c2"]/span
# //*[@id="s5-c17-c3"]/span
# //*[@id="s5-c21-c2"]/span

#price strikethrough
# //*[@id="s5-c10-c2"]/span
# //*[@id="s5-c9-c2"]/span
# //*[@id="s0-c1-c2"]/span
# //*[@id="s0-c2-c1"]/span[1]
# //*[@id="s0-c5-c1"]/span[1]
# //*[@id="s0-c3-c1"]/span[1]
# //*[@id="s0-c10-c1"]/span[1]
# //*[@id="s0-c11-c2"]/span
##############################
# VMWARE
# //*[@id="job-list"]/li[1]/div/div[1]/p[3]/small/span[1]
# //*[@id="job-list"]/li[2]/div/div[1]/p[3]/small/span[1]

##############################
# AWS
#title
# //*[@id="result_1"]/div/div/div/div[2]/div[1]/div[1]/a/h2
# //*[@id="result_2"]/div/div/div/div[2]/div[1]/div[1]/a/h2
# //*[@id="result_3"]/div/div/div/div[2]/div[1]/div[1]/a/h2

#price
# //*[@id="result_0"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span[2]/span/span
# //*[@id="result_1"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span[2]/span/span
# //*[@id="result_2"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span[2]/span/span[1]
# //*[@id="result_3"]/div/div/div/div[2]/div[2]/div[1]/div/div/a/span[2]
# //*[@id="result_4"]/div/div/div/div[2]/div[2]/div[1]/div[2]/a/span[2]/span/span
# //*[@id="result_5"]/div/div/div/div[2]/div[2]/div[1]/div[2]/a/span[2]/span/span

#################################
# XPATH METHOD
#################################
def get_lca(node1, node2):
  """
  node1 and node2 are elements of the same DOM tree

  returns the lowest common ancestor of n1 and n2
  """
  if node1 is node2: return node1
  an1 = list(node1.iterancestors())
  an2 = list(node2.iterancestors())
  if(len(an1)<len(an2)):
    #consider the case that node1 is in an2
    pass
  elif(len(an1)==len(an2)):
    #look for lca in an1 and an2
    pass
  else:
    #consider the case that node2 is in an1
    pass



def get_all_attr_of_xpath(DOM,xpath_pat,el_pat):
  """
  DOM: lxml.html object reprentation of the page
  xpath_pat: encoding of xpath patterns
  el_pat: string representation of the element pattern

  returns: list of all html elements matching el_pat and with xpath matching the xpath_pat
  """


def parse_page(page_str, attr_xpath_pats ):
  """
  page_str: string representation of the webpage html
  attr_xpaths: list of attribute xpath patterns
  """
  tree = html.fromstring(page_str)


###################################
# AUTOMATIC GROUPING OF ATTRIBUTES (BUGGY AF)
###################################
def order_by_obj(page_str,attr_indicies):
  """
  page_str: string representation of the webpage
  attr_indicies: attr_indicies[num][1] is list of all occurences of the pattern attr_indicies[num][0] in the page_str
    ASSUMES that all attr_pattern match exactly with the list items attributes, and that there will only be one match per list item

  returns obj_list, where obj_list[i] contains dictionary of attr and the corresponding attr index found in page_str
  """
  #first reorder the attr_indicies in ascending order
  ascending = sorted(attr_indicies,key=lambda x: x[1][0][0])

  return [
    {
      a[0] : a[1][objindex] for a in ascending
    }
      for objindex in range(len(ascending[0][1]))
  ]

def parse_page(page_str, attr_patterns):
  """
  page_str: string representation of the webpage
  attr_patterns: list of attribute reg exp patterns

  returns a list of objects on the webpage, each object is dictionary of format keywords,values
  """
  attr_indicies = [
    (a, [(m.start(),m.group(0),m.group(2)) 
          for m in re.finditer(a,page_str)]
    )
      for a in attr_patterns
  ]

  if len(attr_indicies[0][1])==0: raise NoMatchesWarning
  
  obj_list = order_by_obj(page_str,attr_indicies)
  return obj_list

def scrape(url=None,headers=None,attr_patterns=None):
  """
  wrapper function
  """
  if attr_patterns is None:
    attr_patterns= [
      #b'(<span class="span-date-added">Date added: )([0-9]+?/[0-9]+?/[0-9]+?) (| </span>)',
      #b'(<span class="span-job-id">Job ID: )(R[0-9]+?)(</span>)',
      b'(<span class="sx-price-whole">)([0-9]+?)(</span>)'
      #b'(<h2 data-attribute="[a-zA-Z[ X]]+" data-max-rows="0" class="a-size-medium s-inline  s-access-title  a-text-normal">)([a-zA-Z[ X]]+)(</h2>)'
    ]
  page_str = get_page_content(url,headers)
  try:
    obj_list=parse_page(page_str,attr_patterns)
  except NoMatchesWarning:
    print('no matches')
    return
  except IndexError:
    print('attributes are not characteristic of each item')
  return page_str
def do_sub(): check_sub()

def check_sub(sub_id=None,url=None,attr_patterns=None,conditions=None):
  page_str=scrape(url=url,attr_patterns=attr_patterns)
  if sub_id is None: sub_id = 0
  if(page_str is not None):
    with open('tmp/'+str(sub_id)+'.html','wb') as f:
      f.write(page_str)
    return True
  else: return False




#html.open_in_browser(tree)