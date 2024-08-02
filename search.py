import dns.resolver
import logging
import concurrent.futures
import whois
from tqdm import tqdm
from utils import find_main_domain, clean_domains, find_domain_or_subdomain, save_to_file

logging.basicConfig(filename='dns_records.log', level=logging.INFO)


def get_dns_records(domain):
    record_types = ['MX', 'NS', 'SOA', 'TXT', 'CNAME', 'SRV', 'PTR']
    answers = {}

    for record_type in record_types:
        try:
            answers[record_type] = [rdata.to_text() for rdata in dns.resolver.resolve(domain, record_type)]
        except Exception as e:
            logging.error(f"Error for domain {domain}, record type {record_type}: {e}")

    return answers


def is_registered(domain):
    try:
        whois_info = whois.whois(domain)
        return bool(whois_info)
    except Exception as e:
        logging.error(f"Error checking domain {domain}: {e}")
        return False


def process_domain(domain):
    results = []
    try:
        for record_type, record_data in get_dns_records(domain).items():
            for record in record_data:
                matches = find_domain_or_subdomain(record)
                if matches:
                    for match in matches:
                        main_domain = find_main_domain(match.strip())
                        if main_domain:
                            if not is_registered(main_domain):
                                save_to_file(domain, main_domain, record_type, record)
                                print(f"Unregistered domain found: {main_domain}")
                                results.append(f"Unregistered domain found: {main_domain}")
    except Exception as e:
        logging.error(f"Error processing domain {domain}: {e}")
    return results


def main():
    with open('cleaned_domains.txt', 'r') as file:
        domains = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_domain, domain): domain for domain in domains}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing domains"):
            domain = futures[future]
            try:
                results = future.result()
                if results:
                    for result in results:
                        logging.info(result)
            except Exception as e:
                logging.error(f"Error with future for domain {domain}: {e}")


if __name__ == "__main__":
    clean_domains()
    main()
