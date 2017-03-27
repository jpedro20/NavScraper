
import sys
import requests
from lxml import html


def parse_navbar_ul(ul_tree):
    """
    Get all <li> items from an unordered list.
    """
    menu_items = []

    for list_item in ul_tree.xpath('./li'):
        link_item = list_item.xpath('./a/text()')
        submenu_items = []

        # This menu link has a submenu
        if "dropdown" in list_item.classes:
            submenu_items = list_item.xpath('./ul[contains(@class, "dropdown-menu")]/li/a/text()')

        if len(link_item) == 1:
            menu_items.append((link_item[0].strip(), submenu_items))

    return menu_items


def parse_navbar_page(html_tree):
    """
    Get all navbar menu links from HTML page.
    """
    menu_items = []

    menu_count = 1
    page_menus = html_tree.xpath('//nav[contains(@class, "navbar")]')
    for menu in page_menus:
        menu_lists = menu.xpath('.//ul[contains(@class, "nav")]')
        current_menu_lists = []

        for menu_list in menu_lists:
            list_items = parse_navbar_ul(menu_list)
            current_menu_lists.extend(list_items)

        menu_items.append(('menu' + str(menu_count), current_menu_lists))
        menu_count += 1

    return menu_items


def nav_scraper(http_url):
    """
    The main entry point for the program.
    """
    try:
        page = requests.get(http_url, timeout=5.0)
        page.raise_for_status()

        html_tree = html.fromstring(page.content)
        menu_links = parse_navbar_page(html_tree)

        print menu_links
    except requests.exceptions.Timeout:
        print >> sys.stderr, 'Request timed out. (timeout=5.0)'
    except requests.exceptions.RequestException as ex:
        print >> sys.stderr, ex.message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: navscraper.py http[s]://<web_url>')

    nav_scraper(sys.argv[1])
