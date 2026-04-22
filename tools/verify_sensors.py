import json
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO)

def verify_config(path='config.json'):
    logging.info('Verifying config')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.parse_args()
    verify_config()
