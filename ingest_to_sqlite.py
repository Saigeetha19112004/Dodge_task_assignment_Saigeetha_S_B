import os
import json
import sqlite3
import glob

DB_PATH = "order_to_cash.db"
DATA_DIR = r"d:\dodge ai_assignment\sap-order-to-cash-dataset\sap-o2c-data"

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def ingest_data():
    conn = create_connection()
    cursor = conn.cursor()

    for root, dirs, files in os.walk(DATA_DIR):
        for d in dirs:
            dir_path = os.path.join(root, d)
            jsonl_files = glob.glob(os.path.join(dir_path, '*.jsonl'))
            if not jsonl_files:
                continue
            
            # Read first file to get schema
            schema = []
            with open(jsonl_files[0], 'r', encoding='utf-8') as f:
                line = f.readline()
                if line:
                    schema = list(json.loads(line).keys())
            
            if not schema:
                continue

            # Create table
            columns = ", ".join([f"{col} TEXT" for col in schema])
            cursor.execute(f"DROP TABLE IF EXISTS {d}")
            try:
                cursor.execute(f"CREATE TABLE {d} ({columns})")
            except Exception as e:
                print(f"Failed to create table {d}: {e}")
                continue

            # Ingest data
            print(f"Ingesting into {d}...")
            insert_sql = f"INSERT INTO {d} ({','.join(schema)}) VALUES ({','.join(['?']*len(schema))})"
            
            for file_path in jsonl_files:
                batch = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            row = []
                            for c in schema:
                                val = data.get(c, None)
                                if isinstance(val, (dict, list)):
                                    val = json.dumps(val)
                                row.append(val)
                            batch.append(tuple(row))
                            if len(batch) >= 5000:
                                cursor.executemany(insert_sql, batch)
                                batch = []
                        except Exception as e:
                            pass
                if batch:
                    cursor.executemany(insert_sql, batch)

    conn.commit()
    conn.close()
    print("Data ingestion complete!")

if __name__ == "__main__":
    ingest_data()
