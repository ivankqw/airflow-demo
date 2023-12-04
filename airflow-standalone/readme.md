## Airflow Standalone

### Prerequisites
- Python 3.8 or higher
- pip 

**Note: It is recommended to use a virtual environment to install Airflow**

Using venv (Pre-installed with Python)
```
cd ~/path/to/your/project
python3 -m venv airflow-env
source airflow-env/bin/activate
```

Using conda (You may need to install conda first)
```
conda create --name airflow-env python=3.8
conda activate airflow-env
```

### Installation Steps

1. Set Airflow Home:
Airflow requires a home directory, and uses ~/airflow by default, but you can set a different location if you prefer. The AIRFLOW_HOME environment variable is used to inform Airflow of the desired location. This step of setting the environment variable should be done before installing Airflow so that the installation process knows where to store the necessary files.

```
export AIRFLOW_HOME=~/airflow
```

Do a quick check to see if the variable is set correctly:

```
echo $AIRFLOW_HOME
```

2. Install Airflow:
```
AIRFLOW_VERSION=2.7.3

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.7.3 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.8.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

3. Run Airflow Standalone 

This initializes the database, creates a user, and starts all components:

```
airflow standalone
```

4. Create a DAGs folder (assuming you're in the home directory and you've set AIRFLOW_HOME to ~/airflow)
```
mkdir ~/airflow/dags
```