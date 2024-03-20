## Running Airflow in Docker

### Before you begin

1. Install Docker Community Edition (CE) on your workstation
2. Install Docker Compose v2.14.0 or newer on your workstation.


### Fetching `docker-compose.yaml`

To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.

```shell
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.3/docker-compose.yaml'
```

This file contains several service definitions:

* `airflow-scheduler` - The scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
* `airflow-webserver` - The webserver is available at http://localhost:8080.
* `airflow-worker` - The worker that executes the tasks given by the scheduler.
* `airflow-triggerer` - The triggerer runs an event loop for deferrable tasks.
* `airflow-init` - The initialization service.
* `postgres` - The database.
* `redis` - The redis - broker that forwards messages from scheduler to worker.


Optionally, you can enable flower by adding `--profile flower` option, e.g. `docker compose --profile flower up`, or by explicitly specifying it on the command line e.g. `docker compose up flower`.

* flower - The flower app for monitoring the environment. It is available at http://localhost:5555.

All these services allow you to run Airflow with CeleryExecutor. For more information, see Architecture Overview.

Some directories in the container are mounted, which means that their contents are synchronized between your computer and the container.

* `./dags` - you can put your DAG files here.
* `./logs` - contains logs from task execution and scheduler.
* `./config` - you can add custom log parser or add airflow_local_settings.py to configure cluster policy.
* `./plugins` - you can put your custom plugins here.

This file uses the latest Airflow image (apache/airflow). If you need to install a new Python library or system library, you can build your image.


### Initializing Environment

Before starting Airflow for the first time, you need to prepare your environment, i.e. create the necessary files, directories and initialize the database.

**Setting the right Airflow user**

On Linux, the quick-start needs to know your host user id and needs to have group id set to 0. Otherwise the files created in `dags`, `logs` and `plugins` will be created with root user ownership. You have to make sure to configure them for the docker-compose:

```shell
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

**Initialize the database**

On all operating systems, you need to run database migrations and create the first user account. To do this, run.

```shell
docker compose up airflow-init
```

After initialization is complete, you should see a message like this:

```shell
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.8.3
start_airflow-init_1 exited with code 0
```

The account created has the login `airflow` and the password `airflow`.

### Running Airflow

Now you can start all services:

```shell
docker compose up
```

In a second terminal you can check the condition of the containers and make sure that no containers are in an unhealthy condition:

```shell
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                              NAMES
247ebe6cf87a   apache/airflow:2.8.3   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-worker_1
ed9b09fc84b1   apache/airflow:2.8.3   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-scheduler_1
7cb1fb603a98   apache/airflow:2.8.3   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    0.0.0.0:8080->8080/tcp             compose_airflow-webserver_1
74f3bbe506eb   postgres:13            "docker-entrypoint.s…"   18 minutes ago   Up 17 minutes (healthy)   5432/tcp                           compose_postgres_1
0bd6576d23cb   redis:latest           "docker-entrypoint.s…"   10 hours ago     Up 17 minutes (healthy)   0.0.0.0:6379->6379/tcp             compose_redis_1
```







**Crontab**
> https://crontab.guru/


**Docker**
```shell
docker build . --tag extending_airflow:latest 

docker compose up -d --no-deps --build airflow-webserver airflow-scheduler
```

