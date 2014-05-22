import MySQLdb
import sys

from settings import database
from queries import *
from utils import load_template

def index(*args, **kwargs):
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    connection = db.cursor()
    
    connection.execute(select_all_categories)
    result = connection.fetchall()
    connection.close()

    box_string = ""
     
    for item in result:
        box_string = box_string+\
                     "<input id=\"%s\" type=\"checkbox\" name=\"checkbox\" value=\"%s\"/> <label for=\"%s\">%s</label><br />" % (item[0], item[1], item[0], item[1])
        
    sidebar_form = """
    <form name="search" action="" method="POST">
    Search query
    <input type="text" name="search_query"></br>
    Initial category
    <div style="height: 6em; width: 12em; overflow: auto;">
    """+box_string+\
        """
    </div>
        <input type="submit" value="Submit"/>
        </form>
        """

    
    template = load_template('index')+sidebar_form+load_template('search_result')
    
    
    if 'search_result' in kwargs:
        content_string="<ul>"
        for item in kwargs['search_result']:
            content_string = content_string+"<li>"+item[0]+"  "+str(item[1])+"</li>"
        content_string = content_string + "</ul>"
        template = template + content_string+load_template('footer')

    elif 'message' in kwargs:
        template = template +kwargs['message']+\
                   load_template('footer')
    else:
        template = template + load_template('footer')
        
    return template

def search(*args, **kwargs):
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    cursor = db.cursor()

    try:
        query = kwargs['inp'].get('search_query')[0]
        cats = []
        cats = cats + (kwargs['inp'].get('checkbox'))
        
        cursor.execute(sql_search_query(query,cats))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        
        template = index(search_result=result)
    except:
        search_error= "Write your query and choose at least one category !(or we don't have stuff that you search for)"
        template= index(message=search_error)
        
    return template

def admin(*args, **kwargs):
    template = load_template('admin_header')+load_template('footer')
    return template
    

def view_category(*args, **kwargs):
    string = "<ul>"
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    connection = db.cursor()
    connection.execute(select_all_categories)
    result = connection.fetchall()
    connection.close()
    for item in result:
        string = string+"<li>"+item[1]+"</li>"
    string = string+"</ul> \n"
    template = load_template('admin_header')+string+load_template('footer')
    return template
    
def add_category(*args, **kwargs):
    
    template = load_template('admin_header')+\
               load_template('add_category')+\
               load_template('footer')
    return template

def save_category(*args, **kwargs):
    cat = kwargs['inp'].get('category')
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    cursor = db.cursor()
    try:
        cursor.execute(insert_category(str(cat[0])))
        db.commit()
    except:     
        db.rollback()
        
    cursor.close()
    db.close()
    
    template = load_template('admin_header')+load_template('footer')
    return template

def view_product(*args, **kwargs):
    string = "<ul>"
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    connection = db.cursor()
    connection.execute(select_all_products)
    result = connection.fetchall()
    connection.close()
    for item in result:
        string = string+"<li>"+item[1]+"</li>"
       
    string = string+"</ul>"
    template = load_template('admin_header')+string+load_template('footer')
    return template

def add_product(*args, **kwargs):
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    cursor = db.cursor()
    cursor.execute(select_all_categories)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    string = ""
    for item in result:
        string = string+"<option>"+item[1]+"</option>"
    
    template = load_template('admin_header')+\
               """
               <form name="add_prod" action="/admin/add_product" method="POST">
Product name : <input type="text" name="product_name"></br>
Product price : <input type="text" name="product_price"></br>
Initial category : <select name="init_cat">"""+ string +"""
<option>cat 1</option>
<option>cat 2</option>

</select>
<input type="submit" value="Submit">
</form>

               """+\
               load_template('footer')
    return template

def save_product(*args, **kwargs):
    prod_name = kwargs['inp'].get('product_name')[0]
    prod_price = kwargs['inp'].get('product_price')[0]
    init_cat = kwargs['inp'].get('init_cat')[0]
    print init_cat
    
    db = MySQLdb.connect(database['host'],
                         database['user'],
                         database['passwd'],
                         database['db'])
    cursor = db.cursor()
    try:
        cursor.execute(insert_product(str(prod_name),float(prod_price), str(init_cat)))
        db.commit()
    except ValueError:
        template = load_template('admin_header')+"VALUE ERROR"+load_template('footer')
        return template
        
    except db.Error as e:
        print "Error code %s" % e.errno
        cursor._executed
        db.rollback()
        
    cursor.close()
    db.close()
    
    template = load_template('admin_header')+load_template('footer')
    return template
    
