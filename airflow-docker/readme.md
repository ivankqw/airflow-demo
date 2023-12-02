## Airflow with Docker 

### Prerequisites
- Docker Desktop that supports Docker Compose

Note: Allocate at least 4GB of memory (preferably 8GB) for Docker to run compose smoothly​

### Installation Steps
1. Fetch the Docker Compose YAML
Use the following command to download the docker-compose.yaml file:

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml'
```
This YAML file defines the necessary services for running Airflow, including airflow-scheduler, airflow-webserver, airflow-worker, airflow-triggerer, airflow-init, postgres, redis, and optionally flower for monitoring​​.

2. Initialize the Environment
Create necessary directories and set the right Airflow user:


```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

For non-Linux systems, manually create an .env file with AIRFLOW_UID=50000 in the same folder as docker-compose.yaml​​.
Initialize the database and create the first user account (username and password will be 'airflow'):

```
docker compose up airflow-init
```
3. Running Airflow
Start all services with the following command:
```
docker compose up
```
Check the condition of the containers using:
```
docker ps
```
Ensure no containers are in an unhealthy state​​.

Interacting with Airflow
CLI Commands: Run commands within the airflow-* services, e.g., `docker compose run airflow-worker airflow info. For ease of use`, you can download optional wrapper scripts:

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.3/airflow.sh'
chmod +x airflow.sh
./airflow.sh info
```

Web Interface: Access Airflow's web interface at http://localhost:8080. The default login is airflow with the password airflow.

REST API: Use basic username-password authentication for API requests. Example using curl:

```
ENDPOINT_URL="http://localhost:8080/"
curl -X GET --user "airflow:airflow" "${ENDPOINT_URL}/api/v1/pools"
```