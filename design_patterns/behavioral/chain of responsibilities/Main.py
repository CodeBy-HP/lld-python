from ConcreteHandlerA import ConcreteHandlerA
from ConcreteHandlerB import ConcreteHandlerB
from ConcreteHandlerC import ConcreteHandlerC


def run():
    concrete_handler_c = ConcreteHandlerC()
    concrete_handler_b = ConcreteHandlerB(concrete_handler_c)
    concrete_handler_a = ConcreteHandlerA(concrete_handler_b)

    requests = ['A','B','C','D']

    for request in requests:
        concrete_handler_a.handle_request(request)
    


if __name__ == '__main__':
    run()