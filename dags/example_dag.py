# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime

from airflow import models
from airflow.operators import bash
from airflow.models.variable import Variable
from google.cloud import secretmanager

# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    "owner": "Composer Example",
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "start_date": YESTERDAY,
}

def get_secret_value(secret_name, project_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_version = client.access_secret_version(name=f"projects/{project_id}/secrets/{secret_name}/versions/latest")
    return secret_version.payload.data.decode("UTF-8")


with models.DAG(
        "composer_sample_dag",
        "catchup=False",
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1),
) as dag:
    # Print the dag_run id from the Airflow logs
    #secret = Variable.get('example-secret')

    secret_name = "example-secret"
    project_id = "qwiklabs-gcp-03-d8830502f2ec"

    secret_value = get_secret_value(secret_name, project_id)


    print_dag_run_conf = bash.BashOperator(
        task_id="print_dag_run_conf", bash_command="echo secret:" + secret_value
    )