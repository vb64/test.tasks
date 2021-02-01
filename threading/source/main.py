"""
IO for zip/xml/csv files
"""
import threading
import random
from zipfile import ZipFile

try:
    from queue import Queue
except ImportError:
    from Queue import Queue  # Python2

LOG = {}

ZIP_FILES = 50
ZIP_THREADS = 10
XML_IN_ZIP = 100

XML_LEVEL_MIN = 1
XML_LEVEL_MAX = 100
XML_OBJECTS_MIN = 1
XML_OBJECTS_MAX = 10

XML_OBJECT_TEMPLATE = "<objectname='{}'/>"
XML_TEMPLATE = """<root>
<varname='id' value='{}'/>
<varname='level' value='{}'/>
<objects>
{}
</objects>
</root>
"""


def make_xml(zip_id, xml_num):
    """Create xml content according rules."""
    xml_id = "Z{}X{}".format(zip_id, xml_num)
    obj_range = range(random.randint(XML_OBJECTS_MIN, XML_OBJECTS_MAX))

    return XML_TEMPLATE.format(
      xml_id,
      random.randint(XML_LEVEL_MIN, XML_LEVEL_MAX),
      '\n'.join([
        XML_OBJECT_TEMPLATE.format("{}OBJ{}".format(xml_id, i)) for i in obj_range
      ])
    )


def make_zip(input_queue, thread_id):
    """Get zip file names from input_queue and write zip file with xml files inside."""
    count = 0
    while True:
        task_id = input_queue.get()
        if task_id is None:
            break

        with ZipFile("{}.zip".format(task_id), 'w') as zfile:
            for i in range(XML_IN_ZIP):
                zfile.writestr("{}.xml".format(i), make_xml(task_id, i))

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
        print("{}: {}".format(i, LOG[i]))
        zips += LOG[i]

    print("Total: {}".format(zips))


if __name__ == '__main__':
    main()
