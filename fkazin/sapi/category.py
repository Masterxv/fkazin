from ..utils.utils import dict_fetchall, where_clause, update_clause
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError


def GET(filters):
    response = {"data": {}, 'status': 200}
    where = where_clause(filters)

    sql = """SELECT `category`.`category_id`,
            `category`.`parent`,
            `category`.`name`,
            `category`.`created_dt`,
            `category`.`active`,
            `category`.`updated_dt`
        FROM `fk_az`.`category` """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, filters)
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-CATEGORY-GET'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-CATEGORY-GET'}
        response['status'] = 500

    if len(data):
        response['data'] = {'category_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def POST(fields):
    response = {"data": {}, 'status': 201}

    sql = """
        INSERT INTO `fk_az`.`category`
            (`category`.`parent`,
              `category`.`name`,
              `category`.`active`)
        values(
            %(parent)s, %(name)s, %(active)s
        )
    """

    sql_last_id = "SELECT LAST_INSERT_ID()"

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.execute(sql_last_id)
                data = cursor.fetchall()
                cursor.close()
                category_id = data[0][0]
                response['data'] = GET({'category_id': category_id})['data']

    except OperationalError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-CATEGORY-POST'}
        response['status'] = 400

    except IntegrityError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-DEFINITION-CATEGORY-POST'}
        response['status'] = 500

    except DatabaseError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DEFINITION-CATEGORY-POST'}
        response['status'] = 500

    return response


def PUT(fields):
    response = {"data": {}, 'status': 200}

    update = update_clause(fields)

    if update:
        update = update + " , updated_dt=current_timestamp "

    sql = "update `fk_az`.`category` " + update + "where category_id = %(category_id)s"

    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                cursor.close()

        response['data'] = GET({'category_id': fields['category_id']})['data']
        if not response['data']:
            response['status'] = 204

    except OperationalError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-CATEGORY-PUT'}
        response['status'] = 400

    except IntegrityError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-DUP-CATEGORY-PUT'}
        response['status'] = 500

    except DatabaseError as e:
        response['data'] = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-CATEGORY'}
        response['status'] = 500

    return response


def DELETE(category_id):
    response = {"data": {}, 'status': 200}
    update = PUT({'category_id': category_id, 'active': 0})

    response['data'] = GET({'category_id': category_id})['data']

    return response
