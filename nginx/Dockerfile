FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/logs
RUN touch /etc/nginx/logs/nginx-access.log

RUN mkdir -p /etc/nginx/logs
RUN touch /etc/nginx/logs/nginx-error.log

COPY nginx.conf /etc/nginx/conf.d
COPY certificate.crt /etc/nginx/ssl/certificate.crt
COPY private.key /etc/nginx/ssl/private.key