import threading
from Queue import Queue

ZIP_FILES = 50
ZIP_THREADS = 10
LOG = {}


def make_zip(input_queue, thread_id):
    count = 0
    while True:
        task_id = input_queue.get()
        if task_id is None:
            break
        count += 1
        input_queue.task_done()

    LOG[thread_id] = count
    input_queue.task_done()


def main():
    queue_zip = Queue()
    for i in range(ZIP_FILES):
        queue_zip.put(i)
    for i in range(ZIP_THREADS):
        queue_zip.put(None)

    for i in range(ZIP_THREADS):
        threading.Thread(target=make_zip, args=(queue_zip, i)).start()

    queue_zip.join()

    zips = 0
    for i in sorted(LOG.keys()):
        print "{}: {}".format(i, LOG[i])
        zips += LOG[i]

    print "Total:", zips


if __name__ == '__main__':  # pragma: no cover
    main()
