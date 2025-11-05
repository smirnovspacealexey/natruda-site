from django.shortcuts import redirect
from django.urls import resolve, Resolver404
import re


class RedirectUnknownURLsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Паттерны которые НЕ должны редиректиться
        self.exclude_patterns = [
            r'^/static/',
            r'^/media/',
            r'^/admin/',
            r'^/__debug__/',
            r'^/favicon\.ico$',
        ]
        self.exclude_regexes = [re.compile(pattern) for pattern in self.exclude_patterns]

    def should_redirect(self, path):
        """Определяет, нужно ли делать редирект для этого пути"""
        # Не редиректим исключенные паттерны
        if any(regex.match(path) for regex in self.exclude_regexes):
            return False

        # Проверяем существует ли URL
        try:
            resolve(path)
            return False  # URL существует - не редиректим
        except Resolver404:
            return True  # URL не существует - редиректим

    def __call__(self, request):
        if self.should_redirect(request.path):
            return redirect('counter')

        return self.get_response(request)