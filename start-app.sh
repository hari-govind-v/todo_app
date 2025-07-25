
set -e

echo "Building containers..."
docker compose build

echo "Running migrations..."
docker compose run --rm migration

echo "Seeding database..."
docker compose run --rm seed

echo "Starting app (web + nginx)..."
docker compose up web nginx
