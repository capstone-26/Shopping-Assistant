from .views import *
from django.shortcuts import redirect
from django.contrib.auth import logout
from datetime import datetime, timedelta
import json

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            current_time = datetime.now()

            if last_activity_str:
                last_activity = datetime.fromisoformat(json.loads(last_activity_str))
                idle_duration = timedelta(seconds=600) # Set the idle duration in seconds
                if (current_time - last_activity) > idle_duration:
                    del request.session['last_activity']
                    
                    return redirect(SignOut)
            else:
                request.session['last_activity'] = json.dumps(current_time.isoformat())
            
                
        request.session['last_activity'] = json.dumps(datetime.now().isoformat())
        response = self.get_response(request)
        return response