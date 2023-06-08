import os
import django
from django.contrib.auth.hashers import make_password
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


users = [
    ('27883209C', 'Manuel', 'Moreno Rodríguez', 'manuel_94', 'manuelrodriguez@alum.us.es', 'hola1234', '+34672451098', '/users/Foto_perfil_1.png', 1, 0),
    ('11974509A', 'Pepe', 'García Luque', 'pepgar', 'pepgar@gmail.com', 'hola1234', '+34632450461', '', 1, 0),
    ('29494873L', 'Jesús', 'Ballestero López', 'jesballop', 'jesballop@alum.us.es', 'adminPass', '+34623406798', '/users/user-avatar.png', 1, 1),
    ('56974511B', 'Carlos', 'Ruiz Galeano', 'car', 'car@gmail.com', 'hola1234', '+34711450461', '', 1, 0),
    ('97376037H', 'Lucía', 'Romero Vera', 'lucia_00', 'lucia2000@gmail.com', 'hola1234', '+34690335690', '/users/Foto_perfil_2.jpg', 1, 0)
]


users_encrypted = []
for user in users:
    encrypted_password = make_password(user[5])
    user_encrypted = user[:5] + (encrypted_password,) + user[6:]
    users_encrypted.append(user_encrypted)


values = ',\n'.join(str(user) for user in users_encrypted)
query = f'''
DROP PROCEDURE IF EXISTS insert_users;

CREATE PROCEDURE insert_users()
BEGIN
    DELETE FROM apis_property_photos;
	DELETE FROM apis_property_rules;
	DELETE FROM apis_property_services;
	DELETE FROM apis_photo;
	DELETE FROM django_admin_log;
	DELETE FROM token_blacklist_blacklistedtoken;
	DELETE FROM token_blacklist_outstandingtoken;
	DELETE FROM apis_property;
	DELETE FROM apis_owner;
	DELETE FROM apis_student;
	DELETE FROM apis_user;

    INSERT INTO apis_user (`dni`, `name`, `surname`, `username`, `email`, `password`, `telephone`, `photo`, `isActive`, `isAdministrator`) 
    VALUES {values};

    INSERT INTO apis_owner (user_ptr_id) SELECT id FROM apis_user WHERE dni IN ('27883209C','56974511B');
    INSERT INTO apis_student (user_ptr_id) SELECT id FROM apis_user WHERE dni IN ('11974509A','97376037H');
END;

CALL insert_users();
COMMIT;
'''


with connection.cursor() as cursor:
    cursor.execute(query)
