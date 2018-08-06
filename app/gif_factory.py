# Import everything needed to edit video clips
from moviepy.editor import *
from tempfile import gettempdir
from urllib.request import urlretrieve
import os
import uuid
from app import fileremover as FileRemover
import requests

class GifFactory(object):

    def __init__(self, file_remover):
        self.tempdir = gettempdir() + '/'
        self.file_remover = file_remover

    def create(self, text, gif,
               hor_align='center', ver_align='top',
               text_height=20, text_width=60):

        original_gif_file = self._download_gif(gif)
        clip = VideoFileClip(original_gif_file)
        # Generate a text clip. You can customize the font, color, etc.
        txt_size = [clip.size[0]*text_width/100, clip.size[1]*text_height/100]
        txt_clip = TextClip(text, color='white', size=txt_size, method="caption", font="Helvetica", stroke_color='black', stroke_width=1)

        txt_clip = txt_clip.set_position((hor_align, ver_align)).set_duration(clip.duration)

        # Overlay the text clip on the first video clip
        video = CompositeVideoClip([clip, txt_clip])

        os.remove(original_gif_file)

        # Write the result to a file
        filename = self.tempdir + str(uuid.uuid4()) + '.gif'
        video.write_gif(filename)
        return filename
    
    def enqueueCaptionTask(self, data, upload_url):
        # create the captioned gif
        gif_file = self.create(**data)

        # upload it to file.io for temp storage (2 weeks)
        files = {'file': open(gif_file, 'rb')}
        res = requests.post(upload_url, files=files)
        
        # uploaded_url = res.json()['link']
        # print('response from server: {} === uploaded_url === {} === '.format(res.text, uploaded_url))

        # resp = send_file(gif_file, mimetype='image/gif')
        # delete the file after it's sent
        # http://stackoverflow.com/questions/13344538/how-to-clean-up-temporary-file-used-with-send-file
        self.file_remover.cleanup_once_done(res, gif_file)
        return res.json()

    def _download_gif(self, url):
        filename = self.tempdir + str(uuid.uuid4()) + '.gif'
        urlretrieve(url, filename)
        # TODO should confirm this is a gif image...
        return filename
