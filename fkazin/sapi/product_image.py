from ..utils.utils import dict_fetchall, where_clause, update_clause, insert_keys_values
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError


def GET(filters):
    response = {"data": {}, 'status': 200}
    where = where_clause(filters)

    sql = """SELECT `product_image`.`image_id`,
            `product_image`.`pid`,
            `product_image`.`img_grp`,
            `product_image`.`image_size`,
            `product_image`.`image_link`,
            `product_image`.`active`,
            `product_image`.`created_dt`
        FROM `fk_az`.`product_image` """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, filters)
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCT-IMAGE-GET'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-PRODUCT-IMAGE-GET'}
        response['status'] = 500

    if len(data):
        response['data'] = {'product_image_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def POST(fields):
    response = {"data": {}, 'status': 201}
    kv = insert_keys_values(fields)

    sql = "INSERT INTO `fk_az`.`product_image` (" + kv['keys'] + ") values(" + kv['values'] + ")"

    sql_last_id = "SELECT LAST_INSERT_ID()"

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.execute(sql_last_id)
                data = cursor.fetchall()
                cursor.close()
                image_id = data[0][0]
                response['data'] = GET({'image_id': image_id})['data']

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCT-IMAGE-POST'}
        response['status'] = 400

    except IntegrityError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-PRODUCT-IMAGE-POST'}
        response['status'] = 500

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-PRODUCT-IMAGE-POST'}
        response['status'] = 500

    return response


def PUT(fields):
    response = {"data": {}, 'status': 200}

    update = update_clause(fields, ignore=['pid', 'image_id'])

    sql = "update `fk_az`.`product_image` " + update + "where pid = %(pid)s and image_id = %(image_id)s"

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.close()

        response['data'] = GET({'pid': fields['pid'], 'image_id': fields['image_id']})['data']
        if not response['data']:
            response['status'] = 204

    except OperationalError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCT-IMAGE'
                                                                                    '-PUT'}
        response['status'] = 400

    except IntegrityError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-PRODUCT-IMAGE-PUT'}
        response['status'] = 500

    except DatabaseError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-PRODUCT-IMAGE'}
        response['status'] = 500

    return response


def DELETE(fields):
    response = {"data": {}, 'status': 200}
    update = PUT({'pid': fields['pid'], 'image_id': fields['image_id'], 'active': 0})
    response['data'] = GET({'pid': fields['pid'], 'image_id': fields['image_id']})['data']

    return response
