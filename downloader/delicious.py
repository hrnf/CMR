import sys, re, os.path, time, zipfile, tempfile, argparse, http.client
from urllib.request import urlopen
from lxml import html

class MaxRetriesReached:
    pass

MAX_RETRY = 10
TIMEOUT = 1 # 1 second

def download_image(url, filepath):
#    print('Downloading url:', url)
    with urlopen(url) as stream:
        with open(filepath, 'wb') as f:
            f.write(stream.read())

def pages_in_chapter(tree):
     return max([int(o.text) for o in tree.xpath('.//option') if o.text != 'Comments'])

def image_in_page(tree):
    return tree.xpath(".//img[@id='image']")[0].get('src')

def url_from_data(series, volume, chapter, page):
    pass

def sid(tree):
    scripts = tree.xpath(".//script")
    script = [s.text for s in tree.xpath(".//script")
              if s.get('src') is None and 'var sid=' in s.text][0]
    sid = script.split(';', 1)[0].strip('\r\nvar sid=')
    return sid

def script_from_sid(sid):
    with urlopen('http://mangafox.me/media/js/list.{}.js'.format(sid)) as stream:
        return str(stream.read(), 'utf-8')

def volumes_from_script(script):
    lines = script.split('\n')
    volume = {}
    for l in lines:
        m = re.search(
            r'\["Vol (?P<volume>\d{2,3}) Ch (?P<chapter>\d{3,5}): (?P<title>.+)","v(?P=volume)/c(?P=chapter)"\],', l)
        if m is None:
            continue
        l = volume.setdefault(m.group('volume'), [])
        l.append({'number' : m.group('chapter'), 'title': m.group('title')})
    return volume

def url_from_chapter(series, volume, chapter):
    return 'http://mangafox.me/manga/{}/v{}/c{}/'.format(
        series, volume, chapter)

def series_from_url(url):
    return re.search(r'http:\/\/mangafox\.me\/manga\/(\w+)\/?.*'
                     , url).group(1)

def volumes_from_url(url):
    '''url = http://mangafox.me/manga/binbougami_ga/'''
    tree = html.parse(url)
    sid_ = sid(tree)
    volume_script = script_from_sid(sid_)
    return volumes_from_script(volume_script)

def download_page(series, volume, chapter, page, destination, tree = None):
    url = url_from_chapter(series, volume, chapter) + str(page) + '.html'
    if tree is None:
        tree = html.parse(url)
    imgurl = image_in_page(tree)
    ext = imgurl.rsplit('.')[-1]
    path = destination + '.' + ext
    for i in range(MAX_RETRY):
        try:
            download_image(imgurl, destination + '.' + ext)
            return path
        except http.client.HTTPException as ex:
            print(ex)
        wtime = random.random() * (i - 1) + TIMEOUT
        print('Retrying in {} seconds'.format(wtime))
        time.sleep(wtime)

def download_chapter(series, volume, chapter, directory):
    url = url_from_chapter(series, volume, chapter) + '1.html'
    tree = html.parse(url)
    pages = pages_in_chapter(tree)
    for page in range(1, pages + 1):
        path = os.path.join(directory, str(page))
        if page != 1:
            tree = None
        yield download_page(series, volume, chapter, page, path, tree)
        time.sleep(1)

def cbz_path(series, volume, chapter, directory):
    fname = '_'.join([series, volume, chapter]) + '.cbz'
    return os.path.join(directory, fname)

def create_zip(destination, paths):
    with zipfile.ZipFile(destination, 'w') as zip_:
        for fp in paths:
            zip_.write(fp)

def download_volume(series, volume, chapters, directory):
    for chapter in chapters:
        chapter = chapter['number']
        with tempfile.TemporaryDirectory() as tmpdir:
            print('Downloading chapter ', chapter)
            print(series, volume, chapter, tmpdir)
            cbz_p = cbz_path(series, volume, chapter, directory)
            try:
                os.stat(cbz_p)
            except FileNotFoundError:
                pass
            else:
                print('Chapter already exists, skipping.')
                continue
            pages = list(
                download_chapter(
                    series,
                    volume,
                    chapter,
                    tmpdir))
            print(cbz_p)
            create_zip(cbz_p, pages)

def download_series(url, directory):
    series = series_from_url(url)
    volumes = volumes_from_url(url)
    for volume in volumes:
        print('Downloading volume ', volume)
        download_volume(series, volume, volumes[volume], directory)

def handle_dir(path):
    try:
        os.makedirs(os.path.expanduser(path), exist_ok=True)
        return path
    except FileExistsError:
        print(('Expected {} to point to a directory or nothing, '
               'instead the path points to a file.').format(path))
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download some delicious mangoes.')
    parser.add_argument('url',
                   help='mangafox url of the series you want to download')
    parser.add_argument('directory',
                   help=('Directory where you wish to put your chapters and '
                         'volumes.'),
                        type=handle_dir,
    )
    parser.add_argument('-v', '--volume', help='To download only one volume')
    parser.add_argument('-c', '--chapter', help='To download only one chapter(volume must be passed) not implemente.d')

    args = parser.parse_args()
    if args.volume is None:
        download_series(args.url, args.directory)
    elif args.chapter is None:
        series = series_from_url(args.url)
        volumes = volumes_from_url(args.url)
        download_volume(series, args.volume, volumes[args.volume], args.directory)
    else:
        raise NotImplementedError()
"""        series = series_from_url(args.url)
        volumes = volumes_from_url(args.url)
        download_chapter(series,
                        args.volume,
                        args.chapter,
                        args.directory)
"""
