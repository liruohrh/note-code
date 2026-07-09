
# MySQL

```bash
docker run -d \
  --name mysql \
  --restart unless-stopped \
  -e MYSQL_ROOT_PASSWORD=root \
  -p 3306:3306 \
  -v mysqldata:/var/lib/mysql \
  mysql:9.6.0
```