import sys
import cookielib
import mechanize
import json
from colorme import ColorMe


class SoundCloudDL(object):
    """
    Convert and download SoundCloud links to Mp3's right on your dekstop.

    Attributes:
        song_link: link extension that is input from the user at command line
    """
    def __init__(self, song_link):
        self.song_link = song_link

        self.br = mechanize.Browser()
        self.sc_site = 'https://soundcloud.com/'
        self.stream_site = 'http://anything2mp3.com/'
        self.url = self.sc_site + song_link
        self.cookiejar = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cookiejar)

        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
        self.br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]


    def page_load(self, _url):
        print 'Verifying url...'+_url
        try:
            self.br.open(_url)
        except mechanize.HTTPError as e:
            ColorMe.color_text(str(e.code) + ': ' + e.reason +
                               '. Exiting program.', 'fail')
            sys.exit()


    def fetch_data(self):
        global track_id
        resolve_api = 'http://api.soundcloud.com/resolve?url='+self.url +\
        '&client_id='+'1179300263838e79a8710078c41555e6'
        print 'Grabbing track information....'
        self.br.open(resolve_api)

        resp = self.br.response()
        j = json.loads(resp.read())
        for k,v in j.iteritems():
            if k == 'id':
                track_id = str(v)

        stream_api = 'http://api.soundcloud.com/tracks/'+track_id+'/stream?client_id=1179300263838e79a8710078c41555e6'

        self.page_load(stream_api)
        ColorMe.color_text('Successfully loaded mp3...', 'ok')

    def download(self):
        with open('test.mp3', 'wb') as f:
            f.write(self.br.response().read())
            print 'read'
        ColorMe.color_text('Download complete.', 'ok')

    def run(self):

        self.page_load(self.url)
        ColorMe.color_text('Url verification successful.', 'ok')

        self.fetch_data()

        self.download()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        ColorMe.color_text('Insufficient arguments. Refer to ReadMe.', 'fail')
    else:
        sc = SoundCloudDL(sys.argv[1])
        sc.run()
