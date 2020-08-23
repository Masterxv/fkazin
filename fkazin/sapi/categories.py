from ..utils.utils import dict_fetchall, where_clause
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError


def GET(filters):
    response = {"data": {}, 'status': 200}
    where = where_clause(filters)

    sql = """SELECT `category`.`category_id`,
            `category`.`parent`,
            `category`.`name`,
            `category`.`active`,
            `category`.`created_dt`,
            `category`.`updated_dt`
        FROM `fk_az`.`category` """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, filters)
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-CATEGORIES-GET'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-CATEGORIES-GET'}
        response['status'] = 500

    if len(data):
        response['data'] = {'categories_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response

