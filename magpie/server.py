#!/usr/bin/env python
from os import path
from random import choice
from string import letters, digits

from sh import git
from tornado import autoreload
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_config_file
from tornado.web import Application

from config import config_path
from handler import get_urls

class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, val):
        self[key] = val

def _rand_str(length=64):
    return ''.join([choice(letters + digits) for i in range(0, length)])

def make_app(config=None):
    root = path.dirname(__file__)
    static_path = path.join(root, 'static')
    template_path = path.join(root, 'template')

    app_config = dict(static_path=static_path,
                      template_path=template_path)

    define('port', default='8080', type=int)
    define('address', default='localhost', type=str)
    define('testing', default=False, type=bool)
    define('repo', default=None, type=str)
    define('username', default=None, type=str)
    define('pwdhash', default=None, type=str)
    define('autosave', default=False, type=bool)
    define('prefix', default='/', type=str)
    define('autosave_interval', default='5', type=int)
    define('wysiwyg', default=False, type=bool)
    define('theme', default=None, type=str)

    if config is not None:
        # This should only ever be used for testing
        parse_config_file(config)
    else:
        parse_config_file(config_path.web)

    if options.testing:
        app_config.update(debug=True)

    if not options.prefix.endswith('/'):
        options.prefix += '/'
    urls = get_urls(options.prefix)

    app_config.update(
      login_url=options.prefix + 'login',
      static_url_prefix=options.prefix + 'static/')

    server = Application(urls, **app_config)
    server.settings = AttrDict(server.settings)
    server.settings.repo = options.repo
    server.settings.username = options.username
    server.settings.pwdhash = options.pwdhash
    server.settings.session = _rand_str()
    server.settings.config_path = config_path
    server.settings.autosave = options.autosave
    server.settings.prefix = options.prefix
    server.settings.autosave_interval = options.autosave_interval
    server.settings.wysiwyg = options.wysiwyg
    server.settings.theme = options.theme

    server.git = git.bake(_cwd=server.settings.repo)

    return server

def main():
    server = make_app()
    server.listen(options.port, options.address)
    autoreload.start()
    autoreload.watch(config_path.web)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
