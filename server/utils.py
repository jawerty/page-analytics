from functools import partial
import time
import threading
import _globals
from typing import Callable
from functools import partial
def runJob(frequency: int, callback: Callable, waitingMessage: str = None, ): 
    if _globals.lockProcess:
        while _globals.lockProcess:
            time.sleep(1)
            if waitingMessage is not None:
                print(waitingMessage) 
    
    _globals.lockProcess = True
    runJobPartial = partial(runJob, frequency, callback, waitingMessage)
    threading.Timer(frequency, runJobPartial).start()        
    callback() #runs immediately as well
    _globals.lockProcess = False
    