import os
from json import dumps, loads
import urllib
from requests import get
import urllib.request
from webbrowser import open as web_open
from re import search as re_search
import argparse
from bs4 import BeautifulSoup
from os import path, mkdir


# Output file name
output_file = 'google_dorks_search_results.txt'

# GitHub repository containing the JSON templates
json_repo_url = 'https://api.github.com/repos/thaaoblues/autodorks/contents/templates/'



# Function to download all the JSON templates from a GitHub repository
def download_json_templates(repo_url):


    with urllib.request.urlopen(repo_url) as url:

        # check if we have created the templates folder
        if not path.exists("templates"):
            mkdir("templates")

        data = loads(url.read().decode())

        for file in data:
            if file['name'].endswith('.json'):
                filename = file['name']

                url = file['download_url']
                with urllib.request.urlopen(url) as url:
                    data = url.read().decode()
                    with open(f"templates/{filename}", 'w') as f:
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


def google_search(url,headers) -> list:
    
    resp = get(url,headers=headers,cookies = {'CONSENT' : 'YES+'}).text
    soup = BeautifulSoup(resp,features="html.parser")

    results = []

    for ele in soup.find_all("h3"):
        results.append({
            "url":"",
            "title": ele.text,
            "description":"desc"
        })

    
    potential_links = soup.find_all("a",href=True)
    
    # two indexes as the list does not share the same length
    link_index = 0
    result_index = 0

    while result_index<len(results):
        
        if str(potential_links[link_index]["href"]).startswith("/url?"):
            results[result_index]["url"] = str(potential_links[link_index]["href"])

            # increments only if we find the link
            result_index += 1


        link_index += 1


    return results



# Main function
def main(args):


    print("[I] checking templates...")
    
    # Check if the JSON templates are present in the current directory
    with urllib.request.urlopen(args.repo_url) as url:


            data = loads(url.read().decode())

            # loop throught all available templates 
            # and trigger a full redownload if one is missing
            for file in data:
                if file['name'].endswith('.json'):
                    filename = file['name']
                    if not os.path.exists(f"templates/{filename}"):
                        
                        print("[I] found missing template, downloading...")

                        download_json_templates(args.repo_url)
                        break


    # check if user just want to list availables templates
    if args.list_templates:

        print(os.listdir("templates"))
        return





    # Load the selected JSON template
    with open(f"templates/{args.json_template}") as f:
        dorks = loads(f.read())


    # specific to domain-targeted dorks
    if args.url :
        # Extract the email address linked to the website
        email_address = extract_email_address(args.url)

        base_query = f"insite:{args.url}"

        report_filename = f"{os.path.splitext(args.json_template)[0]}_{args.url}.txt"
    else:
        base_query = ""
        report_filename = f"{os.path.splitext(args.json_template)[0]}_no_target.txt"
        email_address = "only available in domain-target mode"
    
    print("[I] Making request and generating report...")
    print(f"[I] Future report name : {report_filename}")

    # Generate the report file
    with open(report_filename, 'w') as f:

        f.write(f"Google Dorks Report \n\n")
        f.write(f"Email Address: {email_address}\n\n")

        for dork in dorks['dorks']:
            
            # loads dork to the query
            full_query = base_query + dork['query']

            f.write(f"\n====Query: {full_query}\n")


            #urllib.parse.urlencode()
            search_url = "https://www.google.co.in/search?q={}".format(urllib.parse.quote_plus(f"{full_query} {args.query}"))

            print(f"Search URL: {search_url}")

            f.write(f"Search URL: {search_url}\n\n")

            try:
                # function to retrieve google result
                for result in google_search(
                    search_url,
                    headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }):
                    
                    f.write(dumps(
                        {
                            "title": result["title"],
                            "url":result["url"],
                            "desc":result["description"]
                        }
                    )+"\n")

            except Exception as e:
                print("[X] Error searching for query: " + full_query+"\n"+"\t")
                print(e)

            # open in browser if optionnal arg is present
            if args.open:
                web_open(search_url)



    print(f"Report generated: {report_filename}")

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Automate Google Dorks')
    parser.add_argument('--query','-q',default='', help='The search query to use with the dorks')
    parser.add_argument('--json_template', '-t', type=str, default='commons.json', help='JSON template file containing the Google Dorks to use')
    parser.add_argument('--url', '-u', type=str, default=None, help='URL of the website to search for (optional)')
    parser.add_argument('--open', '-o', action='store_true', help='Open search results in browser (optional)')
    parser.add_argument('--repo_url', '-r', type=str, default=json_repo_url, help="URL of the GitHub repository containing the JSON templates (optional)")
    parser.add_argument('--list_templates', '-ls', action='store_true', help='List all the templates locally availables.')

    args = parser.parse_args()

    main(args)







