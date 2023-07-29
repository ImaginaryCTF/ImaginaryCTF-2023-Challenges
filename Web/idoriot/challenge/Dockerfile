FROM php:apache-bookworm

# Set working directory
WORKDIR /var/www/html

# Copy files to the appropriate location
COPY *.php /var/www/html/

# Copy flag
COPY flag.txt /var/www/html/flag.txt
RUN chmod 444 /var/www/html/flag.txt

# open in-memory sqlite database and initialize schema
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev
RUN docker-php-ext-install pdo_sqlite

# Create rate-limit directory
RUN mkdir /var/www/html/rate-limit
RUN touch /var/www/html/rate-limit/reset
RUN chmod -R 777 /var/www/html/rate-limit

# Expose port 80
EXPOSE 80

VOLUME /var/www/html
VOLUME /var/log/apache2
VOLUME /var/run/apache2
VOLUME /tmp

# Start Apache
CMD ["apache2-foreground"]
