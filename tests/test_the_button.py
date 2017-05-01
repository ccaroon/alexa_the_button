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
                    'action': {
                        'name': 'action',
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
        "demo": "Thank you!"
    }

    # def setUp(self):
    #     print("setup")
    #
    # def tearDown(self):
    #     print("teardown")

    def test_demo(self):
        self.EVENT['request']['intent']['slots']['action']['value'] = "demo"
        result = the_button.the_button_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['demo']
        )

    def test_incorrect_app_id(self):
        event = copy.deepcopy(self.EVENT)
        event['session']['application']['applicationId'] = "foo bar"
        with self.assertRaises(ValueError):
            the_button.the_button_handler(event, {})

################################################################################
if __name__ == "__main__":
    unittest.main()
