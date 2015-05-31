#!/usr/bin/python
import csv, re
from urllib2 import Request, urlopen, URLError

def extract_information():
    
    for i in range(1, 50):
        get_product_url("http://www.nationaltiles.com.au/vic_pm/products/tiles?p="+str(i))

def get_product_url(pagination_url):
    req = Request(pagination_url)
    response = urlopen(req)
    pagination_html = response.read().replace('\r', '').replace('\n', '')
    
    get_details_page_url = re.findall(r'<h2 class="product-name"><a href="(.*?)"', pagination_html)
    for details_url in get_details_page_url:
        extract_details_information(details_url)

def extract_details_information(details_url):
    req = Request(details_url)
    response = urlopen(req)
    pagination_html = response.read().replace('\r', '').replace('\n', '')
    
    try:
        title = re.findall(r'<h1 itemprop="name">(.*?)</h1>', pagination_html)[0]
    except:
        title = ''
    print title
    
    try:
        image_urls = re.findall(r'<div class="more-views">.*?</ul>', pagination_html)[0]
        get_product_imgs = re.findall(r'<a href="(.*?)" rel="gallery" class="pirobox_gall"', image_urls)
    except:
        get_product_imgs = []
    print get_product_imgs
    
    try:
        sku = re.findall(r'SKU</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        sku
    print sku
    
    try:
        country = re.findall(r'Country</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        country = ''
    print country
    
    try:
        area = re.findall(r'Area</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        area = ''
    print area
    
    try:
        body = re.findall(r'Body</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        body = ''
    print body
    
    try:
        size = re.findall(r'Size</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        size = ''
    print size
    
    try:
        feels_like = re.findall(r'Feels Like</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        feels_like = ''
    print feels_like
    
    try:
        finish = re.findall(r'Finish</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        finish = ''
    print finish
    
    try:
        colour = re.findall(r'Colour</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        colour = ''
    print colour
    
    try:
        warranty = re.findall(r'Warranty</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        warranty = ''
    print warranty
    
    try:
        edging = re.findall(r'Edging</p>.*?<p>(.*?)</p>', pagination_html)[-1]
    except:
        edging = ''
    print edging
    
    data_writer.writerow([details_url,
                          title,
                          sku,
                          country,
                          area,
                          body,
                          size,
                          feels_like,
                          finish,
                          colour,
                          warranty,
                          edging,
                          ",".join(get_product_imgs)])
    
    print '-'*78
    
if __name__ == "__main__":
    csv_file_name = 'nationaltiles v0.01.csv'
    f = open('imported_data/'+csv_file_name, "wb")
    data_writer = csv.writer(f)

    data_writer = csv.writer(open('imported_data/'+csv_file_name, 'wb'))
    data_writer.writerow(['URL','Title', 'SKU', 'Country', 'Area', 'Body', 'Size', 'Feels Like', 'Finish',
                          'Colour',
                          'Warranty',
                          'Edging',
                          'Images'])
    extract_information()
