import requests
import json
import yaml, os
import time
import logging, sys
from urllib.parse import urljoin

# Logging config
loglevel = logging.INFO
if os.getenv('DEBUG', 'false').lower() == 'true':
  loglevel = logging.DEBUG
log = logging.getLogger(__name__)
log.setLevel(loglevel)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(loglevel)
formatter = logging.Formatter('%(asctime)s - %(levelname)s == %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}


def test_login(url, username, password):
  _url = urljoin(url, '/api/org')
  r = requests.get(_url, auth=(username, password))
  if 200 <= r.status_code <= 204:
    return True
  else:
    return False


def create_user(session, url, username, password):
  _url = urljoin(url, '/api/admin/users')
  data = {
    'name': username.title(),
    'email': username,
    'login': username,
    'password': password
  }
  r = session.post(_url, data=json.dumps(data))
  if 200 <= r.status_code <= 204:
    out = r.json()
    log.info(out['message'])
    result = update_user_role(
      session=session, url=url, user_id=out['id'], role='Viewer')
    return result
  else:
    log.error('Failed to create login for user: {}'.format(username))
    print(r.text)
    return False


def update_user_role(session, url, user_id, role='Viewer'):
  _url = urljoin(url, '/api/org/users/{}'.format(user_id))
  data = {'role': role}
  r = session.patch(_url, data=json.dumps(data))
  if 200 <= r.status_code <= 204:
    log.info(r.json()['message'])
    return True
  else:
    log.error('Failed to update permission for {}'.format(user_id))
    return False


def update_user_password(session, url, user_id, password):
  _url = urljoin(url, '/api/admin/users/{}/password'.format(user_id))
  data = {'password': password}
  r = session.put(_url, data=json.dumps(data))
  if 200 <= r.status_code <= 204:
    log.info(r.json()['message'])
    return True
  else:
    log.error('Failed to update password for user id: {}'.format(user_id))
    return False


def get_users(session, url, username, password):
  _url = urljoin(url, '/api/users')
  r = session.get(_url)
  if 200 <= r.status_code <= 204:
    out = [x for x in r.json() if x['login'] == username]
    if out:
      out = out[0]
      log.info('Checking if the password should be reset for user: {}'.format(
        username))
      result = test_login(url=url, username=username, password=password)
      if result:
        log.info('Login successful for user: {}'.format(username))
        return result
      else:
        log.info('Resetting password for user: {}'.format(username))
        result = update_user_password(
          session=session, url=url, user_id=out['id'], password=password)
        return result
    else:
      log.info('Creating user: {}...'.format(username))
      result = create_user(
        session=session, url=url, username=username, password=password)
      log.info('successfully created user: {}'.format(username))
      return True
  else:
    log.error('Failed to connect retrieve user details, message: {}'.format(
      r.json()['message']))
    return False


def read_config():
  log.info('Reading config file...')
  configfile = os.path.join(os.path.dirname(__file__), 'config.yml')
  if os.getenv('CONFIG_PATH'):
    configfile = os.getenv('CONFIG_PATH')
    log.info(os.path.exists(configfile))
    log.debug(configfile)
  if not (os.path.exists(configfile) and os.stat(configfile).st_size > 0):
    log.error('cannot read config file: {}'.format(configfile))
    return None
  return yaml.safe_load(open(configfile))


def main():
  log.info('Worker Running')

  admin_username = os.getenv('GRAFANA_ADMIN_USERNAME')
  admin_password = os.getenv('GRAFANA_ADMIN_PASSWORD')

  while True:
    config = read_config()
    if config is not None:
      session = requests.Session()
      session.auth = (admin_username, admin_password)
      session.headers = headers
      for user in config['users']:
        get_users(
          session=session,
          url=config.get('grafana_root_url','http://localhost:3000'),
          username=user['username'],
          password=user['password'])
    time.sleep(60)


if __name__ == '__main__':
  main()
