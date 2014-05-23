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
    query = 'SELECT DISTINCT product.name, product.price FROM category_producs \
    JOIN product ON product_id = product.id \
    JOIN category ON category_id = category.id \
    WHERE category.name IN (' + str(cat_array).strip('[]') + ')AND product.name="' + query_string + '"'
    print query
    return query
