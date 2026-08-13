import threading
import asyncio
from core import *
from engine.task.condition import Condition
from engine.log import Log

CATEGORY_NAME = "TASK"

class Task:

    def __init__(self, process: Callable[[], Awaitable[Any]],
                name: str|None,
                run_for_ever: bool,
                condition: 'Condition') -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.is_finished = False
        self.run_forever = run_for_ever
        self.condition = condition
        self.return_value: Any = None

        def run() -> None:
            try:
                asyncio.set_event_loop(self.loop)
                self.return_value = self.loop.run_until_complete(process())
                if self.run_forever:
                    self.loop.run_forever()
            except Exception as exc:
                Log.FailedTrace(CATEGORY_NAME, exc)
            finally:
                self.is_finished = True

                # Gracefully drain pending tasks before closing the loop.
                # This avoids noisy "Task was destroyed but it is pending" warnings
                # when Ctrl+C interrupts long-running services.
                try:
                    pending = [t for t in asyncio.all_tasks(self.loop) if not t.done()]
                    for pending_task in pending:
                        pending_task.cancel()
                    if pending:
                        self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))

                    self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                    if hasattr(self.loop, "shutdown_default_executor"):
                        self.loop.run_until_complete(self.loop.shutdown_default_executor())
                except Exception:
                    # Never block shutdown on cleanup edge cases.
                    pass

                self.loop.close()
                self.condition.NotifyAll()

        self.thread = threading.Thread(target=run, name=name)

    def Start(self) -> None:
        self.thread.start()

    def Stop(self) -> None:
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

    def WaitFinished(self) -> None:
        def check():
            return self.is_finished
        self.condition.Wait(check)

