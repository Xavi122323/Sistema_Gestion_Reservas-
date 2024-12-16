# Sistema de Gestión de Reservas

## Estrcutura de los archivos

Sistema de Gestión de Reservas/
├── SOAP_service/
│   ├── app/
│   │   ├── service.py
│   │   ├── requirements.txt
│   ├── init-scripts/
│   │   ├── init_soap_db.sql
│   ├── Dockerfile
├── Rest-service/
│   ├── app/
│   │   ├── service.py
│   ├── init-scripts/
│   │   ├── init_rest_db.sql
│   ├── Dockerfile
├── Microservicio/
│   ├── app/
│   │   ├── service.py
│   ├── init-scripts/
│   │   ├── init_inventory_db.sql
│   ├── Dockerfile
├── docker-compose.yml

## Instrucciones de uso

1. Clonar el Repositorio en la ruta deseada

git clone https://github.com/Xavi122323/Sistema_Gestion_Reservas-.git

cd Sistema_Gestion_Reservas

2. Tener Docker y Docker Compose instalados en la máquina

3. Construir las imágenes Docker para cada servicio

docker-compose up

4. Conectarse a cada servicio

http://localhost:8080/?wsdl (Servicio SOAP)

http://localhost:5000/ (Servicio Rest)

http://localhost:5001/ (Microservicio)
