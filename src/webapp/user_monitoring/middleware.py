from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
import os

class DatabaseCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that should be accessible even without a DB
        setup_url = reverse('setup_database')
        static_url = settings.STATIC_URL
        
        # Allow access to setup page and static files
        if request.path == setup_url or request.path.startswith(static_url):
            return self.get_response(request)

        # Check if the database file exists
        db_path = settings.DATABASES['default']['NAME']
        
        if not os.path.exists(db_path):
            # If DB is missing, force redirect to setup
            return redirect('setup_database')

        response = self.get_response(request)
        return response