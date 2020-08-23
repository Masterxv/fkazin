from urllib.parse import parse_qs


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def parse_qs_custom(qs):
    filters = {}
    qs_list = parse_qs(qs)

    for key in qs_list:
        filters[key] = ','.join(qs_list[key])

    return filters


def where_clause(filters):
    where = "where 1=1 "

    for key in filters:
        where = where + ' and ' + key + ' like ' + '%(' + key + ')s '

    return where


def update_clause(filters, ignore=[]):
    update = "SET "

    for key in filters:
        if key not in ignore:
            update = update + key + ' = ' + '%(' + key + ')s ,'

    return update[:-1]


def insert_keys_values(fields):
    kv = {'keys': '', 'values': ''}

    for key in fields:
        kv['keys'] = kv['keys'] + key + ' ,'
        kv['values'] = kv['values'] + '%(' + key + ')s ,'

    if kv['keys']:
        kv['keys'] = kv['keys'][:-1]

    if kv['values']:
        kv['values'] = kv['values'][:-1]

    return kv

