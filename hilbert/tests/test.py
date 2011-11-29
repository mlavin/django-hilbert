from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

from hilbert.test import TestCase, CoverageRunner


class TestRunnerTest(TestCase):
    def do_test(self, default_test_labels_setting, test_labels_passed,
                expected_test_labels_used):

        # FIXME: this method is ugly. It should be possible to clean it up
        # using mock if we're willing to add that as a test dependency.

        if default_test_labels_setting is None:
            if hasattr(settings, 'DEFAULT_TEST_LABELS'):
                delattr(settings, 'DEFAULT_TEST_LABELS')
        else:
            settings.DEFAULT_TEST_LABELS = default_test_labels_setting

        # Avoid all the coverage machinery
        coverage_modules = []
        if hasattr(settings, 'COVERAGE_MODULES'):
            coverage_modules = settings.COVERAGE_MODULES
            delattr(settings, 'COVERAGE_MODULES')

        # monkey-patch DjangoTestSuiteRunner, which is what hilbert runner
        # will invoke
        def fake_run_tests(self, test_labels, extra_tests, **kwargs):
            return test_labels

        real_run_tests = DjangoTestSuiteRunner.run_tests

        # Call run_tests. Using our fake run_tests, it should return
        # whatever hilbert's run_tests passed in as test_labels,
        # which should be the DEFAULT_TEST_LABELS
        try:
            DjangoTestSuiteRunner.run_tests = fake_run_tests
            runner = CoverageRunner()
            labels_used = runner.run_tests(test_labels=test_labels_passed)
        finally:
            # un-monkey-patch
            DjangoTestSuiteRunner.run_tests = real_run_tests
            # restore COVERAGE_MODULES
            settings.COVERAGE_MODULES = coverage_modules
        self.assertEqual(labels_used, expected_test_labels_used)

    def test_default_test_labels(self):
        """If default is set and no tests named on command line, the
        defaults are used"""
        self.do_test(['foo', 'bar'], [], ['foo', 'bar'])

    def test_default_test_labels_unset(self):
        """If default is not set, you get whatever you say on the command line"""
        self.do_test(None, [], [])
        self.do_test(None, ['x', 'y'], ['x', 'y'])

    def test_default_test_labels_all(self):
        """If default is set, you can act like it's not by saying 'all'
        on the command line"""
        self.do_test(['foo', 'bar'], ['all'], [])
