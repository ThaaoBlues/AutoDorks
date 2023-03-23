import engine as autodorks_engine


    

if __name__ == '__main__':

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
    results = vroum_vroum.search()
    






