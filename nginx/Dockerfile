FROM nginx:1.27-alpine

RUN apk add --no-cache openssl

COPY conf.d/pcfinder.conf /etc/nginx/conf.d/default.conf
COPY scripts/start-nginx.sh /start-nginx.sh
RUN chmod +x /start-nginx.sh

CMD ["/start-nginx.sh"]
