"""
IO for zip/xml/csv files
"""

import threading
from Queue import Queue
from zipfile import ZipFile

XML_TEMPLATE = """<root>
</root>
"""

ZIP_FILES = 50
ZIP_THREADS = 10
XML_IN_ZIP = 100
LOG = {}


def make_zip(input_queue, thread_id):
    """ Get zip file names from input_queue and write zip file with xml files inside."""
    count = 0
    while True:
        task_id = input_queue.get()
        if task_id is None:
            break

        with ZipFile("{}.zip".format(task_id), 'w') as zfile:
            for i in range(XML_IN_ZIP):
                zfile.writestr("{}.xml".format(i), XML_TEMPLATE)

        count += 1
        input_queue.task_done()

    LOG[thread_id] = count
    input_queue.task_done()


def main():
    """Write zipz, read zips/xml, write csv."""
    queue_zip = Queue()
    for i in range(ZIP_FILES):  # fill zip file names for writing
        queue_zip.put(i)
    
    for i in range(ZIP_THREADS):  # fill terminator marks for working threads
        queue_zip.put(None)
    for i in range(ZIP_THREADS):  # run zip writers
        threading.Thread(target=make_zip, args=(queue_zip, i)).start()

    queue_zip.join()

    zips = 0
    for i in sorted(LOG.keys()):
        print "{}: {}".format(i, LOG[i])
        zips += LOG[i]

    print "Total:", zips


if __name__ == '__main__':
    main()
