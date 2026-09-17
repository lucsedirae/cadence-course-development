"""Synthetic intake and local HTTP checks, with no provider calls."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/cadence/scripts'))
import cadence
import intake
import progress


class IntakeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name) / 'synthetic-course'
        self.answers = dict(title='Synthetic course', intent='build', delivery='classroom', learners='ncos',
                            duration='few_hours', role='builder', source_material='yes')

    def test_opening_intake_does_not_start_a_project(self):
        self.assertEqual(intake.view(self.project)['status'], 'pending')
        self.assertFalse(self.project.exists())

    def test_invalid_answers_do_not_write(self):
        for answers in ({}, {**self.answers, 'extra': 'value'}, {**self.answers, 'title': ' '},
                        {**self.answers, 'title': 'Name\nwith a newline'}, {**self.answers, 'title': 'x' * 161},
                        {**self.answers, 'learners': 'everyone'}, {**self.answers, 'intent': ['build']}):
            with self.assertRaises(ValueError):
                intake.save(self.project, answers)
        self.assertFalse(self.project.exists())

    def test_requested_choices_and_uncertainty_are_preserved(self):
        self.assertEqual([len(q.get('options', [])) for q in intake.QUESTIONS], [0, 3, 4, 8, 5, 3, 3])
        for question in intake.QUESTIONS[1:]:
            for value, _ in question['options']:
                self.assertEqual(intake.validate({**self.answers, question['id']: value})[question['id']], value)
        answers = dict(title='Unknowns allowed', intent='unsure', delivery='unsure', learners='unsure',
                       duration='unsure', role='instructor', source_material='unsure')
        record = intake.save(self.project, answers)
        self.assertEqual(record['answers'], answers)
        self.assertFalse((self.project / '.cadence/library.sqlite3').exists())
        self.assertEqual(intake.summary(record)[-1]['answer'], 'Not sure yet')

    def test_retry_preserves_answers_and_corrupt_records(self):
        first = intake.save(self.project, self.answers)
        before = intake.record_path(self.project).read_bytes()
        self.assertEqual(intake.save(self.project, self.answers), first)
        with self.assertRaisesRegex(ValueError, 'already saved'):
            intake.save(self.project, {**self.answers, 'intent': 'review'})
        self.assertEqual(intake.record_path(self.project).read_bytes(), before)
        intake.record_path(self.project).write_text('{broken')
        with self.assertRaisesRegex(ValueError, 'preserve'):
            intake.save(self.project, self.answers)

    def test_existing_course_skips_intake(self):
        cadence.initialize(self.project, 'Existing course')
        self.assertEqual(intake.view(self.project)['status'], 'existing')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            intake.save(self.project, self.answers)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cadence.main(['init', '--project', str(self.project)]), 0)

    def test_cli_requires_intake_and_uses_its_name(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cadence.main(['init', '--project', str(self.project), '--title', 'Wrong']), 1)
        self.assertFalse(self.project.exists())
        intake.save(self.project, self.answers)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cadence.main(['init', '--project', str(self.project), '--title', 'Wrong']), 1)
        source = self.project.parent / 'synthetic-guidance'
        source.mkdir()
        (source / 'process.md').write_text('Synthetic institutional process.')
        with patch.object(cadence, 'INSTITUTION_DIR', source), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cadence.main(['init', '--project', str(self.project)]), 0)
        self.assertEqual(cadence.initialize(self.project, 'Ignored')['title'], self.answers['title'])
        self.assertEqual(cadence.list_sources(self.project)[0]['library'], 'institution')

    def test_progress_can_show_unknown_intent_without_starting_work(self):
        intake.save(self.project, {**self.answers, 'intent': 'unsure'})
        progress.initialize(self.project, self.answers['title'], mode='orient')
        state = progress.view(self.project)
        self.assertEqual(state['mode'], 'orient')
        self.assertEqual(state['intake'][1]['answer'], 'Not sure yet')
        self.assertEqual(state['phases']['analysis']['status'], 'pending')

    def test_http_validates_origin_answers_and_routes(self):
        server, url = intake.make_server(self.project, demo=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 2)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        origin = '/'.join(url.split('/', 3)[:3])
        def request(data, **headers):
            return urllib.request.Request(url + 'answers', data=data,
                headers={'Content-Type': 'application/json', 'Origin': origin, **headers}, method='POST')
        with opener.open(url + 'state') as response:
            self.assertEqual(json.load(response)['status'], 'pending')
        with opener.open(url) as response:
            self.assertIn(b'Seven quick questions', response.read())
            self.assertNotIn('Access-Control-Allow-Origin', response.headers)
        for req, expected in [(request(b'{}'), 400), (request(b'x' * 8193), 400),
                              (request(b'{}', Origin='http://attacker.example'), 403),
                              (request(b'{}', Host='attacker.example'), 404),
                              (urllib.request.Request(url + '../.cadence/intake.json'), 404)]:
            with self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(req)
            self.assertEqual(error.exception.code, expected)
        self.assertFalse(self.project.exists())
        with opener.open(request(json.dumps(self.answers).encode())) as response:
            self.assertEqual(json.load(response)['status'], 'complete')
        with opener.open(url + 'state') as response:
            self.assertEqual(json.load(response)['answers'], self.answers)
        self.assertFalse((self.project / '.cadence/library.sqlite3').exists())

    def test_older_intake_remains_readable_without_invented_answers(self):
        legacy = {'version': 1, 'status': 'complete', 'saved_at': '2026-09-17T12:00:00Z',
                  'answers': {q['id']: self.answers[q['id']] for q in intake.QUESTIONS[:4]}}
        path = intake.record_path(self.project)
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(legacy))
        before = path.read_bytes()
        self.assertEqual(intake.read(self.project), legacy)
        self.assertEqual(intake.view(self.project)['status'], 'complete')
        self.assertEqual([r['answer'] for r in intake.summary(legacy)[4:]], ['Not asked in earlier intake'] * 3)
        progress.initialize(self.project, 'Synthetic legacy course')
        self.assertEqual(progress.view(self.project)['intake'][4]['answer'], 'Not asked in earlier intake')
        self.assertEqual(path.read_bytes(), before)

    def test_new_intake_requires_all_seven_answers(self):
        for key in ('duration', 'role', 'source_material'):
            incomplete = {k: v for k, v in self.answers.items() if k != key}
            with self.assertRaisesRegex(ValueError, 'all 7'):
                intake.save(self.project, incomplete)
        record = intake.save(self.project, self.answers)
        self.assertEqual(record['version'], 2)
        self.assertEqual(intake.read(self.project)['answers'], self.answers)
        cli_project = self.project.parent / 'cli-course'
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(intake.main(['save', '--project', str(cli_project), '--title', 'CLI course',
                '--intent', 'review', '--delivery', 'self_paced', '--learners', 'officers',
                '--duration', 'about_a_day', '--role', 'approver', '--source-material', 'no']), 0)
        self.assertEqual(intake.read(cli_project)['answers']['source_material'], 'no')


if __name__ == '__main__':
    unittest.main()
