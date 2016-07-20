from index import IndexHandler
from config import ConfigHandler
from login import LoginHandler
from note import NoteHandler
from notebook import NotebookHandler
from search import SearchHandler

def get_urls(prefix):
	urls = []
	urls.append((prefix + r'?', IndexHandler))
	urls.append((prefix + r'config/?', ConfigHandler))
	urls.append((prefix + r'login/?', LoginHandler))
	urls.append((prefix + r'search/?', SearchHandler))

	# do regex ones last so the others get routed properly
	urls.append((prefix + r'(.+)/(.+)', NoteHandler))
	urls.append((prefix + r'(.+)/?', NotebookHandler))

	return urls
