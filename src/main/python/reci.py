#!/usr/bin/env python

import reci_api
import os.path
import sys
if __name__ == '__main__':
    project = os.path.basename(os.getcwd())
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "default"
    reci_api.realize(project, target, ".", ".")
