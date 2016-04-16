__author__ = 'shaun'

import bs4
import helpers as h
import os


CONTEXTS = ["G", "V", "M", "D"]
skip_words = ["paws"]


def create_table(html, kvdict, ww=False, heading=None):
    """
    Creates a table in the provided html list
    Table can be created either for wake words (ww) or action command templates
    :param html: a list of html
    :param kvdict: is a header mapped to list of values
    :param ww: whether the table is created for wake words
    :param heading: the heading string above the table
    """
    first = False
    html.append("<table border=\"1\">")
    # create table header if not a wake word
    if not ww:
        html.append("<tr><th>Context: Action</th><th>Command</th>")

    for key in kvdict.keys():
        first = True
        # add heading above table
        if heading:
            html.append("<h1>" + str(heading) + "</h1>")
        vals = kvdict[key]

        # add context key to front of item if rendering action command templates
        if not ww:
            context = determine_action_context(key)
            html.append(''.join(["<tr><td>", context, ": ", str(key), "</td>"]))
        for val in vals:
            # determine if we want to print this value or skip it via skip word list
            has_stop_word = False
            if not ww:
                for skip_word in skip_words:
                    if skip_word in str(val[h.CMD]):
                        has_stop_word = True
            if has_stop_word:
                continue

            # print values if two-column table
            if not ww:
                if not first:
                    html.append("<tr><td> </td><td>" + str(val[h.CMD]))
                else:
                    html.append("<td>" + str(val[h.CMD]))
                    first = False
            else:
                # print values if one-column table
                html.append("<tr><td>")
                html.append(str(val))
            html.append("</td></tr>")
    # end html table
    html.append("</table>")
    return html


def start_html():
    # creates the beginning part of html list
    return ["""<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="help_style.css"></head><body>"""]


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


def add_context_info(html, context):
    # adds contextual info to the html help page
    html.append("<h2>You are currently browsing in the ")
    if context is "V":
        html.append("video")
    elif context is "M":
        html.append("music")
    elif context is "D":
        html.append("document")
    else:
        html.append("general")
    html.append(" context.</h2>")
    return html


def create_help_html_page(curr_context, action_dict):
    # begin html document list
    html = start_html()

    # add header info
    html.append("<h1>Web Jargon Help Page</h1>")

    # add current context info to help page
    html = add_context_info(html, curr_context)

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

    # add template header
    html.append("<h1>Available Action Commands and Templates</h1>")

    # filter commands to only those available in the current context
    filtered_action_dict = h.filter_results(action_dict, curr_context)

    # create html tables of action values
    html = create_table(html, filtered_action_dict)

    # finish up html page, prettify with bs4
    help_page = end_html(html)
    return help_page


def run_help_page_creator():
    # load action keys and possible commands
    action_dict = h.load_web_action_template(h.DEFAULT_ACTIONS_PATH, False)
    # create help pages for all contexts
    for context in CONTEXTS:
        # create and write the help page to html page
        file_path = os.path.join(os.getcwd() + "/browser_extension/html_help_pages/",
                                 '_'.join([str(context), "help_page.html"]))
        html = create_help_html_page(context, action_dict)
        try:
            print "writing file to: " + file_path
            f = open(file_path, 'w')
            html = unicode(html)
            ascii_html = html.encode('ascii', 'ignore')
            f.write(ascii_html)
            f.close()
        except IOError:
            print "had issue writing file to file: " + file_path

if __name__ == '__main__':
    run_help_page_creator()
