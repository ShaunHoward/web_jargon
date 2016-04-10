__author__ = 'shaun'

import helpers as h
import bs4


def create_table(html, kvdict, ww=False, heading=None):
    # html is a list of html
    # kvdict is a header mapped to list of values
    first = False
    html.append("<table border=\"1\">")
    # create table header if not a wake word
    if not ww:
        html.append("<tr><th>Context: Action</th><th>Command</th>")

    for key in kvdict.keys():
        first = True
        if heading:
            html.append("<h1>" + str(heading) + "</h1>")
        vals = kvdict[key]
        if not ww:
            context = determine_action_context(key)
            html.append(''.join(["<tr><td>", context, ": ", str(key), "</td>"]))
        for val in vals:
            if not ww:
                if not first:
                    html.append("<tr><td> </td><td>" + str(val[h.CMD]))
                else:
                    html.append("<td>" + str(val[h.CMD]))
                    first = False
            else:
                html.append("<tr><td>")
                html.append(str(val))
            html.append("</td></tr>")
    # end html table
    html.append("</table>")
    return html


def start_html():
    # creates the beginning part of html list
    return ["""<!DOCTYPE html><html><head><style>
            th {
                text-align: center;
            }
            td {
                padding: 4px 4px 4px 4px;
            }
            table {
                border: 1px solid black;
            }
            </style></head><body>"""]


def end_html(html):
    # finishes end part of html list and joins contents to string
    # prettifies contents with beautiful soup 4
    html.append("</body></html>")
    html_str = ''.join(html)
    bs4_html = bs4.BeautifulSoup(html_str, "html.parser").prettify()
    return bs4_html


def determine_action_context(action_token):
    # determines which action context the given action token works in
    context = "G"
    if action_token in h.VIDEO_CONTEXT:
        context = "V"
    elif action_token in h.MUSIC_CONTEXT:
        context = "M"
    elif action_token in h.DOC_CONTEXT:
        context = "D"
    return context


def create_cheat_sheet_html_page(template_path=h.DEFAULT_ACTIONS_PATH):
    # begin html document list
    html = start_html()

    # add header info
    html.append("<h1>Web Jargon Cheat Sheet</h1>")

    # list wake words
    wws = ["Web Jargon", "web jargon", "browser", "Chrome", "chrome"]
    kvdict = {"Wake Words": wws}

    # create the wake words table
    html = create_table(html, kvdict, True, "Wake Words")

    # add the contexts
    html.append("""<h1>Action Request Usage Contexts:</h1><table border=\"1\"><tr><th>Context</th><th>Application</th></tr>
            <tr><td>General (G)</td><td>Almost all web pages (click, search, scroll, forward, backward, zoom in/out, etc.)</td></tr>
            <tr><td>Music (M)</td><td>Spotify, Pandora (play, pause, next song, search artists/songs)</td></tr>
            <tr><td>Video (V)</td><td>YouTube (play, pause, toggle fullscreen)</td></tr>
            <tr><td>Document (D)</td><td>Adobe Acrobat (search for text, go to page, zoom in/out)</td></tr></table>""")

    # load action keys and possible commands
    action_keys_and_vals = h.load_web_action_template(template_path, False)

    # add template header
    html.append("<h1>Action Command Templates</h1>")

    # create html tables of action values
    html = create_table(html, action_keys_and_vals)

    # finish up html page, prettify with bs4
    cheat_sheet = end_html(html)
    return cheat_sheet

if __name__ == '__main__':
    import os
    # create and write the cheat sheet to html page
    file_path = os.path.join(os.getcwd(), "cheat_sheet.html")
    html = create_cheat_sheet_html_page()
    try:
        print "writing file to: " + file_path
        f = open(file_path, 'w')
        f.write(html)
        f.close()
    except IOError:
        print "had issue writing file to file: " + file_path
