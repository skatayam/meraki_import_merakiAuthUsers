# -*- coding: utf-8 -*-
import sys
import requests
from jinja2 import Template, Environment, FileSystemLoader
import csv
args = sys.argv

baseUrl = "https://api.meraki.com/api/v1"
apikey = "YOUR_API_KEY"
orgid = "YOUR_ORG_ID"
netid = "YOUR_NETWORK_ID_for_import_Users"

def main():
    r = None
    headers = {'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'}
    api_url = baseUrl + '/organizations/' + orgid + '/actionBatches'

    env = Environment(loader=FileSystemLoader('./templates', encoding='utf-8'))
    template = env.get_template('AuthUsers.j2')

    data = [i for i in csv.DictReader(open(args[1]))]
    post_data = template.render({"data": data, "nw": netid})

    try:
        r = requests.post(api_url, data=post_data.encode('utf-8'), headers=headers)
        status_code = r.status_code
        resp = r.text
        print("Status code is: " + str(status_code))
        if status_code == 201 or status_code == 202:
            print("Auth Users created successfully...")
            return resp
        else:
            print("Error occurred in POST device claim --> " + resp)
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if r: r.close()

if __name__ == '__main__':
    main()