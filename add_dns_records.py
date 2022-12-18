import json
import os
from pprint import pprint
from dotenv import load_dotenv
from nc_dnsapi import Client, DNSRecord

global add_from_file


add_from_file ="example.com.json"


if __name__ == '__main__':
    
    list_netcup_dns_objects=[]
    load_dotenv()

    customer = os.getenv("NETCUP_ENV_CUSTOMER")
    api_key = os.getenv("NETCUP_ENV_API_KEY")
    api_password = os.getenv("NETCUP_ENV_API_PASSWORD")
    
    with open(add_from_file) as f:
        dns_records = json.load(f)
        domain = list(dns_records.keys())[0]
    #Добавляем записи
    with Client(customer, api_key, api_password) as api:
        for dns_record in dns_records[domain]:
            api.add_dns_record(domain,DNSRecord(dns_record["hostname"],dns_record['type'], dns_record['destination']))
       
    
    
    
        

        

    
            

        



        
        