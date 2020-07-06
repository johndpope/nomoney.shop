import subprocess as sp
from time import sleep


def execute(cmd, directory):
    o, e = sp.Popen(# o = output, e = error
        cmd,
        shell=True,
        stdout=sp.PIPE,
        stderr=sp.STDOUT,
        cwd=directory
    ).communicate()
    return o.decode("utf-8").splitlines()


directory = '/var/www/nomoney.shop'
result = execute('su www-data -c "git pull"', directory)
print(result)
if result[0] != u'Bereits aktuell.':
    result = execute('su www-data -c "venv/bin/python manage.py collectstatic --noinput"', directory)
    print(result)
    result = execute('su www-data -c "venv/bin/python manage.py compilemessages"', directory)
    print(result)
    result = execute('/etc/init.d/apache2 reload', directory)
    print(result)
