def get_html(html_type, i):
    if html_type == "base":
        html_string = open("graph/templates/index/ajax_graph_component.html").read()
        return html_string.replace("{i}", str(i))
    # add new html strings for other html components

