# coding=utf-8

from queries import *
from utils import load_template, create_connection


def index(*args, **kwargs):
    db = create_connection()
    cursor = db.cursor()

    cursor.execute(select_all_categories)
    result = cursor.fetchall()
    cursor.close()

    box_string = ""

    for item in result:
        box_string += "<input id=\"{0}\" type=\"checkbox\" name=\"checkbox\" " \
                      "value=\"{1}\"/> <label for=\"{2}\">{3}</label><br />".format(item[0], item[1], item[0], item[1])

    sidebar_form = "\n    <form name=\"search\" action=\"\" method=\"POST\">\n" \
                   "    Search query\n    <input type=\"text\" name=\"search_query\"></br>\n" \
                   "    Initial category\n    <div style=\"height: 6em; width: 12em; overflow: auto;\">\n" \
                   "    {0}\n    </div>\n        <input type=\"submit\" value=\"Submit\"/>\n        " \
                   "</form>\n        ".format(box_string)

    template = load_template('index') + sidebar_form + load_template('search_result')

    if 'search_result' in kwargs:
        content_string = "<ul>"
        for item in kwargs['search_result']:
            content_string = content_string + "<li>" + item[0] + "  " + str(item[1]) + "</li>"
        content_string += "</ul>"
        template += content_string + load_template('footer')

    elif 'message' in kwargs:
        template += kwargs['message'] + load_template('footer')
    else:
        template += load_template('footer')

    return template


def search(*args, **kwargs):
    db = create_connection()
    cursor = db.cursor()

    try:
        query = kwargs['query_string'].get('search_query')[0]
        cats = []
        cats = cats + (kwargs['query_string'].get('checkbox'))

        cursor.execute(sql_search_query(query, cats))
        result = cursor.fetchall()
        cursor.close()
        db.close()

        template = index(search_result=result)
    except:
        search_error = "Write your query and choose at least one category !(or we don't have stuff that you search for)"
        template = index(message=search_error)

    return template


def admin(*args, **kwargs):
    template = load_template('admin_header') + load_template('footer')
    return template


def view_category(*args, **kwargs):
    string = "<ul>"
    db = create_connection()
    connection = db.cursor()
    connection.execute(select_all_categories)
    result = connection.fetchall()
    connection.close()
    for item in result:
        string += "<li>" + item[1] + "</li>"
    string += "</ul> \n"
    template = load_template('admin_header') + string + load_template('footer')
    return template


def add_category(*args, **kwargs):
    template = load_template('admin_header') + \
               load_template('add_category') + \
               load_template('footer')
    return template


def save_category(*args, **kwargs):
    cat = kwargs['query_string'].get('category')
    db = create_connection()
    cursor = db.cursor()
    try:
        cursor.execute(insert_category(str(cat[0])))
        db.commit()
    except:
        db.rollback()

    cursor.close()
    db.close()

    template = load_template('admin_header') + load_template('footer')
    return template


def view_product(*args, **kwargs):
    string = "<ul>"
    db = create_connection()
    connection = db.cursor()
    connection.execute(select_all_products)
    result = connection.fetchall()
    connection.close()
    for item in result:
        string += "<li><a href=\"/admin/view_product?name={0}\">{0}</a></li>".format(item[1])

    string += "</ul>"
    template = load_template('admin_header') + string + load_template('footer')
    return template


def add_product(*args, **kwargs):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute(select_all_categories)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    string = ""
    for item in result:
        string += "<option>" + item[1] + "</option>"

    add_product_form = "<form name=\"add_prod\" action=\"/admin/add_product\" method=\"POST\">" \
                       "Product name : <input type=\"text\" name=\"product_name\"></br>" \
                       "Product price : <input type=\"text\" name=\"product_price\"></br>" \
                       "Initial category : <select name=\"init_cat\">{0}</select>" \
                       "<input type=\"submit\" value=\"Submit\"></form>".format(string)

    template = load_template('admin_header') + \
               add_product_form + \
               load_template('footer')
    return template


def save_product(*args, **kwargs):
    prod_name = kwargs['query_string'].get('product_name')[0]
    prod_price = kwargs['query_string'].get('product_price')[0]
    init_cat = kwargs['query_string'].get('init_cat')[0]

    db = create_connection()
    cursor = db.cursor()
    try:
        cursor.execute(insert_product(str(prod_name), float(prod_price), str(init_cat)))
        db.commit()
    except ValueError:
        db.rollback()
        template = load_template('admin_header') + "VALUE ERROR" + load_template('footer')
        return template

    except db.Error as e:
        print "Error code %s" % e.errno
        db.rollback()

    cursor.close()
    db.close()

    template = load_template('admin_header') + load_template('footer')
    return template


def view_products_cat(*args, **kwargs):
    product_name = kwargs['query_string'].get('name')[0]
    db = create_connection()
    cursor = db.cursor()
    cursor.execute(sql_categories_for_product(product_name))
    result = cursor.fetchall()
    cursor.close()

    cat_for_prod = ""
    excluded_cats = []
    for item in result:
        cat_for_prod += "<option selected=\"selected\">" + item[0] + "</option>"
        excluded_cats.append(item[0])

    cursor = db.cursor()
    cursor.execute(sql_rest_of_cats(excluded_cats))
    result = cursor.fetchall()
    cursor.close()

    other_cats = ""
    for item in result:
        other_cats += "<option>" + item[0] + "</option>"

    form = "<form name=\"add_prod\" action=\"/admin/add_categories_to_product\" method=\"POST\">" \
           "<table style=\"width: 100%\" cellpadding=\"3\" cellspacing=\"0\"><tr><td style=\"width:33%\">" \
           "Categories<select multiple name=\"init_cat\">{0}</select> </td>" \
           "<td align=\"center\" style=\"width:33%\"><input type=\"Button\" value=\">>\" onClick=\"SelectMoveRows(document.add_prod.init_cat, document.add_prod.other_cat)\"><br>" \
           "<input type=\"Button\" value=\"<<\" onClick=\"SelectMoveRows(document.add_prod.other_cat, document.add_prod.init_cat)\"></td>" \
           "<td style=\"width:33%\">Other categories <select multiple name=\"other_cat\">{1}</select></td></tr></table>" \
           "<input type=\"submit\" value=\"Save\"></form>".format(cat_for_prod, other_cats)
    template = load_template('admin_header') + "Product :" + product_name + form + load_template('footer')
    return template


def add_categories_to_product(*args, **kwargs):
    cat_list = kwargs['query_string'].get('init_cat')

    return cat_list