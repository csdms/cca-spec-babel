#! /usr/bin/env python
import sys

from distutils.core import setup
# for py 2.3, we may have to import from a local copy of the
# current distutils for 2.3 which supports package_data
# but is not widely packaged in 2.3-bearing versions of linux.


verbose=1

import os

########################## main setup ######################

doc_files = []
for f in os.listdir('doc'):
    if f.endswith('.html'): doc_files.append('doc',f)

mydist = setup (name = "ccautil", version = "0.1",
       description = "CCA xml component installation description generator",
       url="https://www.cca-forum.org/bugs/cca-spec-bugs",
       author="Ben Allan",
       author_email="bocca-dev@cca-forum.org",
       packages = ['ccaxml2','ccagm'],
       scripts = ['ccaxml2/genccaxml', 'ccaxml2/queryccaxml', 'ccagm/gen-cca-main' ]
# data_files=[('share/doc', doc_files)]
      )
