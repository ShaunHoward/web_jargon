__author__ = 'shaun'

import helpers as h
import bs4


def create_cheat_sheet_html_page(template_path=h.DEFAULT_ACTIONS_PATH):
    html = ["<!DOCTYPE html><html><body>"]
    action_keys_and_vals = h.load_web_action_template(template_path, False)
    # create html table of actions and values

    for key in action_keys_and_vals.keys():
        html.append("<h1>" + str(key) + "</h1>")
        vals = action_keys_and_vals[key]
        html.append("<table border=\"1\">")
        for val in vals:
            html.append("<tr><td>" + str(val[h.CMD]) + "</td></tr>")
        # end html table
        html.append("</table>")
    html.append("</body></html>")
    html_str = ''.join(html)
    bs4_html = bs4.BeautifulSoup(html_str).prettify()
    return bs4_html

if __name__ == '__main__':
    import os
    # create and write the cheat sheet to html page
    file_path = os.path.join(os.getcwd(), "cheat_sheet.html")
    html = create_cheat_sheet_html_page()
    try:
        print file_path
        f = open(file_path, 'w')
        f.write(html)
        f.close()
    except IOError:
        print "had issue writing file to file: " + file_path
