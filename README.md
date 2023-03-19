# Google Dorks Automation
This is a Python script that automates the process of searching Google for specific information using Google Dorks.

## Usage
To use this script, run the following command:
```shell
python google_dorks.py [-h] [--json_template JSON_TEMPLATE] [--url URL] [--open] [--repo_url REPO_URL] [--template_type TEMPLATE_TYPE] [QUERY]
```

## The script takes the following arguments:

--query or -q : the actual google search you want to make (default to an emplty query, not very usefull wihtout this argument)
--json_template or -t: The JSON template file containing the Google Dorks to use (default: commons.json).
--url or -u: The URL of the website to search for (optional).
--open or -o: Open search results in browser (optional).
--repo_url or -r: The URL of the GitHub repository containing the JSON templates (optional).
--list_templates or -ls : List all the availables json dorks templates under the folder ./templates

The script generates a report file for each search, with the filename <template_type>_<website_url>.txt.

## Example
To search for documentation related to the website example.com using the documentation.json template, run the following command:

```shell
python google_dorks.py -t documentation.json -u example.com "example enterprise"
```

## JSON Templates
This script uses JSON templates to specify the Google Dorks to use for each search. The following JSON templates are available:

common.json Searches a bit of everything with commonly used google dorks
video.json: Searches for videos related to the website.
osint.json: Dorks that are mainly used for OSINT.
confidential.json: tries uncover confidential files from the website.
vulnerabilities.json: common dorks used to find vulnerabilites on a website.
sql_injection.json: template dedicated to finding sql vulnerabilities.

You can still specify an external source of templates from github by using --repo_url

Each JSON template contains a list of Google Dorks to use for the search. The query field in each dork should contain the search query, with the example.com placeholder replaced with the website URL.





