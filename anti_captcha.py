import json
from dotenv import load_dotenv
import os

def acp_api_send_request(driver, message_type, data={}):
    message = {
		# this receiver has to be always set as antiCaptchaPlugin
        'receiver': 'antiCaptchaPlugin',
        # request type, for example setOptions
        'type': message_type,
        # merge with additional data
        **data
    }
    return driver.execute_script("""return window.postMessage({});
    """.format(json.dumps(message)))

def set_anticpatcha_settigns(d):
    load_dotenv()
    d.driver.get('https://antcpt.com/blank.html')
    acp_api_send_request(
        d.driver,
        'setOptions',
        {
            'options': {
                'antiCaptchaApiKey': os.getenv('API_KEY'),
                'solveFuncaptcha': True,
                'solveProxyOnTasks': True,
                'autoSubmitForm': True,
                'userProxyProtocol': os.getenv('PROXY_PROTOCOL'),
                'userProxyServer': os.getenv('PROXY_IP'),
                'userProxyPort': os.getenv('PROXY_PORT'),
                'userProxyLogin': os.getenv('PROXY_LOGIN'),
                'userProxyPassword': os.getenv('PROXY_PASSWORD')
                }
        }
    )
