# File: dags/dynamic_job_runner.py
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models.param import Param
import json, os
from typing import List
import subprocess
import pandas as pd

@dag(
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    params={
        "lot_wafer_list": Param([], type="array"),
        "batch_size": Param(10, type="integer"),
        "form_data_path": Param("/mnt/input/request.json", type="string"),
        "shared_drive_path": Param("/mnt/output/final.csv", type="string")
    },
    tags=["dynamic", "split-job"]
)
def dynamic_batch_job():

    @task()
    def split_batches(lot_wafer_list: List[str], batch_size: int) -> List[List[str]]:
        return [lot_wafer_list[i:i + batch_size] for i in range(0, len(lot_wafer_list), batch_size)]

    @task()
    def run_batch(batch: List[str], form_data_path: str, index: int) -> str:
        batch_input = ",".join(batch)
        output_csv = f"/tmp/output_{index}.csv"
        subprocess.run([
            "/bin/bash", "/opt/airflow/scripts/run_github_action.sh",
            batch_input, form_data_path, output_csv
        ], check=True)
        return output_csv

    @task()
    def merge_csvs(output_paths: List[str], shared_drive_path: str):
        df_all = pd.concat([pd.read_csv(p) for p in output_paths], ignore_index=True)
        df_all.to_csv(shared_drive_path, index=False)

    # DAG execution flow
    batches = split_batches(
        lot_wafer_list='{{ params.lot_wafer_list }}',
        batch_size='{{ params.batch_size }}'
    )
    output_files = run_batch.expand(
        batch=batches,
        form_data_path='{{ params.form_data_path }}',
        index=list(range(100))  # upper bound safeguard
    )
    merge_csvs(output_files, shared_drive_path='{{ params.shared_drive_path }}')


dynamic_batch_job()

