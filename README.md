# Grafana Manage Users


This is a simple app to automate creating users in grafana from a config file.

## Building and running

### Docker

```
docker run -d -v config.yml:/src/config.yml oba11/grafana-manage-users

OR

docker run -d -v config.yml:/config/config.yml -e CONFIG_PATH=/config/config.yml oba11/grafana-manage-users
```

## Configuration

Environment variables `GRAFANA_ADMIN_USERNAME` and `GRAFANA_ADMIN_PASSWORD` must be set.

The configuration is in YAML, with an [example here](./example.yml)

## To do

* Update user role
* Delete users
