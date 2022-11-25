import requests
import urllib.parse
from bs4 import BeautifulSoup
import argparse

url = "https://www.flipkart.com"

global comments
comments = []

global counter
counter = 0

global PRODUCT_NAME 
PRODUCT_NAME = ""

def retrieve_all_phones_links(phone_name):
    query_url = "https://www.flipkart.com/search?q="
    phones_name_encoded = urllib.parse.quote(phone_name)
    phones_search_url = query_url+phones_name_encoded

    phones_result_page = requests.get(phones_search_url).text

    phones_result_page_soup = BeautifulSoup(phones_result_page, "html.parser")
    all_phones_div = phones_result_page_soup.findAll("div", {"class": "_1AtVbE col-12-12"})

    del all_phones_div[0:2]

    product_page_links = []

    for product_div in all_phones_div:
        try:
            product_page_links.append(url+product_div.div.div.div.a["href"])
        except:
            pass

    return product_page_links

def retrieve_product_page(product_page_link):
    product_page = requests.get(product_page_link).text
    product_page_soup = BeautifulSoup(product_page, "html.parser")
    product_name = product_page_soup.findAll("span", {"class":"B_NuCI"})[0].text
    return product_page_soup, product_name

def retrieve_comment_page_link(product_page_soup):
    comments_page_sublink = product_page_soup.findAll("div", {"class": "col JOpGWq"})[0]     #.a["href"]
    comments_page_sublink = comments_page_sublink.findAll("a")[-1]["href"]
    comments_page_link = url + comments_page_sublink
    return comments_page_link

def retrieve_comments(comments_page_link, product_name):
    global counter 
    counter += 1
    comments_page = requests.get(comments_page_link).text
    comments_page_soup = BeautifulSoup(comments_page, "html.parser")

    comments_div = comments_page_soup.findAll("div", {"class":"col _2wzgFH K0kLPL"})
    
    for comment in comments_div:
        rating = comment.find("div", {"class": "_3LWZlK"}).text  # _1BLPMq
        comment_heading = comment.find("p", {"class": "_2-N8zT"}).text
        comment_body = comment.find("div", {"class": "t-ZTKy"}).div.div.text
        user = comment.find("p", {"class": "_2sc7ZR _2V5EHH"}).text
        date_of_comment = comment.findAll("p", {"class": "_2sc7ZR"})[-1].text
        likes = comment.findAll("span", {"class": "_3c3Px5"})[0].text
        dislikes = comment.findAll("span", {"class": "_3c3Px5"})[1].text
    
        comments.append({"product name": product_name,
                "rating": rating,
                "comment title": comment_heading,
                "comment": comment_body,
                "user name": user,
                "date of comment": date_of_comment,
                "likes": int(likes),
                "dislikes": int(dislikes)})

    try:         
        next_page_links = comments_page_soup.findAll("nav", {"class":"yFHi8N"})[0]
        next_page_link = url+next_page_links.findAll("a")[-1]["href"]
        bool_next_page_exists = (next_page_links.findAll("a")[-1].span.text == "Next")
    except:
        bool_next_page_exists = 0

    if bool_next_page_exists and counter<2:
        retrieve_comments(next_page_link, product_name)

    else:
        pass

def run_program(phone_name):
    product_page_links = retrieve_all_phones_links(phone_name)
    for i,product_page_link in enumerate(product_page_links):
        product_page_soup, product_name = retrieve_product_page(product_page_link)
        if i==0:
            PRODUCT_NAME = product_name.split("(")[0].strip()
        if product_name.split("(")[0].strip() != PRODUCT_NAME:
            break
        comments_page_link = retrieve_comment_page_link(product_page_soup)
        retrieve_comments(comments_page_link, product_name)
        global counter
        counter = 0

    PRODUCT_NAME = ""
    global comments
    comments2 = comments.copy()
    comments = []
    return comments2

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--phone_name")
    parsed_args = arg.parse_args()
    run_program(parsed_args.phone_name)