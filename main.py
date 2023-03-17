import os
import json
import urllib
from requests import get
import urllib.request
from googlesearch import search
from webbrowser import open as web_open
from re import search as re_search
import argparse

# Output file name
output_file = 'google_dorks_search_results.txt'

# GitHub repository containing the JSON templates
json_repo_url = 'https://api.github.com/repos/thaooblues/autodorks/contents/json'



# Function to download all the JSON templates from a GitHub repository
def download_json_templates(repo_url):


    with urllib.request.urlopen(repo_url) as url:


        data = json.loads(url.read().decode())

        for file in data:
            if file['name'].endswith('.json'):
                filename = file['name']

                url = file['download_url']
                with urllib.request.urlopen(url) as url:
                    data = url.read().decode()
                    with open(filename, 'w') as f:
                        f.write(data)

# Setup function to download JSON templates from the GitHub repository
def setup():
    print("Downloading JSON templates from GitHub repository...")
    #download_json_templates(json_repo_url)
    print("Done.")





# Function to extract the email address linked to a website
def extract_email_address(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode()
            pattern = r'[\w\.-]+@[\w\.-]+'
            match = re_search(pattern, html)
            if match:
                return match.group()
            else:
                return None
    except:
        return None





# Main function
def main(args):


    print("[I] checking templates...")
    
    # Check if the JSON templates are present in the current directory
    with urllib.request.urlopen(args.repo_url) as url:


            data = json.loads(url.read().decode())

            # loop throught all available templates 
            # and trigger a full redownload if one is missing
            for file in data:
                if file['name'].endswith('.json'):
                    filename = file['name']
                    if not os.path.exists(filename):
                        
                        print("[I] found missing template, downloading...")

                        download_json_templates(args.repo_url)
                        break



    # Load the selected JSON template
    with open(args.json_template) as f:
        dorks = json.load(f)


    # specific to domain-targeted dorks
    if args.url :
        # Extract the email address linked to the website
        email_address = extract_email_address(args.rl)

        query = f"insite:{args.url}"

        report_filename = f"{os.path.splitext(args.json_template)[0]}_{args.url}.txt"
    else:
        query = ""
        report_filename = f"{os.path.splitext(args.json_template)[0]}_no_target.txt"
    
    
    print("[I] Making request and generating report...")
    print(f"[I] Future report name : {report_filename}")

    # Generate the report file
    with open(report_filename, 'w') as f:

        f.write(f"Google Dorks Report for {url}\n\n")
        f.write(f"Email Address: {email_address}\n\n")

        for dork in dorks['dorks']:
            
            # loads dork to the query
            query += dork['query']

            f.write(f"Query: {query}\n")

            search_url = f"https://www.google.com/search?q={query}"

            f.write(f"Search URL: {search_url}\n\n")

            try:
                for result in search(query, num_results=10):
                    f.write(result+"\n")

            except Exception as e:
                print("[X] Error searching for query: " + query)


            # open in browser if optionnal arg is present
            if args.open:
                web_open(search_url)



    print(f"Report generated: {report_filename}")

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Automate Google Dorks')
    parser.add_argument('--json_template', '-t', type=str, default='commons.json', help='JSON template file containing the Google Dorks to use')
    parser.add_argument('--url', '-u', type=str, default=None, help='URL of the website to search for (optional)')
    parser.add_argument('--open', '-o', action='store_true', help='Open search results in browser (optional)')
    parser.add_argument('--repo_url', '-r', type=str, default=json_repo_url, help="URL of the GitHub repository containing the JSON templates (optional)")
    parser.add_argument('--list-templates', '-ls', type=str, help='List all the templates locally availables.')

    args = parser.parse_args()

    main(args)







