from ..utils.utils import dict_fetchall, where_clause, update_clause
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError


def GET(filters):
    response = {"data": {}, 'status': 200}
    where = where_clause(filters)

    sql = """SELECT `products`.`pid`,
            `products`.`name`,
            `products`.`description`,
            `products`.`brand`,
            `products`.`selling_price`,
            `products`.`actual_price`,
            `products`.`category_id`,
            `products`.`link`,
            `products`.`src`,
            `products`.`active`,
            `products`.`created_dt`
        FROM `fk_az`.`products` """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, filters)
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCTS-GET'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-PRODUCTS-GET'}
        response['status'] = 500

    if len(data):
        response['data'] = {'product_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def POST(fields):
    response = {"data": {}, 'status': 201}

    sql = """
        INSERT INTO `fk_az`.`products`
            (`pid`,
            `name`,
            `description`,
            `brand`,
            `selling_price`,
            `actual_price`,
            `category_id`,
            `link`,
            `src`)
        values(
            %(pid)s, %(name)s, %(description)s, %(brand)s, %(selling_price)s, %(actual_price)s, 
            %(category_id)s, %(link)s, %(src)s
        )
    """

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.close()
                data = fields

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-POST'}
        response['status'] = 400

    except IntegrityError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-DEFINITION-POST'}
        response['status'] = 500

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-POST'}
        response['status'] = 500

    response['data'] = data

    return response


def PUT(fields):
    response = {"data": {}, 'status': 200}

    update = update_clause(fields)

    sql = "update `fk_az`.`products` " + update + "where pid = %(pid)s"

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.close()

        response['data'] = GET({'pid': fields['pid']})['data']
        if not response['data']:
            response['status'] = 204

    except OperationalError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PUT'}
        response['status'] = 400

    except IntegrityError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-PRODUCT-PUT'}
        response['status'] = 500

    except DatabaseError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-PRODUCT'}
        response['status'] = 500

    return response


def DELETE(pid):
    response = {"data": {}, 'status': 200}
    update = PUT({'pid': pid, 'active': 0})

    response['data'] = GET({'pid': pid})['data']

    return response
