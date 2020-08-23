from ..utils.utils import dict_fetchall, where_clause
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError


def GET(filters):
    response = {"data": {}, 'status': 200}
    where = where_clause(filters)

    sql = """SELECT `product_image`.`image_id`,
            `product_image`.`pid`,
            `product_image`.`img_grp`,
            `product_image`.`image_size`,
            `product_image`.`active`,
            `product_image`.`image_link`,
            `product_image`.`created_dt`
        FROM `fk_az`.`product_image` """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, filters)
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCT-IMAGES-GET'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-PRODUCT-IMAGES-GET'}
        response['status'] = 500

    if len(data):
        response['data'] = {'product_images_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def DELETE(fields):
    response = {"data": {}, 'status': 200}

    sql = "update `fk_az`.`product_image` set active=0 where pid = %(pid)s"

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.close()
        response['data'] = GET({'pid': fields['pid']})['data']

        if not response['data']:
            response['status'] = 204

    except OperationalError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCT'
                                                                                    '-IMAGES-DELETE'}
        response['status'] = 400

    except IntegrityError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-PRODUCT-IMAGES-DELETE'}
        response['status'] = 500

    except DatabaseError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-PRODUCT-IMAGES'}
        response['status'] = 500

    return response
