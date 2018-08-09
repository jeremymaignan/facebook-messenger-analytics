until echo '\q' | mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" $MYSQL_DATABASE  > /dev/null 2>&1; do
    >&2 echo "MySQL is unavailable - sleeping"
    sleep 2
done
cd /var/app/etl/src/ && python3.7 etl.py
echo "[INFO] Messages loaded"