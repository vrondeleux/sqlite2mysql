# -*- coding: UTF-8 -*-
from distutils.core import setup

setup(name="sqlitetomysql",
      version = u"0.1",
      py_modules = ["sqlitetomysql"],
      description = u"Export Sqlite database file to Mysql database",
      author = u"Vincent Rondeleux",
      author_email = u"vincent.rondeleux@yahoo.fr",
      maintainer = u"Vincent Rondeleux",
      maintainer_email = u"vincent.rondeleux@gmail.com",
      url= u"http://floretinteractive.fr/", 
      download_url = u"http://floretinteractive.fr/downloads/sqlite2mysql",# A confirmer quand la page sera créée.
      packages=['sqlite2mysql'],
      package_dir={'sqlite2mysql': 'src/sqlite2mysql'},
      data_files = [ ("text", ["README.txt"]),]
)