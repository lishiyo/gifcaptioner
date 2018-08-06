"""
app.fileremover
~~~~~~~~~~~~~~
"""

from os import remove
import tempfile
import weakref

class FileRemover(object):
    def __init__(self):
        self.weak_references = dict()  # weak_ref -> filepath to remove

    def cleanup_once_done(self, response, filepath):
        wr = weakref.ref(response, self._do_cleanup)
        self.weak_references[wr] = filepath

    def _do_cleanup(self, wr):
        filepath = self.weak_references[wr]
        print('Deleting %s' % filepath)
        remove(filepath)

    def remove_file(self, filepath):
      print('Deleting %s' % filepath)
      remove(filepath)
