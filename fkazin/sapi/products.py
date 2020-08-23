from ..utils.utils import dict_fetchall, where_clause
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
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-PRODUCTS-GET'}
        response['status'] = 400

    except DatabaseError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-PRODUCTS-GET'}
        response['status'] = 500

    if len(data):
        response['data'] = {"data": {'products_details': data}}

    return response
