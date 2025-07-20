from Handler import Handler

class ConcreteHandlerC(Handler):
    def handle_request(self,request):
        if request == 'C':
            print(f"ConcreteHandlerC handled the request {request}")
        elif self.sucessor:
            self.sucessor.handle_request(request)
        else:
            print(f"request {request} not handled")