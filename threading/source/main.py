"""Ngenix test task.
(C) 2021 by Vitaly Bogomolov mail@vitaly-bogomolov.ru
"""

from threading import Thread
from random import randint
from zipfile import ZipFile
from xml.sax import ContentHandler, parseString
from csv import writer

try:
    from queue import Queue
except ImportError:
    from Queue import Queue  # Python2

ZIP_THREADS = 10

ZIP_FILES = 50
XML_IN_ZIP = 100

XML_LEVEL_MIN = 1
XML_LEVEL_MAX = 100
XML_OBJECTS_MIN = 1
XML_OBJECTS_MAX = 10

XML_OBJECT_TEMPLATE = "<object name='{}'/>"
XML_TEMPLATE = """<root>
<var name='id' value='{}'/>
<var name='level' value='{}'/>
<objects>
{}
</objects>
</root>
"""


def make_xml(zip_id, xml_num):
    """Create xml content according rules."""
    xml_id = "Z{}X{}".format(zip_id, xml_num)

    return XML_TEMPLATE.format(
      xml_id,
      randint(XML_LEVEL_MIN, XML_LEVEL_MAX),
      '\n'.join([
        XML_OBJECT_TEMPLATE.format("{}OBJ{}".format(xml_id, i))
        for i in range(randint(XML_OBJECTS_MIN, XML_OBJECTS_MAX))
      ])
    )


class NgenixXml(ContentHandler):
    """Ngenix xml sax parser."""

    def __init__(self, csv1, csv2):
        """Args csv1 and csv2 are the queues for csv rows."""
        ContentHandler.__init__(self)
        self.var_id = None
        self.csv1 = csv1
        self.csv2 = csv2

    def startElement(self, name, attrs):
        """Put parsed values to csv queues."""
        if name == 'var':
            attr_name = attrs.getValue('name')
            if attr_name == 'id':
                self.var_id = attrs.getValue('value')
            elif attr_name == 'level':
                self.csv1.put((self.var_id, attrs.getValue('value')))
        elif name == 'object':
            self.csv2.put((self.var_id, attrs.getValue('name')))


def handle_zip(mode, zip_names, csv1, csv2):
    """Get zip file names and handle according mode.
    mode must be 'w' or 'r'.
    """
    while True:
        zip_id = zip_names.get()
        if zip_id is None:
            break

        with ZipFile("{}.zip".format(zip_id), mode) as zfile:
            if mode == 'w':
                for i in range(XML_IN_ZIP):
                    zfile.writestr("{}.xml".format(i), make_xml(zip_id, i))
            else:
                parser = NgenixXml(csv1, csv2)
                for i in range(XML_IN_ZIP):
                    parser.var_id = None
                    parseString(zfile.read("{}.xml".format(i)), parser)

        zip_names.task_done()

    zip_names.task_done()


def make_csv(file_name, queue_csv):
    """Get data from queue and put to csv file."""
    fhandle = open(file_name, 'w')
    output = writer(fhandle)
    while True:
        row = queue_csv.get()
        if row is None:
            break
        output.writerow(row)
        queue_csv.task_done()

    queue_csv.task_done()
    fhandle.close()


def init_zip_queue(zip_names):
    """Fill zip file names and terminator marks for working threads."""
    for i in range(ZIP_FILES):
        zip_names.put(i)
    for _ in range(ZIP_THREADS):
        zip_names.put(None)


def main():
    """Write zips, read zips/xml, write csv."""
    zip_names = Queue()

    print("Step 1: Create zip files.")
    init_zip_queue(zip_names)

    for _ in range(ZIP_THREADS):
        Thread(target=handle_zip, args=('w', zip_names, None, None)).start()
    zip_names.join()

    print("Step 2: Create csv files.")
    init_zip_queue(zip_names)
    csv1 = Queue()
    csv2 = Queue()

    for _ in range(ZIP_THREADS):
        Thread(target=handle_zip, args=('r', zip_names, csv1, csv2)).start()

    Thread(target=make_csv, args=('1.csv', csv1)).start()
    Thread(target=make_csv, args=('2.csv', csv2)).start()

    zip_names.join()  # wait for all zips handled

    csv1.put(None)
    csv2.put(None)
    csv1.join()
    csv2.join()


if __name__ == '__main__':
    main()
