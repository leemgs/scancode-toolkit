#
# Copyright (c) 2016-2018 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import json
import os.path

from commoncode.testcase import FileBasedTesting

from textcode.analysis import unicode_text_lines
from textcode.analysis import text_lines
from commoncode.fileutils import resource_iter


def check_text_lines(result, expected_file, regen=False):
        if regen:
            with open(expected_file, 'wb') as tf:
                json.dump(result, tf, indent=2)
        with open(expected_file, 'rb') as tf:
            expected = json.load(tf)
        assert expected == result


class TestAnalysis(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_text_lines_from_list_or_location_yield_same_results(self):
        test_file = self.get_test_loc('analysis/bsd-new')
        with codecs.open(test_file, 'rb', encoding='utf-8') as inf:
            test_strings_list = inf.read().splitlines(True)

        # test when we are passing a location or a list
        from_loc = list(text_lines(location=test_file))
        from_list = list(text_lines(location=test_strings_list))
        assert from_loc != from_list
        assert len(from_loc) > len(from_list)
        assert ''.join(from_loc) == ''.join(from_list)

    def test_unicode_text_lines_handles_weird_xml_encodings(self):
        test_file = self.get_test_loc('analysis/weird_encoding/easyconf-0.9.0.pom')
        result = list(unicode_text_lines(test_file))
        expected_file = self.get_test_loc('analysis/weird_encoding/easyconf-0.9.0.pom.expected')
        check_text_lines(result, expected_file)

    def test_archives_do_not_yield_text_lines(self):
        test_file = self.get_test_loc('archive/simple.jar')
        result = list(text_lines(test_file))
        assert [] == result

    def test_some_media_do_yield_text_lines(self):
        test_dir = self.get_test_loc('media_with_text')
        for test_file in resource_iter(test_dir, with_dirs=False):
            result = list(text_lines(test_file))
            assert result, 'Should return text lines:' + test_file
            assert any('nexb' in l for l in result)

    def test_some_media_do_not_yield_text_lines(self):
        test_dir = self.get_test_loc('media_without_text')
        for test_file in resource_iter(test_dir, with_dirs=False):
            result = list(text_lines(test_file))
            assert [] == result, 'Should not return text lines:' + test_file

    def test_text_lines_handles_sfdb(self):
        test_file = self.get_test_loc('analysis/splinefonts/Ambrosia.sfd')
        result = list(text_lines(test_file))
        expected_file = test_file + '.expected'
        expected = open(expected_file, 'rb').read().splitlines(True)
        assert expected == list(result)

    def test_text_lines_handles_jsmap1(self):
        test_file = self.get_test_loc('analysis/jsmap/angular-sanitize.min.js.map')
        result = list(text_lines(test_file))
        expected_file = test_file + '.expected'
        check_text_lines(result, expected_file)

    def test_text_lines_handles_jsmap2(self):
        test_file = self.get_test_loc('analysis/jsmap/types.js.map')
        result = list(text_lines(test_file))
        expected_file = test_file + '.expected'
        check_text_lines(result, expected_file)

    def test_text_lines_handles_jsmap3(self):
        test_file = self.get_test_loc('analysis/jsmap/ar-ER.js.map')
        result = list(text_lines(test_file))
        expected_file = test_file + '.expected'
        check_text_lines(result, expected_file)

    def test_text_lines_handles_jsmap4(self):
        test_file = self.get_test_loc('analysis/jsmap/button.js.map')
        result = list(text_lines(test_file))
        expected_file = test_file + '.expected'
        check_text_lines(result, expected_file)

    def test_text_lines_handles_broken_jsmap_as_plain_text(self):
        test_file = self.get_test_loc('analysis/jsmap/broken.js.map')
        result = list(text_lines(test_file))
        expected_file = test_file + '.expected'
        check_text_lines(result, expected_file)
