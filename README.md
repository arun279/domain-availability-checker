## Domain Availability Checker
This script checks the availability of domain names with a given word and various top-level domains (TLDs). If a domain name is available, it will be added to a file named `available_domains_for_[word].txt` and if not, it will be added to `unavailable_domains_for_[word].txt`.

## Dependencies
-  argparse
- json
- logging
- os
- time
- contextlib
- requests
- tqdm
- tqdm.contrib.concurrent
- whois
- re
- concurrent.futures

## Usage
1. Make sure you have python installed in your system
2. Install the dependencies by running the following command:
```
pip install -r requirements.txt
```
3. Run the script by using the following command:
```
python domain_availability_checker.py [word]
```
word - The word to check availability for. It can only contain lowercase alphabetical characters.

## Error Handling
Errors encountered while checking the availability of a domain name will be logged in a file named `errors.log`. The script will also retry checking the availability of a domain name for up to 2 times before moving on to the next domain name.

## TLDs
The script will first check for the existence of a file named tlds.txt in the current directory. If it exists, it will use the TLDs in that file, otherwise it will fetch a list of TLDs from the IANA website.

## Progress
The script uses the tqdm library to display the progress of checking the availability of domain names.

## Concurrency
This script uses the `concurrent.futures` library to perform the availability check of multiple domain names concurrently. The ProcessPoolExecutor is used to create a pool of worker processes that will carry out the availability check for each domain name. This allows for efficient use of system resources and faster completion of the task as multiple domain names can be checked simultaneously.