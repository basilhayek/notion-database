import logging
import os
import pprint
import time

from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties, Children
from notion_database.search import Search

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NOTION_KEY = os.getenv('NOTION_KEY')

def main():


    # List Database
    logger.debug("List Database")
    S = Search(integrations_token=NOTION_KEY)
    S.search_dbs()

    print(S.result)

    for i in S.result["results"]:
        database_id = i["id"]
        logger.debug(database_id)
        run_retrieve_suite(database_id)

def run_retrieve_suite(database_id):
    logger.debug("** Retrieve suite")
    D = Database(integrations_token=NOTION_KEY)
    D.retrieve_database(database_id=database_id)
    print(D.result)    


def run_full_suite(database_id):
    # Retrieve Database
    logger.debug("Retrieve Database")
    D = Database(integrations_token=NOTION_KEY)
    D.retrieve_database(database_id=database_id)

    PROPERTY = Properties()
    PROPERTY.set_title("name", "title")
    PROPERTY.set_rich_text("description", "notion-datebase")
    PROPERTY.set_number("number", 1)
    PROPERTY.set_select("select", "test1")
    PROPERTY.set_multi_select("multi_select", ["test1", "test2"])
    PROPERTY.set_multi_select("multi_select2", ["test1", "test2", "test3"])
    PROPERTY.set_checkbox("checkbox", True)
    PROPERTY.set_url("url", "www.google.com")
    PROPERTY.set_email("email", "test@test.com")
    PROPERTY.set_phone_number("phone", "010-0000-0000")

    children = Children()
    children.set_body("hello world!")

    # Create Page
    logger.debug("Create Page")
    P = Page(integrations_token=NOTION_KEY)
    P.create_page(database_id=database_id, properties=PROPERTY, children=children)

    # Retrieve Page
    logger.debug("Retrieve Page")
    page_id = P.result["id"]
    logger.debug(page_id)
    P.retrieve_page(page_id=page_id)

    PROPERTY.clear()
    PROPERTY.set_title("name", "Custom_title")
    PROPERTY.set_rich_text("description", "Custom_description")
    PROPERTY.set_number("number", 2)

    # Update Page
    logger.debug("Update Page")
    P.update_page(page_id=page_id, properties=PROPERTY)

    time.sleep(1)
    # Archive Page
    logger.debug("Archive Database")
    P.archive_page(page_id=page_id, archived=True)

    time.sleep(1)
    # Un-Archive Page
    logger.debug("Un-Archive Database")
    P.archive_page(page_id=page_id, archived=False)

    # Create Database
    logger.debug("Create Database")

    PROPERTY = Properties()
    PROPERTY.set_title("child_name")
    PROPERTY.set_rich_text("child_description")
    PROPERTY.set_number("child_number")
    PROPERTY.set_select("child_select")
    PROPERTY.set_multi_select("child_multi_select")
    PROPERTY.set_multi_select("child_multi_select2")
    PROPERTY.set_checkbox("child_checkbox")
    PROPERTY.set_url("child_url")
    PROPERTY.set_email("child_email")
    PROPERTY.set_phone_number("child_phone")
    D.create_database(page_id=page_id, title="TEST TITLE", properties=PROPERTY)

    # Finding all pages in a database
    D.find_all_page(database_id=database_id)
    pprint.pprint(D.result)

    # D.run_query_database(database_id=database_id, body={})

if __name__ == "__main__":
    main()