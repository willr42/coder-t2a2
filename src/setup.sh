#!/bin/bash
set -eo pipefail # Fail on error
RED='\033[0;31m' # Color variables
NC='\033[0m'

# Function to suppress pushd/popd output
silent(){
	"$@" > /dev/null 2>&1
}

# move to temporary directory, otherwise we get error output when we switch to postgres user
silent pushd /tmp || echo "Something went wrong changing to the temporary dir"

# Check for postgres
if ! [ -x "$(command -v psql)" ]; then
	echo -e "${RED}ERROR: This project requires Postgresql to be installed."
	echo -e "Please consult https://www.postgresql.org/ for instructions.${NC}"
	exit 1
fi
echo "Creating database and user..."
sudo su postgres -c "psql -U postgres -tc \"SELECT 1 FROM pg_user WHERE usename = 'plantadmin'\" | grep -q 1 || psql -U postgres -c \"CREATE USER plantadmin\""
sudo su postgres -c "echo \"SELECT 'CREATE DATABASE plantapi' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'plantapi')\gexec\" | psql"
echo "User and database created successfully."
silent popd

echo "Generating .env file..."
cat << EOF > .env
DATABASE_URL="postgresql+psycopg2://plantadmin:plants@${HOSTNAME}/plantapi"
SECRET_KEY="example_secret_key"
EOF
