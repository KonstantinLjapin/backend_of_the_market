#!/bin/bash
# need chmod +

# Загружаем переменные из .env
if [ -f .env ]; then
    while IFS='=' read -r key value; do
        if [[ ! $key =~ ^# && -n $key ]]; then
            value="${value%\"}"
            value="${value#\"}"
            export "$key"="$value"
        fi
    done < .env
fi

# Проверяем режим полного сброса
HARD_RESET=${HARD_DEV_RESET:-FALSE}
HARD_RESET=$(echo "$HARD_RESET" | tr '[:lower:]' '[:upper:]')

# Создаем только необходимую для данных БД директорию
mkdir -p dump/postgres

# Генерируем SECRET_KEY (если его еще нет)
if ! grep -q "SECRET_KEY=" .env; then
    echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
fi

# Обновляем requirements.txt
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate;
    pip freeze > requirements.txt;
    deactivate;
fi

# Создаем сеть и запускаем контейнеры
sudo docker network create -d bridge market_backend 2>/dev/null || true
sudo docker compose up;

# Очистка после завершения
sudo docker stop $(sudo docker ps -a -q) 2>/dev/null || true;
sudo docker rm $(sudo docker ps -a -q) 2>/dev/null || true;
sudo docker rmi $(sudo docker images --format="{{.Repository}} {{.ID}}" | \
                  grep "^backmarket" | cut -d' ' -f2) 2>/dev/null || true;
sudo docker network rm "market_backend" 2>/dev/null || true;

# Удаление в зависимости от режима
if [ "$HARD_RESET" = "TRUE" ]; then
    echo "HARD RESET: Удаление всех данных и миграций"
    # Удаляем данные
    sudo rm -rf dump/ alembic/version
else
    echo "SOFT RESET: Сохранение миграций"
    # Удаляем только данные БД
    sudo rm -rf dump/postgres/* 2>/dev/null
fi

# Удаляем requirements.txt
sudo rm -f requirements.txt 2>/dev/null

# Удаляем SECRET_KEY из .env
if [ -f .env ]; then
    sed -i '/^SECRET_KEY=/d' .env
fi