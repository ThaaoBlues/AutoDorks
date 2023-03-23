import argparse
import engine as autodorks_engine

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Automate Google Dorks')
    parser.add_argument('--query','-q',default='', help='The search query to use with the dorks')
    parser.add_argument('--json_template', '-t', type=str, default='commons.json', help='JSON template file containing the Google Dorks to use')
    parser.add_argument('--url', '-u', type=str, default=None, help='URL of the website to search for (optional)')
    parser.add_argument('--open', '-o', action='store_true', help='Open search results in browser (optional)')
    parser.add_argument('--repo_url', '-r', type=str, default=autodorks_engine.JSON_REPO_URL, help="URL of the GitHub repository containing the JSON templates (optional)")
    parser.add_argument('--list_templates', '-ls', action='store_true', help='List all the templates locally availables.')
    parser.add_argument('--check_404', '-c4', action='store_true', help='Will test each link and not add the ones returning 404. (slower)')

    args = parser.parse_args()

    
    # a simple class to pass arguments to the engine 
    # so the engine can be used in more than one context
    args = autodorks_engine.EngineArguments(
        query=args.query,
        json_template=args.json_template,
        url=args.url,
        repo_url=args.repo_url,
        list_templates=args.list_templates,
        check_404=args.check_404
        )
    
    # create an instance of the engine
    vroum_vroum = autodorks_engine.Engine(args)

    # start the motor and make a lot of noises
    vroum_vroum.search()






