import subprocess as sp


class Main:
    def __init__(self, directory):
        self.directory = directory
        result = self.execute_wwwdata('git pull')
        if result[0] != u'Bereits aktuell.':
            self.execute_venv('pip install -r requirements.txt')
            self.execute_venv('manage.py collectstatic --noinput')
            self.execute_venv('manage.py compilemessages')
            self.execute_venv('manage.py migrate')
            self.execute('systemctl restart nomoney.shop')

    def execute_venv(self, cmd):
        """ execute in the context of the virtualenv
        full command: su www-data -c "venv/bin/python {}"
        :param cmd: command to insert
        :returns: execution result
        """
        return self.execute_wwwdata('venv/bin/python {}'.format(cmd))

    def execute_wwwdata(self, cmd):
        """ execute as www-data user
        full command: su www-data -c "{}"
        :param cmd: command to insert
        :returns: execution result
        """
        return self.execute('su www-data -c "{}"'.format(cmd))

    def execute(self, cmd):
        """ execute
        :param cmd: command to insert
        :returns: execution result
        """
        o, _ = sp.Popen(  # o = output, e = error
            cmd,
            shell=True,
            stdout=sp.PIPE,
            stderr=sp.STDOUT,
            cwd=self.directory
        ).communicate()
        return o.decode("utf-8").splitlines()


if __name__ == '__main__':
    main = Main('/var/www/nomoney.shop')
