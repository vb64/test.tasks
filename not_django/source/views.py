from not_django import Response, render


def not_implemented(request):
    return Response(body="Not implemented yet")


def comment_list(request):
    return Response(body=render('list.html'))


def comment_new(request):
    return Response(body=render('comment.html'))


def statistic(request):
    return Response(body=render('stat.html'))


def root(request):
    return Response(body=render('root.html'))


urls = {
  'GET': {
    'static': {
      '/': root,
      '/comment/': comment_new,
      '/view/': comment_list,
      '/stat/': statistic,
    },
    'dynamic': [
      ('/stat/[0-9]+/$', not_implemented),
      ('/ajax/region/[0-9]+/$', not_implemented),
    ]
  },
  'POST': {
    'static': {
      '/comment/': not_implemented,
      '/view/': not_implemented,
    },
  },
}
