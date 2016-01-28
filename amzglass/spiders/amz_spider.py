import scrapy
from amzglass.items import AmzProduct
import re
from bs4 import BeautifulSoup
from bs4 import Tag
import os
from itertools import chain

def absolute_file_paths(directory, num = float("inf")):
    i = 0
    ret = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            if ".html" in f:
                i += 1
                ret.append("file://" + os.path.abspath(os.path.join(dirpath, f)))
                if i >= num:
                    return ret

class AmzSpider(scrapy.Spider):
    name = "amazon"
    directory = "../other/"
    num = 10
    start_urls = absolute_file_paths(directory, num)

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        item = AmzProduct()

        # Get all item attributes
        item['html_file'] = get_html_name(response)
        item['title'] = get_title(soup)
        item['price'] = get_price(soup)
        item['brand'] = get_brand(soup)
        item['feature_bullets'] = get_bullets(soup)
        item['description'] = get_desc(soup)
        item['details'] = get_details(soup)
        item['tech_specs'] = get_tech_specs(soup)

        yield item


def get_html_name(response):
    return response.url.split("/")[-1]


def get_title(soup):
    title_css = [
        ("id","productTitle"),
        ("id", "btAsinTitle")
    ]
    title = ""
    for row in title_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            title = tag.text.strip()
            break
    return title


def get_price(soup):
    price = ""
    price_css = [
        ("id","priceblock_ourprice"),
        ("class_", "a-color-price"),
        ("id","actualPriceValue")
    ]
    for row in price_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            price = tag.text
            break
    return price


def get_brand(soup):
    brand = ""
    brand_css = [
        ("id","brand"),
    ]
    for row in brand_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            brand = tag.text
            break
    return brand

def get_bullets(soup):
    feature_bullets = ""
    feature_bullets_css = [
        ("id","feature-bullets"),
        ("id","feature-bullets-btf"),
        ("id", "bookDescription_feature_div"),
        ("class_","productDescriptionWrapper"),
        ("id","productDescription")
    ]

    for row in feature_bullets_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            feature_bullets = tag.text.strip()
            break
    return feature_bullets

def get_desc(soup):
    description = ""
    description_css = [
        ("id", "bookDescription_feature_div"),
        ("class_","productDescriptionWrapper"),
        ("id","productDescription")
    ]

    for row in description_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            if val == "bookDescription_feature_div":
                # Get book description
                description = tag.find("noscript").text.strip()
            else:
                description = tag.text.strip()
            break
    return description

def get_details(soup):
    all_details = {}
    details = Tag(name="table")
    details_css = [
        ("id", "productDetailsTable"),
        ("id","detail-bullets"),
        ("id","detailBullets")
    ]

    for row in details_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            details = tag
            break

    for t in details.findAll("li"):
        text = t.text.strip()
        colon_pos = text.find(":")
        attr = text[:colon_pos].strip()
        val = text[colon_pos+1:].strip()
        if t.find("a"):
            remove_text = t.find("a").text
            val = val.replace(remove_text,"").replace("()","").strip()
        # if attr == "Shipping Weight":
        #     break
        if attr == "Average Customer Review":
            val = t.find("a").text
            try:
                val = re.search(r'\d.\d', val).group().strip()
            except:
                pass
        if attr == "Amazon Best Sellers Rank":
            a = re.search(r'#.+?\d ', val)
            a = a.group().replace(" ","").replace("#","").replace(",","")
            val = a
        all_details[attr] = val
    return all_details

def get_tech_specs(soup):
    all_specs = {}
    details = Tag(name="table")
    details_css = [
        ("id", "productDetailsTable"),
        ("id","detail-bullets"),
        ("id","detailBullets")
    ]

    for row in details_css:
        key, val = row
        tag = soup.find(**{key:val})
        if tag:
            details = tag
            break

    for t in details.findAll("li"):
        text = t.text.strip()
        colon_pos = text.find(":")
        attr = text[:colon_pos].strip()
        val = text[colon_pos+1:].strip()
        if t.find("a"):
            remove_text = t.find("a").text
            val = val.replace(remove_text,"").replace("()","").strip()
        # if attr == "Shipping Weight":
        #     break
        if attr == "Average Customer Review":
            val = t.find("a").text
            try:
                val = re.search(r'\d.\d', val).group().strip()
            except:
                pass
        if attr == "Amazon Best Sellers Rank":
            a = re.search(r'#.+?\d ', val)
            a = a.group().replace(" ","").replace("#","").replace(",","")
            val = a
        all_specs[attr] = val
    return all_specs

