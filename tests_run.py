import unittest
import xmlrunner
import logger
import click
import time


def find_testsuit(run_tests):

    suite = unittest.TestSuite()

    if run_tests in 'discovery':
        dis = unittest.TestLoader()
        all_demo_tests = dis.discover('discovery', '*.py')
        for test in all_demo_tests:
            suite.addTests(test)

    if run_tests in 'traffic_management_1':
        dis = unittest.TestLoader()
        all_demo_tests = dis.discover('traffic_management', 'test_load_balancing.py')
        for test in all_demo_tests:
            suite.addTests(test)

    if run_tests in 'traffic_management_2':
        dis = unittest.TestLoader()
        all_demo_tests = dis.discover('traffic_management', 'test_virtual_service.py')
        for test in all_demo_tests:
            suite.addTests(test)

    if run_tests in 'traffic_management_3':
        dis = unittest.TestLoader()
        all_demo_tests = dis.discover('traffic_management', 'test_header_rule.py')
        for test in all_demo_tests:
            suite.addTests(test)

    if run_tests in 'failure_recovery':
        dis = unittest.TestLoader()
        all_demo_tests = dis.discover('failure_recovery', '*.py')
        for test in all_demo_tests:
            suite.addTests(test)

    if run_tests in 'envoyctl':
        dis = unittest.TestLoader()
        tests = dis.discover('envoyctl', '*pilot*.py')
        for test in tests:
            suite.addTests(test)
        tests = dis.discover('envoyctl', 'test_proxy_list.py')
        for test in tests:
            suite.addTests(test)
        tests = dis.discover('envoyctl', 'test_proxy_config.py')
        for test in tests:
            suite.addTests(test)
        tests = dis.discover('envoyctl', 'test_iptables.py')
        for test in tests:
            suite.addTests(test)

    runner = xmlrunner.XMLTestRunner(output='test-reports')
    runner.run(suite)


def set_env(env):
    with open('update_env.txt', 'wr') as f:
        f.writelines('env:%s' % env)
    print("create update_env time is %s" % time.time())


@click.command()
@click.option('--feature', help='The feature you want to test.')
@click.option('--env', help='The environment you want to run tests')
def parse_command(feature, env):
    print("feature is %s, env is %s" % (feature, env))
    set_env(env)
    find_testsuit(feature)


if  __name__ == "__main__":
    logger.create_log()
    parse_command()
