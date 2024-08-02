import re
import os
import pandas as pd

tld = ['com', 'net', 'org', 'info', 'biz', 'gov', 'edu', 'co']


def find_main_domain(subdomain):
    # split by dot
    domain_parts = subdomain.split('.')
    # if the part before the last dot is a TLD, then the domain is 3 parts otherwise 2
    if domain_parts[-2] in tld:
        domain = '.'.join(domain_parts[-3:])
    else:
        domain = '.'.join(domain_parts[-2:])

    return domain


def clean_domains():
    # remove clean_domains.txt if it exists
    try:
        os.remove('cleaned_domains.txt')
    except FileNotFoundError:
        pass
    with open('domains.txt', 'r') as file:
        main_domains = []
        for line in file:
            subdomain = line.strip()
            main_domain = find_main_domain(subdomain)
            main_domains.append(main_domain)

        # remove duplicates
        main_domains = list(set(main_domains))

        with open('cleaned_domains.txt', 'w') as output_file:
            for domain in main_domains:
                output_file.write(domain + '\n')


def find_domain_or_subdomain(record_text):
    # Regular expression to match domain and subdomains
    pattern = re.compile(r'\b((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,})\b')
    domains = pattern.findall(record_text)
    return domains  # Directly return domains


def save_to_file(domain, main_domain, record_type, record):
    # Save the domain, main_domain, record_type and record to a CSV file
    data = {
        'Domain': [domain],
        'Unregistered Domain': [main_domain],
        'Record Type': [record_type],
        'Record': [record]
    }
    df = pd.DataFrame(data)
    if not os.path.exists('output.csv'):
        df.to_csv('output.csv', index=False)
    else:
        df.to_csv('output.csv', mode='a', header=False, index=False)