from os.path import join

import bcrypt
from tornado.web import authenticated

from base import BaseHandler

class ConfigHandler(BaseHandler):
    ALLOWED = {'testing': bool, 'port': int, 'pwdhash': str, 'repo': str,
               'username': str, 'autosave': bool, 'address': str, 'theme': str}
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
            elif val is None or val == '':
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
        for key, val in new.items():
            if self.ALLOWED[key] == str:
                config_file.write("%s='%s'\n" % (key, val))
            else:
                config_file.write("%s=%s\n" % (key, val))
        config_file.close()
        self.redirect('/')

    def _fetch_existing_config(self):
        existing = dict()
        for config in open(self.settings.config_path.web).readlines():
            key, val = config.strip().replace(' = ', '=').split('=')
            existing[key] = val.replace("'", "")
        return existing
