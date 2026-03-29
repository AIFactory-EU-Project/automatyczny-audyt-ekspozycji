# SKU Manager Service API

## Usage

Api can be viewed and tested at: `/api/doc`


## Development environment setup in PHPStorm

### PHP file template

```
<?php
/**
* @license AiFactory
*/
declare(strict_types=1);
```

### Quality tools

`Settings -> Languages & Frameworks -> PHP -> Quality tools`

#### Code sniffer

`Configuration: Local`

`Code sniffer path: [PROJECT_ABSOLUTE_PATH]/vendor/bin/phpcs`

#### PHP CS Fixer

`Configuration: Local`

`PHP CS Fixer path: [PROJECT_ABSOLUTE_PATH]/vendor/bin/php-cs-fixer`

#### Inspections

`Settings -> Editor -> Inspections`

`PHP -> Quality tools`

##### PHP Code Sniffer validation:

`Installed standard paths: [PROJECT_ABSOLUTE_PATH]/vendor/escapestudios/symfony2-coding-standard`

`Coding standard: Custom` -> `Path to ruleset: [PROJECT_ABSOLUTE_PATH]/phpcs.xml.dist`


##### PHP CS Fixer validation:

`Ruleset: Custom` -> `Path to ruleset: [PROJECT_ABSOLUTE_PATH]/.php_cs.dist`


#### File watcher
`Settings -> Tools -> File Watchers`

```
Name: PHP CS Fixer
File type: PHP
Scope: Current File

Program: $ProjectFileDir$/vendor/friendsofphp/php-cs-fixer/php-cs-fixer
Arguments fix --rules=@Symfony,-no_superfluous_phpdoc_tags
Output paths to refresh: $ProjectFileDir$
Working Directory: $ProjectFileDir$
```

### Sample development docker compose

```
version: '3.4'

services:
  sku-manager-php-apache:
    environment:
      - PORT=8001
      - MAIL_SENDER_ADDRESS=sender.address@example.com
      - APP_ENV=dev
      - SYSTEM_NAME=System name
      - FRONTEND_URL_PASSWORD_RESET=localhost/password/reset/
      - CORS_ALLOW_ORIGIN=^https?://localhost(:[0-9]+)?$$
      - JWT_SECRET_KEY=LOCAL_DEVELOPMENT_JWT_SECRET_KEY_PLACEHOLDER
      - JWT_PUBLIC_KEY=LOCAL_DEVELOPMENT_JWT_PUBLIC_KEY_PLACEHOLDER
      - JWT_PASSPHRASE=LOCAL_DEVELOPMENT_JWT_PASSPHRASE_PLACEHOLDER
      - DATABASE_URL=LOCAL_DEVELOPMENT_JDATABASE_URL_PLACEHOLDER
      - MAILER_DSN=LOCAL_DEVELOPMENT_MAILER_DSN
    network_mode: host
    build:
      context: ./
      dockerfile: ./Dockerfile
    image: sku-web-editor-php-apache
    volumes:
      - ./config:/var/www/html/config
      - ./public:/var/www/html/public
      - ./src:/var/www/html/src
      - ./templates:/var/www/html/templates
      - ./tests:/var/www/html/tests
      - ./db:/var/www/html/db
```
