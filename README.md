# Grafana Users Manager


This is a simple app to automate creating users in grafana from a config file.

## Building and running

### Docker

```
docker run -d -v config.yml:/src/config.yml oba11/grafana-users-manager

OR

docker run -d -v config.yml:/config/config.yml -e CONFIG_PATH=/config/config.yml oba11/grafana-users-manager
```

## Configuration

Environment variables `GRAFANA_ADMIN_USERNAME` and `GRAFANA_ADMIN_PASSWORD` must be set.

The configuration is in YAML, with an [example here](./example.yml) with `grafana_root_url` default to `http://localhost:3000` if not specified in the configuration file.

```
grafana_root_url: http://localhost:3000
users:
- username: user1
  password: pass1
- username: user2
  password: pass
```

## To do

* Update user role
* Delete users
