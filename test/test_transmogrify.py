from transmogrify.transmogrify import transmogrify
from deem.testfixture import BaseTest
from datetime import datetime
import os
import os.path
import json


class TestTransmogrify(BaseTest):
    def setUp(self):
        super().setUp()

    def test_transmogrify_date_format(self):
        date_format = '%Y-%m-%dT%H:%M:%S.%f'

        raw_event = {
            'server': '10.10.0.177',
            'date': '2019-07-01T15:27:25.000000',
            'severity': 'WARN',
            'process': 'microsrvc',
            'message': 'retry failed to downstream service luxadapter'
        }

        expected_log_events = [
            {
                'server': '10.10.0.177',
                # test date format is JavaScript ISO format
                'date': datetime.strptime('2019-07-01T15:27:25.000000', date_format).strftime(date_format),
                'severity': 'WARN',
                'process': 'microsrvc',
                'message': 'retry failed to downstream service luxadapter'
            }
        ]
        actual_log_events = transmogrify([raw_event])

        self._assert_dict_lists_equal(expected_log_events, actual_log_events)

    def test_transmogrify_all_formats(self):
        raw_events = self._read_json('transmogrify-input.json')
        expected_log_events = self._read_json('transmogrify-output.json')
        actual_log_events = transmogrify(raw_events)

        self._assert_dict_lists_equal(expected_log_events, actual_log_events)

    def _read_json(self, file_name: str):
        file_path = os.path.abspath(os.path.join(__file__, '..', file_name))
        with open(file_path) as f:
            data = json.load(f)
        return data

    def _assert_dict_lists_equal(self, one: [dict], two: [dict]):
        self.assertEqual(len(one), len(two))
        for dict_one, dict_two in zip(one, two):
            self.assertDictEqual(dict_one, dict_two)
