# AWS EC2
    docker-server
         ├── docker-compose.yml
         ├── nginx
         │   ├── Dockerfile
         │   ├── nginx-app.conf
         │   └── nginx.conf
         └── subbly-docker
# docker-compose.yml
    version: '3'
    services:

        nginx:
            container_name: nginx
            build: ./nginx
            image: docker-server/nginx
            restart: always
            ports:
              - "80:80"
            volumes:
              - ./subbly-docker:/srv/docker-server
              - ./log:/var/log/nginx
            depends_on:
              - django

        django:
            container_name: django
            build: ./subbly-docker
            image: docker-server/django
            restart: always
            command: uwsgi --ini uwsgi.ini
            volumes:
              - ./subbly-docker:/srv/docker-server
              - ./log:/var/log/uwsgi
# Dockerfile
        FROM nginx:latest

        COPY nginx.conf /etc/nginx/nginx.conf
        COPY nginx-app.conf /etc/nginx/sites-available/

        RUN mkdir -p /etc/nginx/sites-enabled/\
            && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

        # EXPOSE 80
        CMD ["nginx", "-g", "daemon off;"]




        
        
