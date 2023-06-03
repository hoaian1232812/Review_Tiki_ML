import csv

import requests
import json

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
url_page = "https://tiki.vn/api/v2/products?limit=40&include=advertisement&aggregations=2&trackity_id=6f3e60f3-58ba-19a8-5351-4b33c80c7de0&q=%C4%91i%E1%BB%87n+tho%E1%BA%A1i&page={}"
def crawl_product_id():
    product_list = []
    i = 1
    while (True):
        print("Crawl page: ", i)
        print(url_page.format(i))
        response = requests.get(url_page.format(i), headers=headers)

        if (response.status_code != 200):
            break

        products = json.loads(response.text)["data"]
        if (len(products) == 0):
            break

        for product in products:
            product_id = str(product["id"])
            print("Product ID: ", product_id)
            product_list.append(product_id)
        i += 1
    return product_list, i

def crawl_product(product_list=[]):
    product_detail_list = []
    url = "https://tiki.vn/api/v2/products/{}"
    for product_id in product_list:
        response = requests.get(url.format(product_id), headers=headers)
        if(response.status_code == 200):
            product_detail_list.append(response.text)
            print("Crawl_product",product_id,response.status_code)
    return product_detail_list

def crawl_review_product(product_list=[]):
    review_list = []
    url = "https://tiki.vn/api/v2/reviews?limit=5&include=comments,contribute_info,attribute_vote_summary&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page={}&spid={}&product_id={}&seller_id=1"
    for product_id in product_list:
        i = 1
        print(url.format(i, product_id, product_id))
        while(True):
            response = requests.get(url.format(i, product_id, product_id), headers=headers)
            if (response.status_code != 200):
                print('Lỗi')
                break
            review_data = json.loads(response.text)['data']
            if (len(review_data) == 0):
                break
            for review in review_data:
                print("Review ID: ", review['id'], "product", product_id)
                review_list.append(review)
            i += 1
    return review_list


def adjust_product(product):
    try:
        e = json.loads(product)
    except json.JSONDecodeError:
        return None
    if not e.get("id", False):
        return None
    # for field in flatten_field:
    #     if field in e:
    #         e[field] = json.dumps(e[field], ensure_ascii=False).replace('\n','')
    return e


def save_product_list(product_json_list, review=False):
    if(review):
        product_file = "D:\TL_BT\Machine Learning\mobile_review_tiki.csv"
    else:
        product_file = "D:\TL_BT\Machine Learning\mobile_tiki.csv"
    file = open(product_file, "w",newline='',encoding='utf-8-sig')
    csv_writer = csv.writer(file)
    count = 0
    for p in product_json_list:
        if p is not None:
            if count == 0:
                header = p.keys()
                csv_writer.writerow(header)
                count += 1
            values = [p.get(key,'') for key in header]
            csv_writer.writerow(values)
    file.close()
    print("Save file: ", product_file)
product_list, page = crawl_product_id()
products = crawl_product(product_list)
product_json_list = [adjust_product(p) for p in products]
save_product_list(product_json_list)
review_json_list = crawl_review_product(product_list)
save_product_list(review_json_list, review=True)
