"""
Created on Jul 05, 2026

@author: CyberiaResurrection
"""
import os
from unittest.mock import patch

import responses

from Tests.Pyfakefs.baseTest import baseTest
from pytest_console_scripts import ScriptRunner


class testWikiUploadPDF(baseTest):

    @patch('time.sleep', return_value=None)
    @responses.activate
    def test_get_sector_no_routes(self, patched_time_sleep):
        secpath = self.unpack_filename('../DownloadFiles/Reft Sector.sec')
        xmlpath = self.unpack_filename('../DownloadFiles/Reft Sector.xml')
        runpath = self.unpack_filename('PyRoute/downloadsec.py')

        seccontent = ''
        with open(secpath) as f:
            seccontent = f.read()

        xmlcontent = ''
        with open(xmlpath) as f:
            xmlcontent = f.read()

        self.setUpPyfakefs(allow_root_user=False)
        self.fs.add_real_file(runpath, target_path='/downloadsec.py')
        os.environ.update({'XDG_DATA_HOME': '/PyRoute/'})
        with open('/seclist', 'wt', encoding='utf-8') as f:
            f.writelines('Reft Sector')

        responses.add(
            responses.GET,
            'http://www.travellermap.com/api/sec',
            body=seccontent
        )
        responses.add(
            responses.GET,
            'http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml',
            body=xmlcontent
        )

        cwd = os.getcwd()
        runner = ScriptRunner(launch_mode="inprocess", rootdir=cwd, print_result=False)
        foo = runner.run(['/downloadsec.py', '/seclist', "/"])
        self.assertEqual(0, foo.returncode, "downloadsec did not complete successfully: " + foo.stderr)

        responses.assert_call_count('http://www.travellermap.com/api/sec?sector=Reft+Sector&type=SecondSurvey&milieu=M1105', 1)
        responses.assert_call_count('http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml', 1)

        downloadsec = '/Reft Sector.sec'
        downloadxml = '/Reft Sector.xml'

        self.assertTrue(os.path.exists(downloadsec))
        self.assertTrue(os.path.exists(downloadxml))

        secactual = ''
        with open(downloadsec) as f:
            secactual = f.read()
        self.assertEqual(seccontent, secactual)

        xmlactual = ''
        with open(downloadxml) as f:
            xmlactual = f.read()
        self.assertEqual(xmlcontent, xmlactual)
        patched_time_sleep.assert_called_once()

    @patch('time.sleep', return_value=None)
    @responses.activate
    def test_get_sector_routes(self, patched_time_sleep):
        secpath = self.unpack_filename('../DownloadFiles/Reft Sector-routes.sec')
        xmlpath = self.unpack_filename('../DownloadFiles/Reft Sector.xml')
        runpath = self.unpack_filename('PyRoute/downloadsec.py')

        seccontent = ''
        with open(secpath) as f:
            seccontent = f.read()

        xmlcontent = ''
        with open(xmlpath) as f:
            xmlcontent = f.read()

        self.setUpPyfakefs(allow_root_user=False)
        self.fs.add_real_file(runpath, target_path='/downloadsec.py')
        os.environ.update({'XDG_DATA_HOME': '/PyRoute/'})
        with open('/seclist', 'wt', encoding='utf-8') as f:
            f.writelines('Reft Sector')

        secparams = {'sector': 'Reft Sector', 'type': 'SecondSurvey', "milieu": 'M1105', 'routes': 1}
        responses.add(
            responses.GET,
            'http://www.travellermap.com/api/sec?sector=Reft+Sector&type=SecondSurvey&milieu=M1105&routes=1',
            match=[responses.matchers.query_param_matcher(secparams)],
            body=seccontent
        )
        responses.add(
            responses.GET,
            'http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml',
            body=xmlcontent
        )

        cwd = os.getcwd()
        runner = ScriptRunner(launch_mode="inprocess", rootdir=cwd, print_result=False)
        foo = runner.run(['/downloadsec.py', '--routes', '/seclist', "/"])
        self.assertEqual(0, foo.returncode, "downloadsec did not complete successfully: " + foo.stderr)

        responses.assert_call_count('http://www.travellermap.com/api/sec?sector=Reft+Sector&type=SecondSurvey&milieu=M1105&routes=1', 1)
        responses.assert_call_count('http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml', 1)

        downloadsec = '/Reft Sector.sec'
        downloadxml = '/Reft Sector.xml'

        self.assertTrue(os.path.exists(downloadsec))
        self.assertTrue(os.path.exists(downloadxml))

        secactual = ''
        with open(downloadsec) as f:
            secactual = f.read()
        self.assertEqual(seccontent, secactual)

        xmlactual = ''
        with open(downloadxml) as f:
            xmlactual = f.read()
        self.assertEqual(xmlcontent, xmlactual)
        patched_time_sleep.assert_called_once()

    @patch('time.sleep', return_value=None)
    @responses.activate
    def test_get_sector_no_routes_retry_once(self, patched_time_sleep):
        secpath = self.unpack_filename('../DownloadFiles/Reft Sector.sec')
        xmlpath = self.unpack_filename('../DownloadFiles/Reft Sector.xml')
        runpath = self.unpack_filename('PyRoute/downloadsec.py')

        seccontent = ''
        with open(secpath) as f:
            seccontent = f.read()

        xmlcontent = ''
        with open(xmlpath) as f:
            xmlcontent = f.read()

        self.setUpPyfakefs(allow_root_user=False)
        self.fs.add_real_file(runpath, target_path='/downloadsec.py')
        os.environ.update({'XDG_DATA_HOME': '/PyRoute/'})
        with open('/seclist', 'wt', encoding='utf-8') as f:
            f.writelines('Reft Sector')

        baseurl = 'http://www.travellermap.com/api/sec'

        rsp1 = responses.add(
            responses.GET,
            baseurl,
            status=500
        )
        rsp2 = responses.add(
            responses.GET,
            baseurl,
            body=seccontent
        )
        responses.add(
            responses.GET,
            'http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml',
            body=xmlcontent
        )

        cwd = os.getcwd()
        runner = ScriptRunner(launch_mode="inprocess", rootdir=cwd, print_result=False)
        foo = runner.run(['/downloadsec.py', '/seclist', "/"])
        self.assertEqual(0, foo.returncode, "downloadsec did not complete successfully: " + foo.stderr)

        responses.assert_call_count('http://www.travellermap.com/api/sec?sector=Reft+Sector&type=SecondSurvey&milieu=M1105', 2)
        responses.assert_call_count('http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml', 1)

        downloadsec = '/Reft Sector.sec'
        downloadxml = '/Reft Sector.xml'

        self.assertTrue(os.path.exists(downloadsec))
        self.assertTrue(os.path.exists(downloadxml))

        secactual = ''
        with open(downloadsec) as f:
            secactual = f.read()
        self.assertEqual(seccontent, secactual)

        xmlactual = ''
        with open(downloadxml) as f:
            xmlactual = f.read()
        self.assertEqual(xmlcontent, xmlactual)
        patched_time_sleep.assert_called_once()

    @patch('time.sleep', return_value=None)
    @responses.activate
    def test_get_sector_no_routes_retry_four_times(self, patched_time_sleep):
        secpath = self.unpack_filename('../DownloadFiles/Reft Sector.sec')
        xmlpath = self.unpack_filename('../DownloadFiles/Reft Sector.xml')
        runpath = self.unpack_filename('PyRoute/downloadsec.py')

        seccontent = ''
        with open(secpath) as f:
            seccontent = f.read()

        xmlcontent = ''
        with open(xmlpath) as f:
            xmlcontent = f.read()

        self.setUpPyfakefs(allow_root_user=False)
        self.fs.add_real_file(runpath, target_path='/downloadsec.py')
        os.environ.update({'XDG_DATA_HOME': '/PyRoute/'})
        with open('/seclist', 'wt', encoding='utf-8') as f:
            f.writelines('Reft Sector')

        baseurl = 'http://www.travellermap.com/api/sec'

        rsp1 = responses.add(
            responses.GET,
            baseurl,
            status=500
        )
        rsp2 = responses.add(
            responses.GET,
            baseurl,
            status=500
        )
        rsp3 = responses.add(
            responses.GET,
            baseurl,
            status=500
        )
        rsp4 = responses.add(
            responses.GET,
            baseurl,
            status=500
        )
        responses.add(
            responses.GET,
            'http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml',
            body=xmlcontent
        )

        cwd = os.getcwd()
        runner = ScriptRunner(launch_mode="inprocess", rootdir=cwd, print_result=False)
        foo = runner.run(['/downloadsec.py', '/seclist', "/"])
        self.assertEqual(0, foo.returncode, "downloadsec did not complete successfully: " + foo.stderr)

        responses.assert_call_count('http://www.travellermap.com/api/sec?sector=Reft+Sector&type=SecondSurvey&milieu=M1105', 4)
        responses.assert_call_count('http://travellermap.com/api/metadata?sector=Reft+Sector&accept=text%2Fxml', 1)

        downloadsec = '/Reft Sector.sec'
        downloadxml = '/Reft Sector.xml'

        self.assertFalse(os.path.exists(downloadsec))
        self.assertTrue(os.path.exists(downloadxml))

        xmlactual = ''
        with open(downloadxml) as f:
            xmlactual = f.read()
        self.assertEqual(xmlcontent, xmlactual)
        patched_time_sleep.assert_called_once()
