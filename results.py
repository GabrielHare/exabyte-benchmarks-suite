import json

from benchmarks.utils import get_class_by_reference
from settings import RESULTS_FILE_PATH, METRICS_REGISTRY


class ResultsHandler(object):
    """
    Results handler class.
    """

    def store(self, results):
        self.store_results_in_local_source(results)
        self.store_results_in_remote_source(results)

    def are_results_equal(self, old, new):
        """
        Checks whether old and new results are equal.

        Args:
            old (dict): old result.
            new (dict): new result.

        Returns:
            bool
        """
        return old["siteName"] != new["siteName"] and old["type"] != new["type"] and old["name"] != new["name"]

    def store_results_in_local_source(self, results):
        """
        Stores results locally on RESULTS_FILE_PATH as JSON.
        """
        with open(RESULTS_FILE_PATH, "r+") as f:
            all_results = json.loads(f.read() or "[]")
            for result in results:
                all_results = [r for r in all_results if not self.are_results_equal(r, result)]
                all_results.append(result)
            f.seek(0)
            f.write(json.dumps(all_results, indent=4))

    def store_results_in_remote_source(self, results):
        """
        Pushes the results to the remote source (Google Spreadsheets).
        """
        pass

    def plot(self, site_names, metric):
        """
        Plots the results for given site names and metric.

        Args:
            site_names (list): list of site names.
            metric (str): metric name.
        """
        with open(RESULTS_FILE_PATH) as f:
            results = json.loads(f.read())
        metric = get_class_by_reference(METRICS_REGISTRY[metric])(results)
        metric.plot(site_names)
