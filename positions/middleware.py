from positions.utils import update_positions

class UpdatePositionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        update_positions()
        response = self.get_response(request)
        return response