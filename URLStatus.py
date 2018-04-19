import requests
import json
from time import sleep

class URLStatus:
    user_agents = {}
    urls = []
    errors = []

    def __init__(self, args):
        self.user_agents = self._getUAs(args)
        self.urls = self._getUrls(args)
        self.runTests(args)
        print(self.errors)


    def runTests(self, args):
        allowed_devices = ['desktop','mobile','tablet']
        if not args.desktop:
            allowed_devices.remove('desktop')
        if not args.mobile:
            allowed_devices.remove('mobile')
        if not args.tablet:
            allowed_devices.remove('tablet')

        for url in self.urls:
            for device in self.user_agents:
                if device in allowed_devices:
                    for ua in self.user_agents[device]:
                        self._test(url, ua)

    def _test(self, url, ua):
        headers = {'user-agent':ua}
        print "\nTesting URL: %s With UA: %s" % (url, ua)
        for n in range(5): # sometimes we get ioerror and need to retry
            try:
                r = requests.get(url, headers=headers)
                print("'{}' >> URL FINAL >> '{}'".format(url, r.url))
                print("Status {}, Historico: {}".format(r.status_code, r.history))
                sleep(0.5)
                break

            except requests.exceptions.TooManyRedirects:
                print("*** REDIRECT LOOP!! ***")
                print("*** REDIRECT LOOP!! ***")
                self.errors.append([url, ua, "REDIRECT LOOP"])
                break
                #exit(1)
            
            except requests.exceptions.RequestException as e:
                print("Request error: {}".format(e))
                self.errors.append([url, ua, "REQUEST ERROR"])
                exit(1)

            except IOError as e:
                print("Request error, retrying... {}".format(e))
                self.errors.append([url, ua, "IOERROR"])

    def _getUAs(self, args):
        if args.user_agents_file:
            if ".json" in args.user_agents_file:
                user_agents = json.load(open(args.user_agents_file,'r'))
            else:
                print("file type not yet supported")
                exit()
        else:
            user_agents = json.load(open("uas.json",'r'))
        
        return user_agents

    def _getUrls(self, args):
        if args.urls_file:
            with open(args.urls_file) as f:
                urls = [line.rstrip() for line in f.readlines()]
        else:
            urls = [args.url]
        return urls