import unittest
import os, os.path, shutil
from delicious import *

PATH = os.path.expanduser('~/mangoes')

class Tester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = html.parse('http://mangafox.me/manga/binbougami_ga/v06/c023/8.html')

    @unittest.skip("takes too long")
    def testdownload(self):
        filename = 'tempfile'
        download_image('http://a.mfcdn.net/store/manga/7654/06-023.0/compressed/tbinbougamiga_-ch023_004.jpg', filename)
        os.stat(filename)
        os.remove(filename)
        
    def test_pagelist(self):
        pages = pages_in_chapter(self.tree)
        self.assertEqual(28, pages)

    def test_image_in_page(self):
        url = image_in_page(self.tree)
        self.assertTrue('.jpg' in url)

    def test_sid(self):
        sid_ = sid(html.parse('http://mangafox.me/manga/binbougami_ga/'))
        int(sid_)

    def test_script_from_sid(self):
        self.assertTrue('var' in script_from_sid('7654'))

    def test_volumes_from_script(self):
        script = """var chapter_list = new Array(
  ["Vol 00 Ch 000: [Oneshot]","v00/c000"],
  ["Vol 01 Ch 001: You Might Be a God but Aren't You a Small Breasts God and Not a Misfortune God","v01/c001"],
  ["Vol 16 Ch 073.1: Come here","v16/c073.1"]
);"""
        v = volumes_from_script(script)

    def test_url_from_chapter(self):
        self.assertEqual(
            'http://mangafox.me/manga/binbougami_ga/v06/c023/',
            url_from_chapter('binbougami_ga', '06', '023'))
        
    def test_series_from_url(self):
        self.assertEqual(
            'binbougami_ga',
            series_from_url('http://mangafox.me/manga/binbougami_ga/'))

    def test_volumes_from_url(self):
        self.assertTrue(len(volumes_from_url('http://mangafox.me/manga/binbougami_ga/')) > 0)

    @unittest.skip("takes too long")
    def test_download_page(self):
        self.assertEqual(
            download_page('binbougami_ga', '01', '001', 1, 'test'),
            'test.jpg'
        )

    @unittest.skip("takes too long")
    def test_download_page_tree(self):
        self.assertEqual(
            download_page('binbougami_ga', '01', '001', 1, 'test', self.tree),
            'test.jpg'
        )

    @unittest.skip("takes too long")
    def test_download_chapter(self):
        itr = download_chapter('binbougami_ga', '01', '001', PATH)
        for i in itr:
            print(i)

    def test_cbz_path(self):
        print(cbz_path('binbougami_ga', '01', '001', PATH))

    def test_cbz_path(self):
        p = os.path.join(PATH, '{}.jpg')
        create_zip(os.path.join(PATH, 'mango.cbz'), [p.format(i) for i in range(1, 11)])

    @unittest.skip("takes too long")
    def test_download_volume(self):
        download_volume('binbougami_ga',
                        '01',
                        [
                            {'number':'001'},
                            {'number':'002'}
                        ],
                        PATH)

    @unittest.skip("takes too long")
    def test_download_series(self):
        download_series('http://mangafox.me/manga/binbougami_ga/',
                        os.path.join(PATH, 'series'))

    def test_handle_dir(self):
        '''Known error, if path points to a file handle_dir does not raise
an error.'''
        p = os.path.join(PATH, 'foo/bar')
        self.assertEqual(handle_dir(p), p)
        os.stat(p)
        shutil.rmtree(p)

if __name__ == '__main__':
    unittest.main()
