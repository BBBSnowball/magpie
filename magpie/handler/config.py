from os.path import join

import bcrypt
from tornado.web import authenticated
from tornado.util import exec_in

from base import BaseHandler

class ConfigHandler(BaseHandler):
    ALLOWED = {'testing': bool, 'port': int, 'pwdhash': str, 'repo': str,
               'username': str, 'autosave': bool, 'autosave_interval': int,
               'address': str, 'wysiwyg' : bool, 'theme': str, 'prefix': str}
    @authenticated
    def get(self):
        themes = {
          'Amelia':    '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/amelia/bootstrap.min.css',
          'Cerulean':  '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/cerulean/bootstrap.min.css',
          'Cosmo':     '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/cosmo/bootstrap.min.css',
          'Cyborg':    '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/cyborg/bootstrap.min.css',
          'Darkly':    '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/darkly/bootstrap.min.css',
          'Flatly':    '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/flatly/bootstrap.min.css',
          'Journal':   '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/journal/bootstrap.min.css',
          'Lumen':     '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/lumen/bootstrap.min.css',
          'Readable':  '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/readable/bootstrap.min.css',
          'Simplex':   '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/simplex/bootstrap.min.css',
          'Slate':     '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/slate/bootstrap.min.css',
          'Spacelab':  '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/spacelab/bootstrap.min.css',
          'Superhero': '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/superhero/bootstrap.min.css',
          'United':    '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/united/bootstrap.min.css',
          'Yeti':      '//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/yeti/bootstrap.min.css'
        }
        self.render('config.html', config=self._fetch_existing_config(), themes=themes)

    @authenticated
    def post(self):
        old = self._fetch_existing_config()
        new = dict()
        for key in self.ALLOWED.keys():
            if self.ALLOWED[key] == bool:
                val = self.get_argument(key, False)
            else:
                val = self.get_argument(key, None)
            if key == 'theme' and val is not None:
                new[key] = str(val)
            elif (val is None or val == '') and key in old:
                new[key] = old[key]
            elif key == 'pwdhash':
                new[key] = bcrypt.hashpw(val, bcrypt.gensalt())
            elif self.ALLOWED[key] == str:
                new[key] = str(val)
            elif self.ALLOWED[key] == int:
                new[key] = int(val)
            elif self.ALLOWED[key] == bool:
                new[key] = bool(val)
        config_file = open(self.settings.config_path.web, 'w')
        for key, val in sorted(new.items()):
            config_file.write("%s=%r\n" % (key, val))
        config_file.close()
        self.redirect(self.settings.prefix)

    def _fetch_existing_config(self):
        # We could use tornado.options.OptionParser, but we would have to
        # define the options before reading the file. Instead, we use code
        # that is similar to that in tornado.
        path = self.settings.config_path.web
        #NOTE This code is copied from tornado. Therefore, the license of
        #     tornado applies (Apache License 2.0).
        config = {}
        with open(path) as f:
            exec_in(f.read(), config, config)
        return config
