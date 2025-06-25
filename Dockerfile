# Use the official Apache Airflow image as the base
FROM apache/airflow:2.9.1-python3.9

# Switch to root to install system packages
USER root

# Install any OS-level dependencies (adjust as needed)
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy your DAGs and custom scripts into the image
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

# Ensure script is executable
RUN chmod +x /opt/airflow/scripts/run_github_action.sh

