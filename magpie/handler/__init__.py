from index import IndexHandler
from config import ConfigHandler
from login import LoginHandler
from note import NoteHandler
from notebook import NotebookHandler
from search import SearchHandler

urls = []
urls.append((r'/magpie/?', IndexHandler))
urls.append((r'/magpie/config/?', ConfigHandler))
urls.append((r'/magpie/login/?', LoginHandler))
urls.append((r'/magpie/search/?', SearchHandler))

# do regex ones last so the others get routed properly
urls.append((r'/magpie/(.+)/(.+)', NoteHandler))
urls.append((r'/magpie/(.+)/?', NotebookHandler))
