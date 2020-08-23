from ..sapi import categories, category


def leaves():
    v_categories = categories.GET({'active': 1})['data']['categories_details']
    v_leaves = []

    for row in v_categories:
        is_parent = False
        print("checking: " + str(row['category_id']))
        for cat in v_categories:
            if row['category_id'] != cat['category_id']:
                print("-->checking parent: " + str(cat['category_id']))
                if cat['parent'] == row['category_id']:
                    is_parent = True
                    break
        if not is_parent:
            v_leaves.append(row)

    return v_leaves


def every():
    v_categories = {}
    v_categories = categories.GET({})
    if 'data' in v_categories and 'categories_details' in v_categories['data']:
        return v_categories['data']['categories_details']


def add(name, active=0, parent=None):
    if len(parent) == 0:
        parent = None

    response = category.POST({'name': name, 'active': active, 'parent': parent})

    if 'status' in response and response['status'] == 201:
        result = "Category Created"
    else:
        result = "Error Creating Category"

    return result


def update(category_id, name, active=0, parent=None):
    if len(parent) == 0:
        parent = None

    response = category.PUT({'category_id': category_id, 'name': name, 'active': active, 'parent': parent})

    if 'status' in response and response['status'] == 201:
        result = "Category Updated"
    else:
        result = "Error Updating Category"

    return result
