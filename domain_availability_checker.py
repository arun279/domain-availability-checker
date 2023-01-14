import argparse
import json
import logging
import os
import time
import contextlib
import requests
from tqdm import tqdm as tqdm_lib
from tqdm.contrib.concurrent import process_map
import whois
import re
from concurrent.futures import ProcessPoolExecutor, as_completed

def get_tlds():
    """Fetch TLDs from file or ICANN"""
    if os.path.exists("tlds.txt"):
        with open("tlds.txt", "r") as file:
            tlds = file.read().lower().split("\n")
    else:
        response = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
        tlds = response.text.lower().split("\n")
    return tlds

def is_available(whois_info):
    """Check if all fields in the whois info are null"""
    whois_json = json.dumps(whois_info)
    return all(val is None for val in json.loads(whois_json).values())

def check_availability(word, tld):
    """Check the availability of a domain name with the given word and TLD."""
    domain = word + "." + tld
    for i in range(3):
        try:
            with open("errors.log", "w") as f, contextlib.redirect_stdout(f):
                whois_info = whois.whois(domain)
            if is_available(whois_info):
                with open(f"available_domains_for_{word}.txt", "a") as file:
                    file.write(f"{domain}\n")
                break
            else:
                with open(f"unavailable_domains_for_{word}.txt", "a") as file:
                    file.write(f"{domain}\n")
                break
        except Exception as e:
            if i < 2:
                time.sleep(5)
            else:
                logging.error(f"Error occured while checking availability of {domain}: {e}")
                continue

def find_unchecked_domains(word: str):
    with open("tlds.txt", "r") as file:
        tlds_set = set(tld.lower() for tld in file.read().split("\n"))
    with open(f"available_domains_for_{word}.txt", "r") as file:
        available_domains = set(domain.lower() for domain in file.read().split("\n"))
    with open(f"unavailable_domains_for_{word}.txt", "r") as file:
        unavailable_domains = set(domain.lower() for domain in file.read().split("\n"))
    available_tlds = available_domains | unavailable_domains
    extracted_tlds = set()
    for tld in available_tlds:
        extracted_tlds.add(tld.split('.')[-1])
    unchecked_domains = tlds_set - extracted_tlds
    with open("unchecked_domains.txt", "w") as file:
        file.write("\n".join(unchecked_domains))


def main(word: str):
    if re.match("^[a-z]+$", word) is None:
        raise ValueError("The word can only contain lowercase alphabetical characters")
    tlds = get_tlds()
    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(check_availability, word, tld) for tld in tlds[1:]]
        for f in tqdm_lib(as_completed(futures), total=len(tlds)):
            pass
    find_unchecked_domains(word)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str, help="The word to check availability for")
    args = parser.parse_args()
    try:
        main(args.word)
    except ValueError as e:
        print(e)
