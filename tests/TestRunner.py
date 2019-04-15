import unittest


from concurrencytest import ConcurrentTestSuite, fork_for_tests


import logging

from tests.test_auth import TestAuthWithGoogleAuth, TestAuthWithOAuth2Client, TestAuthWithoutAuth, \
    TestGoogleAuthWithoutHttplib2
from tests.test_media_upload import TestMediaUpload

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_Trigger():
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromTestCase(TestAuthWithGoogleAuth))
        suite.addTests(loader.loadTestsFromTestCase(TestAuthWithOAuth2Client))
        suite.addTests(loader.loadTestsFromTestCase(TestAuthWithoutAuth))
        suite.addTests(loader.loadTestsFromTestCase(TestGoogleAuthWithoutHttplib2))
        suite.addTests(loader.loadTestsFromTestCase(TestMediaUpload))

        logger.debug('Loaded %d test cases...' % suite.countTestCases())
        runner = unittest.TextTestRunner()
        logger.debug('\nRun same tests with 8 processes:')
        concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(8))
        runner.run(concurrent_suite)


if __name__=='__main__':
    test_Trigger()