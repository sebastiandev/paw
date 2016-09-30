import multiprocessing
import requests
import os
from lxml import html
from emailer import Emailer
from webpeeper import email_credentials


class Peeper(object):

    def __init__(self, *finders):
        self._finders = finders
        self._emailer = Emailer(*email_credentials())
        self._findings_file_name = os.path.join(os.path.expanduser("~"), 'findings')

        with open(self._findings_file_name, 'r') as f:
            self._findings = set([e.strip().replace('\r', '').replace('\n', '') for e in f.readlines()])

    def _peep_url(self, finder):
        req = requests.get(finder.url)
        tree = html.fromstring(req.content)
        findings = finder.find(tree)

        if findings:
            msg = ''
            for title, content, content_date, link in findings:
                if link not in self._findings:
                    self._findings.add(link)
                    msg += "\r\n  - Link: {}\r\n    Date: {}\r\n    Title: {}\r\n    Post: {}\r\n""" \
                        .format(link, content_date, title, content)

            if msg:
                header = "{} with keywords {}".format(finder.name, ','.join(finder.keywords))
                header += "\r\n\r\n"
                header += msg

                self._emailer.send('devsebas@gmail.com',
                                   ["superpacko@gmail.com", "grillo.svy@gmail.com"],
                                   'Promociones Aereas',
                                   header)

    def _store_findings(self):
        with open(self._findings_file_name, 'w') as f:
            f.write('\n'.join(self._findings))

    def peep(self):
        processes = []

        if len(self._finders) == 1:
            self._peep_url(self._finders[0])

        else:
            for finder in self._finders:
                p = multiprocessing.Process(name='peep', target=self._peep_url, args=(finder,))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

        self._store_findings()

if __name__ == '__main__':
    import argparse
    from finders import PromocionesAereasFinder

    parser = argparse.ArgumentParser("URL Peeper")
    parser.add_argument("--promociones-aereas", action='store_true', help="Look for specific offers", required=False)
    args = parser.parse_args()

    finders = []
    if args.promociones_aereas:
        finders.append(PromocionesAereasFinder())

    Peeper(*finders).peep()
