from django.shortcuts import render

from recipes.utils import authenticated_user_context_update


def page_not_found(request, exception):
    """ This page informs about the absence of a page. """
    page_title = "Страница не найдена"
    context = {"page_title": page_title, "path": request.path}
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/404.html", context, status=404)


def server_error(request):
    """ This page informs about server error. """
    page_title = "Ошибка сервера"
    context = {"page_title": page_title}
    context = authenticated_user_context_update(request, context)
    return render(request, "templates/500.html", context, status=500)
