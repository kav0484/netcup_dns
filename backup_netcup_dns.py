import json
import datetime
import time
import os
from dotenv import load_dotenv
from nc_dnsapi import Client

#vars
list_domains=[]
list_records=[]



def dump_domain_dns_recors(domain,api,save_path):
    records = api.dns_records(domain)
    for record in records:
        list_records.append({"hostname": record.hostname, "type":record.type, "destination": record.destination })
        
    data = {domain: list_records}

    date = datetime.date.today().strftime("%d-%m-%Y")

    filename=save_path + '/' + domain + "_" + date + ".json"

    with open(filename, "w") as write_file:
        json.dump(data, write_file, indent=4)


if __name__ == '__main__':
    load_dotenv()
    now = time.time()

    customer = os.getenv("NETCUP_ENV_CUSTOMER")
    api_key = os.getenv("NETCUP_ENV_API_KEY")
    api_password = os.getenv("NETCUP_ENV_API_PASSWORD")
    save_path = os.getenv("NETCUP_ENV_SAVE_PATH")
    retention_days = os.getenv("NETCUP_ENV_RETENTION_JSON_FILE_DAYS")

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    
    with open('domains.txt') as f:

        all_strings = f.readlines()
        for string in all_strings:
            if string.strip() != '':
                list_domains.append(string.strip())

    
    for domain in list_domains:
        with Client(customer, api_key, api_password) as api:
            dump_domain_dns_recors(domain,api,save_path)

    #Удаляем файлы старше NETCUP_ENV_RETENTION_JSON_FILE_DAYS
    for f in os.listdir(save_path):
        path_f = save_path + '/' + f
        
        if os.stat(path_f).st_mtime < now - int(retention_days) * 86400:
            if os.path.isfile(path_f):
                os.remove(path_f)

    

        






