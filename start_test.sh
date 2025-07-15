#!/bin/bash

set -e

if ! grep -q "^SECRET_KEY=" .env; then
  echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
  echo "✔ SECRET_KEY добавлен в .env"
else
  echo "✔ SECRET_KEY уже есть"
fi


if ! docker network inspect market_backend >/dev/null 2>&1; then
  echo "Создание сети market_backend..."
  docker network create -d bridge market_backend
fi


echo "🚀 Запуск docker-compose..."
docker-compose up --build


echo "Остановка контейнеров..."
docker stop $(docker ps -aq) || true
docker rm $(docker ps -aq) || true

# 5. Удаление образов с именем backend
echo "🧹 Удаление образов backend..."
docker rmi $(docker images --format "{{.Repository}} {{.ID}}" | grep "^backend" | cut -d' ' -f2) || true


docker network rm market_backend || true


echo "Очистка папки dump/"
rm -rf dump/


echo "🧽 Удаление SECRET_KEY из .env"
sed -i '' '/^SECRET_KEY=/d' .env 2>/dev/null || sed -i '/^SECRET_KEY=/d' .env

echo "✅ Готово!"
