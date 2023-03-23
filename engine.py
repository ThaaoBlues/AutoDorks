import os
from json import dumps, loads
import urllib
from requests import get
import urllib.request
from re import search as re_search
from bs4 import BeautifulSoup
from os import path, mkdir


# GitHub repository containing the JSON templates
JSON_REPO_URL = 'https://api.github.com/repos/thaaoblues/autodorks/contents/templates/'


class EngineArguments():


    """
    a simple class to pass arguments to the engine 
    so the engine can be used in more than one context
    """

    def __init__(self,query="",json_template="",url="",repo_url=JSON_REPO_URL,list_templates=False,check_404=False) -> None:
        
        
        self.query = query
        self.json_template = json_template
        self.url = url
        self.repo_url = repo_url
        self.list_templates = list_templates
        self.check_404 = check_404


class Engine():

    def __init__(self,args:EngineArguments) -> None:
        
        
        self.args = args





    # Function to download all the JSON templates from a GitHub repository
    def download_json_templates(self):


        # check if we have created the templates folder
        if not path.exists("templates"):
            mkdir("templates")

        data = get(self.args.repo_url).json()

        for file in data:
            if file['name'].endswith('.json'):
                filename = file['name']

                url = file['download_url']
                data = get(url).text

                with open(f"templates/{filename}", 'w') as f:
                    f.write(data)




    # Function to extract the email address linked to a website
    def extract_email_address(self,url):
        try:
            html = get(url).text
            pattern = r'[\w\.-]+@[\w\.-]+'
            match = re_search(pattern, html)
            if match:
                return match.group()
            else:
                return None
        except:
            return None


    def google_search(self,url,headers) -> list:
        
        # don't forget the conset cookie to get rid of google consent prompt
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
                results[result_index]["url"] = str(potential_links[link_index]["href"]).replace("/url?esrc=s&q=&rct=j&sa=U&url=","")

                # increments only if we find the link
                result_index += 1


            link_index += 1


        return results



    # Main functionZ
    def search(self) -> list:

        # list of results that is returned, idk if it could overflow with many results x')
        returned_results = []


        print("[I] checking templates...")
        
        # Check if the JSON templates are present in the current directory

        data = get(self.args.repo_url).json()

        # loop throught all available templates 
        # and trigger a full redownload if one is missing
        for file in data:
            if file['name'].endswith('.json'):
                filename = file['name']
                if not os.path.exists(f"templates/{filename}"):
                    
                    print("[I] found missing template, downloading...")

                    self.download_json_templates(self.args.repo_url)
                    break


        # check if user just want to list availables templates
        if self.args.list_templates:

            print(os.listdir("templates"))
            return





        # Load the selected JSON template
        with open(f"templates/{self.args.json_template}") as f:
            dorks = loads(f.read())


        # specific to domain-targeted dorks
        if self.args.url :
            # Extract the email address linked to the website
            email_address = self.extract_email_address(self.args.url)

            base_query = f"insite:{self.args.url}"

            report_filename = f"{os.path.splitext(self.args.json_template)[0]}_{self.args.url}.txt"
        else:
            base_query = ""
            report_filename = f"{os.path.splitext(self.args.json_template)[0]}_no_target.txt"
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
                search_url = "https://www.google.co.in/search?q={}".format(urllib.parse.quote_plus(f"{full_query} {self.args.query}"))

                print(f"Search URL: {search_url}")

                f.write(f"Search URL: {search_url}\n\n")

                try:
                    # function to retrieve google result
                    for result in self.google_search(
                        search_url,
                        headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }):
                        if self.args.check_404:

                            # skip if 404 error returned by the link
                            if get(result["url"]).status_code == 404:
                                continue


                        returned_results.append(
                            {
                                "title": result["title"],
                                "url":result["url"],
                                "desc":result["description"]
                            }
                        )


                        f.write(dumps(
                            returned_results[-1]
                        )+"\n")

                except Exception as e:
                    print("[X] Error searching for query: " + full_query+"\n"+"\t")
                    print(e)



        print(f"Report generated: {report_filename}")


        return returned_results