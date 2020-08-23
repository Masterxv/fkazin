import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import products as PRODUCTS, product as PRODUCT, category as CATEGORY, categories as CATEGORIES
from . import product_images as PRODUCT_IMAGES, product_image as PRODUCT_IMAGE
from ..utils import utils
from django.contrib.auth.decorators import user_passes_test
# from ..identity import models as identity


@csrf_exempt
# @user_passes_test(identity.auth, login_url="/identity/account/login/", redirect_field_name=None)
def products(request):

    response = {'data': {}, 'status': 400}

    if request.method == 'GET':
        filters = utils.parse_qs_custom(request.META['QUERY_STRING'])
        response = PRODUCTS.GET(filters)
    else:
        return HttpResponse('', status=405)

    return JsonResponse(response['data'], status=response['status'], safe=False)


@csrf_exempt
# @user_passes_test(identity.auth, login_url="/identity/account/login/", redirect_field_name=None)
def product(request):

    response = {'data': {}, 'status': 400}

    if request.method == 'GET':
        pid = request.get_full_path().split("/")[-1]
        response = PRODUCT.GET({'pid': pid})

    elif request.method == 'POST':
        body = json.loads(request.body)
        response = PRODUCT.POST(body)

    elif request.method == 'PUT':
        body = json.loads(request.body)
        if 'pid' in body:
            response = PRODUCT.PUT(body)

    elif request.method == 'DELETE':
        pid = request.get_full_path().split("/")[-1]
        response = PRODUCT.DELETE(pid)

    else:
        return HttpResponse('', status=405)

    return JsonResponse(response['data'], status=response['status'], safe=False)


@csrf_exempt
# @user_passes_test(identity.auth, login_url="/identity/account/login/", redirect_field_name=None)
def category(request):

    response = {'data': {}, 'status': 400}
    category_id = request.get_full_path().split("/")[-1]

    if request.method == 'GET':
        response = CATEGORY.GET({'category_id': category_id})

    elif request.method == 'POST':
        body = json.loads(request.body)
        response = CATEGORY.POST(body)

    elif request.method == 'PUT':
        body = json.loads(request.body)
        body['category_id'] = category_id
        response = CATEGORY.PUT(body)

    elif request.method == 'DELETE':
        response = CATEGORY.DELETE(category_id)

    else:
        return HttpResponse('', status=405)

    return JsonResponse(response['data'], status=response['status'], safe=False)


@csrf_exempt
# @user_passes_test(identity.auth, login_url="/identity/account/login/", redirect_field_name=None)
def categories(request):

    response = {'data': {}, 'status': 400}

    if request.method == 'GET':
        filters = utils.parse_qs_custom(request.META['QUERY_STRING'])
        response = CATEGORIES.GET(filters)
    else:
        return HttpResponse('', status=405)

    return JsonResponse(response['data'], status=response['status'], safe=False)


@csrf_exempt
# @user_passes_test(identity.auth, login_url="/identity/account/login/", redirect_field_name=None)
def product_images(request):

    response = {'data': {}, 'status': 400}
    pid = request.get_full_path().split("/")[-3]

    if request.method == 'GET':
        filters = utils.parse_qs_custom(request.META['QUERY_STRING'])
        filters['pid'] = pid
        response = PRODUCT_IMAGES.GET(filters)

    elif request.method == 'DELETE':
        response = PRODUCT_IMAGES.DELETE({'pid': pid})

    else:
        return HttpResponse('', status=405)

    return JsonResponse(response['data'], status=response['status'], safe=False)


@csrf_exempt
# @user_passes_test(identity.auth, login_url="/identity/account/login/", redirect_field_name=None)
def product_image(request):

    response = {'data': {}, 'status': 400}
    fields = utils.parse_qs_custom(request.META['QUERY_STRING'])
    fields['pid'] = request.get_full_path().split("/")[-3]
    fields['image_id'] = request.get_full_path().split("/")[-1]

    if request.method == 'GET':
        response = PRODUCT_IMAGE.GET(fields)

    elif request.method == 'POST':
        body = json.loads(request.body)
        body['pid'] = fields['pid']
        body['image_id'] = fields['image_id']
        response = PRODUCT_IMAGE.POST(body)

    elif request.method == 'PUT':
        body = json.loads(request.body)
        body['pid'] = fields['pid']
        body['image_id'] = fields['image_id']
        response = PRODUCT_IMAGE.PUT(body)

    elif request.method == 'DELETE':
        response = PRODUCT_IMAGE.DELETE(fields)

    else:
        return HttpResponse('', status=405)

    return JsonResponse(response['data'], status=response['status'], safe=False)
