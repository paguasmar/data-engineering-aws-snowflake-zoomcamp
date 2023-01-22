from sqlalchemy import create_engine
import pandas as pd
from time import time
import argparse
import os
import pyarrow.parquet as pq
"""
URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --url=${URL} \
    --table_nam=yellow_taxi
"""

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    url=params.url
    table_name=params.table_name
    parquet_name="in.parquet"

    os.system(f'wget {url} -O {parquet_name}')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    parquet_file = pq.ParquetFile(parquet_name)

    for batch in parquet_file.iter_batches():
        t_start = time()
        df = batch.to_pandas()
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()
        print('inserted another chunk, took %.3f second' % (t_end - t_start))

    print("Finished ingesting data into the postgres database")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest Parquet data to Postgres")
    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="db for postgres")
    parser.add_argument("--url", help="url of parquet file")
    parser.add_argument("--table_name", help="table name to write to in postgres")
    args = parser.parse_args()
    main(args)