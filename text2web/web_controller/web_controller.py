from selenium import webdriver

__author__ = 'shaun'


def control_web(controls):
    """
    :param controls: a list of string commands in the order of desired execution
    :return: the status of the operation as an English string as if spoken word
    """
    status = ''
    return status

driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()
