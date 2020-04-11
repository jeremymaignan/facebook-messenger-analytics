cd /var/app/etl/src/ && python3.7  utils/test_db_connection.py
cd /var/app/etl/src/ && time python3.7 etl.py && echo "[INFO] Messages loaded" || echo "[ERROR] Fail to load messages"
