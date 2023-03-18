#!/bin/bash
set -eo pipefail # Fail on error
RED='\033[0;31m' # Color variables
NC='\033[0m'

# Function to suppress pushd/popd output
silent(){
	"$@" > /dev/null 2>&1
}

# move to directory of the script
cd -P -- "$(dirname -- "$0")"
cd ..

# Check for postgres
if ! [ -x "$(command -v psql)" ]; then
	echo -e "${RED}ERROR: This project requires Postgresql to be installed."
	echo -e "Please consult https://www.postgresql.org/ for instructions.${NC}"
	exit 1
fi

echo "Creating database and user..."
echo "Please enter your Postgres password."
psql -c "SELECT 1 FROM pg_user WHERE usename = 'plantadmin'" | grep -q 1 || psql -c "CREATE USER plantadmin WITH PASSWORD 'plants'"
echo "User created succesfully."
echo "SELECT 'CREATE DATABASE plantapi' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'plantapi')\gexec" | psql
psql -c "ALTER DATABASE plantapi OWNER TO plantadmin"
echo "User and database created successfully."

read -p "Postgres port (leave blank for default): " POSTGRES_PORT
echo "Generating .env file..."
cat << EOF > .env
DATABASE_URL="postgresql+psycopg2://plantadmin:plants@localhost:${POSTGRES_PORT:-5432}/plantapi"
SECRET_KEY="example_secret_key"
EOF

if ! [ -x "$(command -v python3)" ]; then
	echo -e "${RED}ERROR: This project requires Python3 to be installed."
	echo -e "Please consult https://www.python.org/ for instructions.${NC}"
	exit 1
fi

echo "Creating venv..."
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r ./requirements.txt
flask db drop
flask db create
flask db seed
flask run

