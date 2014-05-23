URL_MAP = [('/', 'index', 'GET'),
           ('/', 'search', 'POST'),
           ('/admin', 'admin', 'GET'),
           ('/admin/view_product', 'view_product', 'GET'),
           ('/admin/view_category', 'view_category', 'GET'),
           ('/admin/add_category', 'add_category', 'GET'),
           ('/admin/add_category', 'save_category', 'POST'),
           ('/admin/add_product', 'add_product', 'GET'),
           ('/admin/add_product', 'save_product', 'POST'),
           ('/admin/view_product?', 'view_products_cat', 'GET'),
           ('/admin/add_categories_to_product', 'add_categories_to_product', 'POST')]


