FROM apache/airflow:2.10.0
RUN pip install pandas
RUN pip install --upgrade redis celery kombu