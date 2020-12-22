import os

mongo_host = os.environ.get('M_HOST')
mongo_port = os.environ.get('M_PORT')
mongo_login = os.environ.get('M_HAB_USER')
mongo_password = os.environ.get('M_HAB_PWD')

telega_token = os.environ.get('HABR_BOT_TOKEN')
telega_webhook_url = f'https://{os.environ.get("HABR_BOT_HOOK_HOST")}/{os.environ.get("HABR_BOT_HOOK_PATH")}'
