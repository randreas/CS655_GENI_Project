import time

class Command:
    def execute(self):
        pass
    def getResult(self):
        pass


class testCommand(Command):
    def execute(self):
        print("helloworld")

def timeTaken(command:Command):
    start_time = time.time()
    command.execute()
    return (time.time()- start_time)

print(timeTaken(testCommand()))
