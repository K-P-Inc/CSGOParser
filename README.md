# Инструкция по запуску локально

## Выбор нужных маркетов

Для выбора нужных маркетов, используйте файл `prepare-build-config.yml`.

## Настройка Docker Compose

В файле `docker-compose.global_worker.build.yml.j2` убедитесь, что включена маскировка IP:

``` yaml
com.docker.network.bridge.enable_ip_masquerade:  "true"
```

## Применение изменений в воркерах

После внесения изменений в конфигурацию воркеров, выполните следующую команду:

``` bash
BUILD_TYPE=global_worker WEAPON_TYPES=AK-47  ansible-playbook  prepare-build-config.yml
```

## Запуск Docker Compose

Для запуска Docker Compose с пересборкой, выполните следующую команду:

``` bash
docker-compose  up  -d  --build
```

## Запуск фронта

Перейдите в директорию фронта:

``` bash
cd  app
```

Обновите npm пакеты:

``` bash
npm  i
```

Запустите фронт:

``` bash
npm  run  dev
```
