import sys
import os
import unittest

if __name__ == '__main__':

    sys.path.insert(1, os.path.join('..', 'source'))
    verbose = 1
    suite = None
    loader = unittest.TestLoader()
    buf = True

    if "verbose" in sys.argv:
        verbose = 2

    if (len(sys.argv) > 2) and (sys.argv[2] not in ["verbose"]):
        suite = loader.loadTestsFromNames([sys.argv[2]])
        buf = False
    else:
        suite = loader.discover('.')

    sys.exit(
      0 if unittest.TextTestRunner(verbosity=verbose, buffer=buf).run(suite).wasSuccessful() else 1
    )
