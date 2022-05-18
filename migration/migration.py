import xmlrpc.client
url_odoo14 = "http://localhost:8069"
db_odoo14 = 'odoo14'
user_name_db_odoo14 = 'admin'
password_db_odoo14 = 'admin'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_odoo14))
model_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_odoo14))
version_db_odoo14 = common_1.version()

url_odoo15 = "http://localhost:8045"
db_odoo15 = 'odoo1'
user_name_db_odoo15 = 'admin'
password_db_odoo15 = 'admin'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_odoo15))
model_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_odoo15))
version_db_odoo15 = common_2.version()
print("odoo14", version_db_odoo14)
print("odoo15", version_db_odoo15)

odoo_14 = common_1.authenticate(db_odoo14, user_name_db_odoo14,
                                password_db_odoo14, {})
odoo_15 = common_2.authenticate(db_odoo15, user_name_db_odoo15,
                                password_db_odoo15, {})
model_contacts = model_1.execute_kw(db_odoo14, odoo_14, password_db_odoo14,
                                    'res.partner', 'search_read',
                                    [[]], {'fields': ['id', 'name', 'email']})
print("contacts", model_contacts)
for line in model_contacts:
    new_data = model_2.execute_kw(db_odoo15, odoo_15, password_db_odoo14,
                                  'res.partner', 'create', [line])
