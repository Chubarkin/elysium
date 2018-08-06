import mock
import unittest

from elysium.query.commands import Command


class TestCommand(unittest.TestCase):
    @mock.patch('elysium.query.commands.const.COMMAND_TMPL', '%s %s')
    def test_to_str(self):
        command = Command()
        command.TYPE = 'TEST'
        self.assertEqual(command.to_str(), 'TEST ')

        command = Command('TEST_STRING')
        command.TYPE = 'TEST'
        self.assertEqual(command.to_str(), 'TEST TEST_STRING')
