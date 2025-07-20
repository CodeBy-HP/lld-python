from Handler import Handler

class ConcreteHandlerA(Handler):
    def handle_request(self,request):
        if request == 'A':
            print(f"ConcreteHandlerA handled the request {request}")
        elif self.sucessor:
            self.sucessor.handle_request(request)
        else:
            print(f"request {request} not handled")

