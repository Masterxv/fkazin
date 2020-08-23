from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from ..xapi import categories
import requests
import json
from ..utils.utils import parse_qs_custom
import re
from urllib.parse import urlparse


def home(request):
    return render(request, 'admin_home.html')


def add_amazon(request):
    context_data = {'categories': categories.leaves()}
    data = {}

    if request.META['QUERY_STRING']:
        data = parse_qs_custom(request.META['QUERY_STRING'].replace(u'\xa0', u''))
        if 'link' in data:
            o = urlparse(data['link'])
            data['link'] = o.scheme + "://" + o.netloc + o.path + "?tag=t00fd-21"
            data['pid'] = o.path.split("/")[-1]

        if 'actual_price' in data:
            data['actual_price'] = data['actual_price'].replace("\u20b9", '').replace(" ", "").replace(",", "").strip()
            data['actual_price'] = data['actual_price'].split("-")[0]
        if 'selling_price' in data:
            data['selling_price'] = data['selling_price'].replace("\u20b9", '').replace(" ", "").replace(",", "").strip()
            data['selling_price'] = data['selling_price'].split("-")[0]

        context_data['data'] = data

    return render(request, 'add_amazon.html', context_data)


def add_flipkart(request):
    context_data = {'categories': categories.leaves()}
    return render(request, 'add_flipkart.html', context_data)


def edit_categories(request):
    context_data = {'categories': categories.every()}
    return render(request, 'edit_categories.html', context_data)


def add_category(request):
    response = "Error Creating Category - ERR-1"
    if request.method == 'POST':
        if 'name' in request.POST and 'active' in request.POST and 'parent' in request.POST:
            response = categories.add(request.POST['name'], request.POST['active'], request.POST['parent'])

    return redirect("./edit-categories?message=" + response)


def update_category(request):
    response = "Error Updating Category - ERR-1"
    if request.method == 'POST':
        if 'category_id' in request.POST and 'name' in request.POST and 'active' in request.POST \
                and 'parent' in request.POST:
            response = categories.update(request.POST['category_id'], request.POST['name'], request.POST['active'],
                                         request.POST['parent'])

    return redirect("./edit-categories?message=" + response)


def approve_products(request):
    return render(request, 'approve_products.html')


def fk_product_by_id(request):
    product_details = {
        'pid': '',
        'link': '',
        'name': '',
        'description': '',
        'brand': '',
        'selling_price': '',
        'actual_price': '',
        'image_small': '',
        'image_medium': '',
        'image_large': ''
    }
    pid = request.GET['pid']
    url = "https://affiliate-api.flipkart.net/affiliate/1.0/product.json?id=" + pid

    payload = {}
    headers = {
        'Fk-Affiliate-Id': 'tnhpindia',
        'Fk-Affiliate-Token': 'f40996af11994496b1ffd196a75e89fb'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    jsondata = json.loads(response.text)
    product_details['pid'] = jsondata['productBaseInfoV1']['productId']
    product_details['name'] = jsondata['productBaseInfoV1']['title']
    product_details['link'] = jsondata['productBaseInfoV1']['productUrl']
    product_details['brand'] = jsondata['productBaseInfoV1']['productBrand']
    product_details['description'] = jsondata['productBaseInfoV1']['productDescription']

    try:
        product_details['actual_price'] = jsondata['productBaseInfoV1']['maximumRetailPrice']['amount']
        product_details['selling_price'] = jsondata['productBaseInfoV1']['maximumRetailPrice']['amount']
    except:
        print("No MRP")

    try:
        if not product_details['actual_price']:
            product_details['actual_price'] = jsondata['productBaseInfoV1']['flipkartSellingPrice']['amount']
            product_details['selling_price'] = jsondata['productBaseInfoV1']['flipkartSellingPrice']['amount']
    except:
        print("No selling price")

    try:
        product_details['selling_price'] = jsondata['productBaseInfoV1']['flipkartSpecialPrice']['amount']
    except:
        print("No special")

    try:
        product_details['image_small'] = jsondata['productBaseInfoV1']['imageUrls']['200x200']
    except:
        print("No 200")

    try:
        product_details['image_medium'] = jsondata['productBaseInfoV1']['imageUrls']['400x400']
    except:
        print("No 400")

    try:
        product_details['image_large'] = jsondata['productBaseInfoV1']['imageUrls']['800x800']
    except:
        print("No 800")

    return JsonResponse(product_details, safe=False)


def test_az(request):
    url = "https://www.amazon.in/Bourge-Loire-63-Running-Shoes-8-Loire-63-D-Grey-08/dp/B07MPZ56SM?ref_" \
          "=Oct_DLandingS_D_d1284c06_62&smid=AT95IG9ONZD7S"

    payload = {}
    headers = {

    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return HttpResponse(response.text)


def remove_control_chart(s):
    return re.sub(r'\\x..', '', s)
