FROM nginx:1.25-bookworm

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/casei.nginx.conf /etc/nginx/sites-available/casei.nginx.conf

RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/casei.nginx.conf /etc/nginx/sites-enabled

#CMD ["nginx", "-g", "daemon off;"]