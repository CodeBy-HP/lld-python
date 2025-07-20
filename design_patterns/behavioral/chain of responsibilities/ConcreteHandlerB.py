from Handler import Handler

class ConcreteHandlerB(Handler):
    def handle_request(self,request):
        if request == 'B':
            print(f"ConcreteHandlerB handled the request {request}")
        elif self.sucessor:
            self.sucessor.handle_request(request)
        else:
            print(f"request {request} not handled")