Follow these steps to run Binance app:

# Start your application with Docker Compose command
docker-compose -f docker-compose.yml -f docker-compose-postgres.yml up -d

# Run Alembic upgrade to head to apply migrations
alembic upgrade head

# Start the Uvicorn server
uvicorn main:app

# Execute "/bitcoin/run" endpoint to run background tasks. Make sure it appears in Postgresql database

# Execute "/bitcoin/{coin_name}" endpoint with 'BTC' or 'ETH' values to visualize heatmap


Prepared by Kapparova Aknur



