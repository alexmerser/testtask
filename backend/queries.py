# coding=utf-8

select_all_categories = 'SELECT * FROM category'
select_all_products = 'SELECT * FROM product'


def insert_category(cat_name):
    query = 'INSERT INTO category ( name ) VALUES ( "' + cat_name + '" );'
    return query


def insert_product(prod_name, prod_price, cat_name):
    query = 'CALL new_product_with_cat("%s", %s, "%s");' % (prod_name, prod_price, cat_name)
    return str(query)


def sql_search_query(query_string, cat_array):
    if query_string is "":
        ext_list = str(cat_array).strip('[]')
        query = "SELECT DISTINCT product.name, product.price FROM category_producs " \
            "JOIN product ON product_id = product.id " \
            "JOIN category ON category_id = category.id " \
            "WHERE category.name IN ({0})".format(ext_list)
    elif cat_array is None:
        query = "SELECT DISTINCT product.name, product.price FROM product WHERE product.name LIKE '%{0}%'".format(query_string)
    else:
        ext_list = str(cat_array).strip('[]')
        query = "SELECT DISTINCT product.name, product.price FROM category_producs " \
                "JOIN product ON product_id = product.id " \
                "JOIN category ON category_id = category.id " \
                "WHERE category.name IN ({0}) AND product.name LIKE '%{1}%'".format(ext_list, query_string)
        print query
    return query


def sql_categories_for_product(product_name):
    query = "SELECT DISTINCT category.name FROM category_producs " \
            "JOIN product ON product_id = product.id " \
            "JOIN category ON category_id = category.id " \
            "WHERE product.name=\"{0}\"".format(product_name)
    return query


def sql_rest_of_cats(cat_array):
    query = 'SELECT category.name FROM category WHERE category.name NOT IN ({0})'.format(
        str(cat_array).strip('[]').replace(" ", ""))
    return query


def sql_assign_product_to_category(prod_name, cat_list):
    ext_list = str(cat_list).strip('[]')
    query = "REPLACE INTO category_producs (product_id, category_id) SELECT product.id, category.id FROM " \
            "product JOIN category WHERE product.name='{0}' " \
            "AND category.name IN ({1});".format(prod_name[0], ext_list)
    return query


def sql_del_category_from_product(prod_name, cat_list):
    ext_list = str(cat_list).strip('[]')
    query = "DELETE FROM category_producs WHERE category_id NOT IN " \
            "(SELECT category.id FROM category WHERE category.name IN ({1})) " \
            "AND product_id IN " \
            "(SELECT product.id FROM product WHERE product.name = '{0}');".format(prod_name[0], ext_list)
    return query


def sql_products_for_category(cat_id):
    query = "SELECT DISTINCT product.name FROM category_producs " \
            "JOIN product ON product_id = product.id " \
            "JOIN category ON category_id = category.id " \
            "WHERE category_id={0}".format(cat_id)
    print query
    return query


def sql_rest_of_prods(prod_array):
    if prod_array == []:
        query = 'SELECT product.name FROM product'
    else:
        query = 'SELECT product.name FROM product WHERE product.name NOT IN ({0})'.format(
            str(prod_array).strip('[]').replace(" ", ""))
    print query
    return query


def sql_add_product_to_category(category_id, prod_list):
    ext_list = str(prod_list).strip('[]')
    query = "REPLACE INTO category_producs (product_id, category_id) SELECT product.id, category.id FROM " \
            "product JOIN category WHERE category.id={0} " \
            "AND product.name IN ({1});".format(category_id, ext_list)
    print query
    return query


def sql_del_product_from_category(category_id, prod_list):
    ext_list = str(prod_list).strip('[]')
    query = "DELETE FROM category_producs WHERE product_id NOT IN " \
            "(SELECT product.id FROM product WHERE product.name IN ({1})) " \
            "AND category_id={0};".format(category_id, ext_list)
    return query