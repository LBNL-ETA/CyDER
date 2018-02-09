import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

import argparse
from tools import db_models

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd_parser = parser.add_subparsers(dest='cmd')
    parser_import_models = cmd_parser.add_parser('import_models', help='Import models to the db')
    parser_import_models.add_argument('model_names', nargs='*')
    args = parser.parse_args()

    if args.cmd == 'import_models':
        for model_name in args.model_names:
            print('Model ' + model_name)
            db_models.import_model(model_name)
