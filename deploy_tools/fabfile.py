from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/pavkozlov/TDD_todo_list.git'


def deploy():
    '''развернуть'''
    site_folder = f'/home/{env.user}/sites/todo.itpavel.ru'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    '''создать структуру каталога, если нужно'''
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    '''получить самый свежий исходный код'''
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    '''обновить настройки'''
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    '''обновить виртуальную среду'''
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + 'bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip3 install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    '''обновить статические файлы'''
    run(f'cd {source_folder} && ../virtualenv/bin/python3 manage.py collectstatic --noinput')


def _update_database(source_folder):
    '''обновить базу данных'''
    run(
        f'cd {source_folder} && ../virtualenv/bin/python3 manage.py migrate --noinput'
    )


# sudo
# ln - s.. / sites - available / todo.itpavel.ru / etc / nginx / sites - enabled / todo.itpavel.ru
#
# sed
# "s/SITENAME/todo.itpavel.ru/g"
# source / deploy_tools / nginx.template.conf | sudo
# tee / etc / nginx / sites - available / todo.itpavel.ru
#
# sed
# "s/SITENAME/todo.itpavel.ru/g"
# source / deploy_tools / gunicorn - systemd.template.service | sudo
# tee / etc / systemd / system / gunicorn - todo.itpavel.ru.service
