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
import os

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

# Check if the environment variable TESTING is set
testing_mode = os.environ.get("TESTING", "false").lower() == "true"


with models.DAG(
        "composer_sample_dag",
        "catchup=False",
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1),
) as dag:
    # Print the dag_run id from the Airflow logs

    if testing_mode:
        # Set a mocked secret variable for testing
        mocked_secret = "mocked_secret_val"
    else:
        # Retrieve the actual secret from Airflow Variable
        mocked_secret = Variable.get("example-secret")
    print_dag_run_conf = bash.BashOperator(
        task_id="print_dag_run_conf", bash_command="secret:" + mocked_secret
    )