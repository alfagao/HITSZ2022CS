from wy163_crawler import crawler
from data_wash import dispose
from datastore import store
import os

if __name__ == '__main__':
    crawler()
    dispose()
    store()
    os.system("pause")
