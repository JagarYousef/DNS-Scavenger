## DNS Scavenger
### Expired domains in DNS records finder
This script will find expired domains (not registered) in DNS records, it takes a list of domains and search in all its `MX`, `NS`, `SOA`, `TXT`, `CNAME`, `SRV`, `PTR` records for other domains and then check if these domains are available or not.

### Usage
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
# add your domains in `domains.txt` file
$ python3 search.py
```

### Why this could be useful?
This could be useful for finding expired domains that are still being used in DNS records, so for example if there are old forgetten domains in `MX` records could be misused by attackers to send phishing emails, so it is better to find them and fix these records.

### False Positives
There could be false positives that comes usually from the `whois` so it is better to check manually if the found domain is registered or not.