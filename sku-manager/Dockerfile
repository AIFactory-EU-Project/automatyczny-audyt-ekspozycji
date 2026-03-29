FROM php:7.4-apache

RUN apt-get update --fix-missing
RUN apt-get install -y curl build-essential libssl-dev libzip-dev zlib1g-dev libpq-dev

RUN docker-php-ext-install zip
RUN docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql
RUN docker-php-ext-install pdo pdo_pgsql pgsql

ENV APACHE_DOCUMENT_ROOT /var/www/html/public
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

RUN a2enmod rewrite headers

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html/

COPY composer.json composer.lock ./

RUN composer install --prefer-dist --dry-run

COPY . ./

RUN composer install --prefer-dist --optimize-autoloader

RUN chmod -R 777 ./var