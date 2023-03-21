from user_accounts.utils import update_values

class UpdateValuesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        update_values()
        response = self.get_response(request)
        return response