import logging

import ckan.plugins.toolkit as tk

from ckanext.qa.interfaces import IQaTask, IQaProperty, IQaReport, IQaAction
from ckanext.qa.utils import merge_with_extras

log = logging.getLogger(__name__)


class QaNoResourcesTask(IQaTask):
    
    def task_job(self, user):
        # Get the required API actions
        get_packages = tk.get_action('current_package_list_with_resources')
        patch_package = tk.get_action('package_patch')
        
        # User context has to be specifically created as job doesn't have awareness of current user
        context = { 'user': user }

        # Query the API using cursor to find all packages
        page = 0
        all_pkgs = []
        while (True):
            pkgs = get_packages(context, { 'limit': 100, 'offset': page*100 })
            if len(pkgs) > 0:
                all_pkgs = all_pkgs + pkgs
                page += 1
            else:
                break
            
        for pkg in all_pkgs:
            # Run an empty patch on the package - this will trigger run_on_single_entity to be be run 
            # afterwards which does the actual work of updating the extras
            try:
                patch_package(context, { 'id': pkg['id'] })
            except Exception as e:
                log.error(f"Could not patch package: {pkg['name']}, {e}")

    def run_on_single_entity(self, entity):
        # Get the required API action
        patch_package = tk.get_action('package_patch')
        
        # Add/update QA property for each package
        pkg = entity
        extras = pkg['extras']
        extras = merge_with_extras(extras, QaNoResourcesProperty.name, 'True' if len(pkg['resources']) == 0 else 'False')
        
        try:
            patch_package(None, { 'id': pkg['id'], 'extras': extras })
        except Exception as e:
            log.error(f"Could not patch package: {pkg['name']}, {e}")
        
    def run(self):
        func = self.task_job
        user = tk.g.user
        tk.enqueue_job(func, [user])
            
        
class QaNoResourcesProperty(IQaProperty):
    name = 'qa_no_resources'

    
class QaNoResourcesReport(IQaReport):
    @classmethod
    def run_qa_task(cls):
        task = QaNoResourcesTask()
        task.run()
    
    @classmethod
    def generate(cls):
        # Run the QA task before generating the report
        # TODO as this is now scheduled job, it needs to be run seprately from the report.
        cls.run_qa_task()
        
        # Get the required API actions
        get_packages = tk.get_action('current_package_list_with_resources')
        
        # Query the API using cursor to find all packages
        page = 0
        all_pkgs = []
        while (True):
            pkgs = get_packages(None, { 'limit': 100, 'offset': page*100 })
            if len(pkgs) > 0:
                all_pkgs = all_pkgs + pkgs
                page += 1
            else:
                break
        
        # Build report table detailing packages with no resources
        report_table = []
        fields = ['id', 'title', 'num_resources']
        for pkg in all_pkgs:
            extras = pkg['extras']
            if ({ 'key': QaNoResourcesProperty.name, 'value': 'True' } in extras):
                report_table.append({ k: pkg[k] for k in fields})
                
        return {
            'table': list(report_table),
            'total_num_packages': len(all_pkgs),
        }
        
    @classmethod
    def get_qa_actions(cls):
        # TODO add some actions (e.g. remove dataset or set to private visibility)
        return []
    
qa_no_resources_report_info = {
    'name': 'datasets-with-no-resources',
    'description': 'Datasets with no resources',
    'option_defaults': None,
    'option_combinations': None,
    'generate': QaNoResourcesReport.generate,
    'template': 'report/qa_no_resources.html'
}