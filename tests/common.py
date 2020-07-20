"""Several utils for testing."""
import in_place
from threading import RLock
from collections import defaultdict
from precogs.toolbox.thread import threaded


def change_configuration_file_nt(filename, term, repl):
    """Replace in place."""

    with in_place.InPlace(filename) as inplacefile:
        for line in inplacefile:
            raplaced = line.replace(term, repl)
            inplacefile.write(raplaced)


@threaded
def change_configuration_file(filename, term, repl):
    """Replace in place."""

    return change_configuration_file_nt(filename, term, repl)


class LoggerHooks:  # noqa
    def __init__(self):  # noqa
        self.count_pc = 0
        self.predict_binary = {'good': 0, 'bad': 0, 'skipped': 0}
        self.predict_installer = {1: 0, 0: 0, 'skipped': 0}
        self.installer = 0
        self.lock = RLock()


class Hooks:  # noqa
    def __init__(self, metric):  # noqa
        self.metric = metric

    def on_process_created_reduced(self, node):
        # with self.metric.lock:
        self.metric.count_pc += 1
        self.metric.predict_binary[node.binary['prediction']] += 1
        self.metric.predict_installer[node.installer['prediction']] += 1
        if node.installer['prediction'] != "skipped":
            # _prediction = "installer" if node.installer[
            #     'prediction'] == 1 else "not_installer"
            if "installer" == node.installer['prediction']:
                self.metric.installer += 1
            # try:
            #     a = node.ctx['processName']
            # except Exception:
            #     assert False


class ProducerMockCounter:
    def __init__(self, config):
        self.calls = defaultdict(int)
        self.route = int(config["service.classifier.number_of_routes"])

    def produce(self, topic, datum):
        topic = int(topic, 16) % self.route
        self.calls[topic] += 1

    def flush(self):
        pass
