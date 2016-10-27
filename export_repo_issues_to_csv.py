"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import requests

GITHUB_USER = 'jobiols'
GITHUB_PASSWORD = ''
REPO = 'odoo/odoo'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

nnn = 0


def write_issues(r):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    print r


#    for issue in r.json():
#        print '#', nnn, issue['number'], issue['title']
#        print '-' * len(issue['title'])
#        if 'body' in issue:
#            print issue['body']
#            print '-' * len(issue['title'])


def get_requests(ISSUES_FOR_REPO_URL, AUTH):
    print 'get_requests'
    if GITHUB_PASSWORD:
        return requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
    else:
        return requests.get(ISSUES_FOR_REPO_URL)

# csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
# csvout = csv.writer(open(csvfile, 'wb'))
# csvout.writerow(('id', 'Title', 'Body', 'Created At', 'Updated At'))

r = get_requests(ISSUES_FOR_REPO_URL, AUTH)
write_issues(r)
print 'antes get pepe'

print 'despues get'
# more pages? examine the 'link' header returned
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<') + 1:-1]) for url, rel in
         [link.split(';') for link in
          r.headers['link'].split(',')]])

    while 'last' in pages and 'next' in pages:
        r = get_requests(pages['next'], 1, auth=AUTH)
        print 'aaa', r
        write_issues(r)
        if pages['next'] == pages['last']:
            break
