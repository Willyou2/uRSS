import requests
import re
def get_page_content(url=None,headers=None):
  if headers is None: 
    headers = {
      'Accept':'*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
      'Connection':'keep-alive',
      'DNT':'1',
      'Host':'www.amazon.com',
      'Referer':'https://www.amazon.com/s/ref=sr_st_price-asc-rank?keywords=gaming+gloves&rh=n%3A468642%2Ck%3Agaming+gloves&qid=1518230048&sort=price-asc-rank',
      'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
  if url is None: url = 'https://www.amazon.com/s/ref=sr_st_price-asc-rank?keywords=gaming+gloves&rh=n%3A468642%2Ck%3Agaming+gloves&qid=1518230048&sort=price-asc-rank'
  r=requests.get(url,headers=headers)
  #tree = html.fromstring(r.content)
  return r.content

def order_by_obj(page_str,attr_indicies):
  """
  page_str: string representation of the webpage
  attr_indicies: attr_indicies[num][1] is list of all occurences of the pattern attr_indicies[num][0] in the page_str
    ASSUMES that all attr_pattern match exactly with the list items attributes, and that there will only be one match per list item

  returns obj_list, where obj_list[i] contains dictionary of attr and the corresponding attr index found in page_str
  """
  #first reorder the attr_indicies in ascending order
  ascending = sorted(attr_indicies,key=lambda x: x[1][0])
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
    (a,[(m.start(),m.group(0)) for m in re.finditer(a,page_str)])
      for a in attr_patterns
  ]
  
  obj_list = order_by_obj(page_str,attr_indicies)
  return obj_list

def scrape(url=None,headers=None,attr_patterns=None):
  """
  wrapper function
  """
  if attr_patterns is None:
    attr_patterns= [
      b'<span class="sx-price-whole">[0-9]+</span>',
      b'<sup class="sx-price-fractional">[0-9]+</sup>'
    ]
  page_str = get_page_content(url,headers)
  obj_list=parse_page(page_str,attr_patterns)
  return obj_list


#html.open_in_browser(tree)