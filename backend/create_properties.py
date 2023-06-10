import os
import django
from django.contrib.auth.hashers import make_password
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()



query = f'''
DROP PROCEDURE IF EXISTS insert_properties;

CREATE PROCEDURE insert_properties()
BEGIN
	DELETE FROM apis_property_photos;
	DELETE FROM apis_property_rules;
	DELETE FROM apis_property_services;
	DELETE FROM apis_property;
	DELETE FROM apis_photo;
	DELETE FROM apis_service;
	DELETE FROM apis_rule;
	
	INSERT INTO apis_photo (photo, owner_id)
	SELECT '/properties/Imagen_1.jpg', id FROM apis_user WHERE dni = '27883209C'
	UNION ALL
	SELECT '/properties/Imagen_2.jpg', id FROM apis_user WHERE dni = '27883209C'
	UNION ALL
	SELECT '/properties/Imagen_3.jpg', id FROM apis_user WHERE dni = '27883209C'
	UNION ALL
	SELECT '/properties/Imagen_4.jpg', id FROM apis_user WHERE dni = '27883209C'
	UNION ALL
	SELECT '/properties/Imagen_5.jpg', id FROM apis_user WHERE dni = '56974511B'
	UNION ALL
	SELECT '/properties/Imagen_6.jpg', id FROM apis_user WHERE dni = '56974511B'
	UNION ALL
	SELECT '/properties/Imagen_7.jpg', id FROM apis_user WHERE dni = '56974511B'
	UNION ALL
	SELECT '/properties/Imagen_8.jpg', id FROM apis_user WHERE dni = '56974511B'
	UNION ALL
	SELECT '/properties/Imagen_9.jpg', id FROM apis_user WHERE dni = '27883209C'
	UNION ALL
	SELECT '/properties/Imagen_10.jpg', id FROM apis_user WHERE dni = '56974511B'
	UNION ALL
	SELECT '/properties/Imagen_11.jpg', id FROM apis_user WHERE dni = '56974511B';
	
	INSERT INTO apis_service (`name`) VALUES ('WiFi'), ('Aire acondicionado'), ('Calefacción'), ('Lavadora');
	INSERT INTO apis_rule (`name`) VALUES ('No se permite fumar'), ('No se permiten mascotas'), ('No se permiten hacer fiestas');
	
	
	INSERT INTO apis_property (title, localization, price, `type`, dormitories, size, baths, owner_id)
	SELECT 'Piso en el centro de Sevilla', 'Ronda de Triana-Patrocinio-Turruñuelo, Sevilla', 800, 'Inmueble completo', 3, 120, 2, id FROM apis_user 
	WHERE dni = '27883209C'
	
	UNION ALL
	SELECT 'Habitación con baño privado', 'Camas, Camas, Sevilla 41900', 400, 'Habitacion', 1, 20, 1, id FROM apis_user WHERE dni = '27883209C'
	UNION ALL
	
	SELECT 'Habitación en un 5º piso con ascensor', 'Avenida de Pino Montano 5, 41016 Sevilla', 300,'Habitacion',1 ,30 ,0 ,id FROM apis_user 
	WHERE dni = '56974511B'
	UNION ALL
	
	SELECT 'Cama en habitación con otro compañero', 'Los Remedios, Sevilla, 41011', 100, 'Cama', 1, 20, 0, id FROM apis_user WHERE dni = '56974511B'
	UNION ALL
	SELECT '3ra planta, sin ascensor, piso completo', 'Arco norte - Avda España, Dos Hermanas, Sevilla 41701', 700, 'Inmueble completo', 2, 70, 1,id 
	FROM apis_user WHERE dni = '56974511B'
	
	UNION ALL
	SELECT 'Piso completo en Sevilla, 8º planta', 'Avenida de Pino Montano 2, 41015 Sevilla', 500,'Inmueble completo',2 ,75 ,1 ,id FROM apis_user 
	WHERE dni = '27883209C';
	
	
	
	
	
	INSERT INTO apis_property_photos (property_id, photo_id)
	SELECT p.id, ph.id FROM apis_property p, apis_photo ph
	WHERE (p.title = 'Piso en el centro de Sevilla' AND ph.photo = '/properties/Imagen_2.jpg')
	OR (p.title = 'Piso en el centro de Sevilla' AND ph.photo = '/properties/Imagen_3.jpg')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND ph.photo = '/properties/Imagen_5.jpg')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND ph.photo = '/properties/Imagen_6.jpg')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND ph.photo = '/properties/Imagen_7.jpg')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND ph.photo = '/properties/Imagen_8.jpg')
	OR (p.title = 'Habitación con baño privado' AND ph.photo = '/properties/Imagen_4.jpg')
	OR (p.title = 'Cama en habitación con otro compañero' AND ph.photo = '/properties/Imagen_1.jpg')
	OR (p.title = 'Piso completo en Sevilla, 8º planta' AND ph.photo = '/properties/Imagen_9.jpg')
	OR (p.title = 'Habitación en un 5º piso con ascensor' AND ph.photo = '/properties/Imagen_10.jpg')
	OR (p.title = 'Habitación en un 5º piso con ascensor' AND ph.photo = '/properties/Imagen_11.jpg');
	
	INSERT INTO apis_property_rules (property_id, rule_id)
	SELECT p.id, r.id FROM apis_property p, apis_rule r
	WHERE (p.title = 'Piso en el centro de Sevilla' AND r.`name` = 'No se permite fumar')
	OR (p.title = 'Habitación con baño privado' AND r.`name` = 'No se permiten mascotas')
	OR (p.title = 'Piso en el centro de Sevilla' AND r.`name` = 'No se permite fumar')
	OR (p.title = 'Cama en habitación con otro compañero' AND r.`name` = 'No se permiten hacer fiestas');
	
	
	INSERT INTO apis_property_services (property_id, service_id)
	SELECT p.id, s.id FROM apis_property p, apis_service s
	WHERE (p.title = 'Piso en el centro de Sevilla' AND s.`name` = 'WiFi')
	OR (p.title = 'Piso en el centro de Sevilla' AND s.`name` = 'Aire acondicionado')
	OR (p.title = 'Piso en el centro de Sevilla' AND s.`name` = 'Calefacción')
	OR (p.title = 'Cama en habitación con otro compañero' AND s.`name` = 'Lavadora')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND s.`name` = 'Calefacción')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND s.`name` = 'Aire acondicionado')
	OR (p.title = '3ra planta, sin ascensor, piso completo' AND s.`name` = 'Lavadora');


END;


CALL insert_properties();
COMMIT;

'''


with connection.cursor() as cursor:
    cursor.execute(query)
