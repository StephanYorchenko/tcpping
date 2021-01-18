import sys

import ui
from domain import ResultStruct
from tcp_factory import TCPWorkerFactory

if __name__ == "__main__":
    results = ResultStruct(*ResultStruct.default_config())
    interface = ui.CLInterface.start(TCPWorkerFactory(), results)
    interface.run()
    sys.exit(0)
