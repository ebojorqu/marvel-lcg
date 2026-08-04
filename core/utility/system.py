import os

class System:

    @staticmethod
    def Run(cmd: str):
        os.system(cmd)

    @staticmethod
    def SetTitle(title: str):
        if os.name == 'nt':
            System.Run(f'title {title}')
        else:
            # ANSI escape sequence for terminal title on Unix-like systems.
            print(f'\33]0;{title}\a', end='')

    @staticmethod
    def Pause():
        System.Run('pause')

    @staticmethod
    def Sleep(secs: float):
        from time import sleep
        return sleep(secs)

