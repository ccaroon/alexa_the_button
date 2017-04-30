import copy
import unittest
import the_button
import secrets

class TestTheButton(unittest.TestCase):

    EVENT = {
        'request': {
            'type': "IntentRequest",
            'intent': {
                'name': "TheButton",
                'slots': {
                    'aspect': {
                        'name': 'aspect',
                        'value': None
                    }
                }
            }
        },
        'session': {
            'new': True,
            'application': {
                'applicationId': secrets.APPLICATION_ID
            }
        }
    }

    test_patterns = {
        'deploy': "Deploying",
        "test": "Testing",
        "spin": "Spinning"
    }

    # def setUp(self):
    #     print("setup")
    #
    # def tearDown(self):
    #     print("teardown")

    def test_deploy(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "deploy"
        result = the_button.the_button_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['deploy']
        )

    def test_test(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "test"
        result = the_button.the_button_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['test']
        )

    def test_spin(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "spin"
        result = the_button.the_button_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['spin']
        )

    def test_incorrect_app_id(self):
        event = copy.deepcopy(self.EVENT)
        event['session']['application']['applicationId'] = "foo bar"
        with self.assertRaises(ValueError):
            the_button.the_button_handler(event, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
