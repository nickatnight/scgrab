import cookielib
import json
import keys
import mechanize
import pbar
import sys
from colorme import ColorMe
from track import TrackInfo


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
        self.url = self.sc_site + song_link
        self.json_response = {}
        self.cookiejar = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cookiejar)

        # Don't handle HTTP-EQUIV headers
        self.br.set_handle_equiv(True)

        self.br.set_handle_redirect(True)
        # See original page request
        self.br.set_handle_referer(True)
        # Ignore robots.txt...
        self.br.set_handle_robots(False)
        # Allow 1 refresh redirect
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
        # Headers for browser
        self.br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]


    def page_load(self, _url):
        """
        Check the new GET request and verify the response is 200. Log error
        otherwise.

        _url: url of GET request
        """
        print 'Verifying url...'+_url
        try:
            self.br.open(_url)
        except mechanize.HTTPError as e:
            ColorMe.color_text(str(e.code) + ': ' + e.reason +
                               '. Exiting program.', 'fail')
            sys.exit()


    def parse_data(self, json_data):
        """
        Parse the JSON request from the soundcloud resolve api. Store the data
        in Track Info for pre depoloyment to mutagen.

        json_data: JSON response from sc api
        """

        # Object that stores track meta data
        ti = TrackInfo()

        # Iterate over json object for storage into *ti*
        for k,v in json_data.iteritems():
                if k == 'id':
                    ti._id = str(v)
                if k == 'user':
                    ti._artist = v['username']
                if k == 'title':
                    ti._title = v
                if k == 'release_year':
                    ti._year = v

        return ti

    def fetch_data(self):
        """
        Generate data from the SoundCloud api response. Must have teh client ID
        in order to authorize the request.
        """

        # Need to fix this
        global track_id
        tags = None

        # This response will generate JSON data that includes the all track
        # information.
        resolve_api = 'http://api.soundcloud.com/resolve?url='+self.url +\
            '&client_id='+keys.ID
        print 'Grabbing track information....'
        self.br.open(resolve_api)

        # Grab the browswer response and format the json data into an object
        resp = self.br.response()
        j = json.loads(resp.read())

        # Parse the data to retrive only what we need
        tags = self.parse_data(j)

        #self.id3_tag(tags)

        stream_api = 'http://api.soundcloud.com/tracks/' + tags._id + \
            '/stream?client_id=' + keys.ID

        self.page_load(stream_api)
        ColorMe.color_text('Successfully loaded mp3...', 'ok')

    def download(self):
        """
        Writes the response from SoundCloud stream api and saves track to
        current working directory. Create seperate thread for progress bar and
        wait till download completes.
        """

        # Init progress bar thread
        p = pbar.ProgressBar()
        p.start()

        try:
            # Write JSON response
            with open('test.mp3', 'wb') as f:

                f.write(self.br.response().read())

                # Stop the progress bar and notify the user
            pbar.stop = True

        except:
            pbar.kill = True
            pbar.stop = True
            sys.exit('Write Error...\n')

        ColorMe.color_text('\nDownload complete.', 'ok')

    def id3_tag(self):
        pass

    def run(self):
        """
        Main
        """

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
