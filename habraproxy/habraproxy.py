"""
habraproxy.py — это простейший http-прокси-сервер, запускаемый локально (порт на ваше 
усмотрение), который показывает содержимое страниц Хабра. С одним исключением: после  
каждого слова из шести букв должен стоять значок «™». Примерно так:

http://habrahabr.ru/company/yandex/blog/258673/
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают проблемы и 
особенности TLS. Я хочу воспользоваться этой возможностью, чтобы поговорить об одной из 
них, а именно — о настройке ciphersiutes.

http://127.0.0.1:8232/company/yandex/blog/258673/
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают проблемы и 
особенности TLS. Я хочу воспользоваться этой возможностью, чтобы поговорить об одной из 
них, а именно™ — о настройке ciphersiutes. 

Условия:
  * Python 2.x
  * можно использовать любые общедоступные библиотеки, которые сочтёте нужным
  * чем меньше кода, тем лучше. PEP8 — обязательно
  * в случае, если не хватает каких-то данных, следует опираться на здравый смысл

Если задача кажется слишом простой, можно добавить следующее:
  * параметры командной строки (порт, хост, сайт, отличный от хабра и т.п.)
  * после старта локального сервера автоматически запускается браузер с открытой 
    обработанной™ главной страницей

Зависимостей от сторонних библиотек нет. 

Ограничения:
  * обрабатывает только GET запросы
  * не маркирует слова в тегах <script> и <code>, в комментариях и атрибутах (alt, title и т.п.)
  * не отрабатывает изменения в DOM, которые делаются из js
"""

from urllib2 import urlopen
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from HTMLParser import HTMLParser

host = "https://habrahabr.ru"
port = 8080


def insert_marks(line, offsets, mark_symbol):
    start = 0
    l = []
    for offset in offsets:
        l.append(line[start:offset])
        start = offset
    l.append(line[start:])
    return mark_symbol.join(l)


class MarkWords(HTMLParser):

    def run(
      self,
      html,
      mark_symbol=u'\u2122',
      word_length=6,
      passthrough_tags=('script', 'style', 'code',),
      non_word_chars=':;(){}[].,!?"\''
    ):
        self.passthrough_tags = passthrough_tags
        self.non_word_chars = non_word_chars
        self.word_length = word_length
        self.passthrough_flag = False
        self.marks = {}
        self.hrefs = []

        result = []
        lines = html.splitlines(True)
        if len(lines[0]) > 2:
            result.append('\n')

        # this loop is needed for correct line numbering by HTMLParser.getpos()
        for line in lines:
            self.feed(line)
        self.close()

        for key, line in enumerate(lines, start=1):
            if key in self.marks:
                line = insert_marks(line, self.marks[key], mark_symbol)
            if key in self.hrefs:
                line = line.replace(host, "http://localhost:%d" % port)

            result.append(line)

        return "".join(result)

    def handle_starttag(self, tag, attrs):
        if tag in self.passthrough_tags:
            self.passthrough_flag = True

        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and attr[1].startswith(host):
                    self.hrefs.append(self.getpos()[0])
                    break

    def handle_endtag(self, tag):
        if tag in self.passthrough_tags:
            self.passthrough_flag = False

    def handle_data(self, data):
        if self.passthrough_flag:
            return

        line, offset = self.getpos()
        start = 0
        for word in data.split():
            word = word.strip(self.non_word_chars)
            if len(word) == self.word_length:
                start = data.find(word, start) + self.word_length
                self.marks.setdefault(line, []).append(offset + start)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = urlopen("%s%s" % (host, self.path))
        data = response.read()

        content_type = ""
        for h in response.info().headers:
            if h.startswith("Content-Type"):
                key, content_type = h.rstrip().split(': ')
                break

        if 'text/html;' in content_type:
            encoding = content_type.split('charset=')[1]
            p = MarkWords()
            data = p.run(data.decode(encoding)).encode(encoding)
            count = reduce(lambda x, y: x + len(y), p.marks.values(), 0)
            print "words marked:", count

        self.send_response(response.getcode())
        self.wfile.write(data)


def main():
    print "visit http://localhost:%d/" % port
    HTTPServer(("localhost", port), Handler).serve_forever()

if __name__ == '__main__':
    main()
