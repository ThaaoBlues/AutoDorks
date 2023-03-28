import engine as autodorks_engine
from webui import webui


def build_html(results):

    page_content = "<html>"


    for ele in results:

        page_content += "<h3><a href='{}'>{}</a></h3>".format(ele["url"],ele["title"])

    page_content += "</html>"
    
    return page_content

if __name__ == '__main__':

    gui_handler = webui.window()


    # a simple class to pass arguments to the engine 
    # so the engine can be used in more than one context
    args = autodorks_engine.EngineArguments(
        query="grand theft auto",
        json_template="game_cracks.json",
        check_404=False
        )
    
    # create an instance of the engine
    vroum_vroum = autodorks_engine.Engine(args)

    # start the motor and make a lot of noises
    results = vroum_vroum.search()

    gui_handler.show(build_html(results))
    webui.wait()


    






