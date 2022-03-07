import json
import logging

import ckan.plugins.toolkit as tk

from ckanext.qa.interfaces import IQaTask, IQaProperty, IQaReport, IQaAction
from ckanext.qa.utils import merge_with_extras, should_patch_entity, get_all_pkgs

log = logging.getLogger(__name__)

class QaNoResourcesTask(IQaTask):
    def task_job(self):
        # Get all packages and associated resources
        pkgs = get_all_pkgs()
        
        # Get the required API actions
        patch_package = tk.get_action('package_patch')
    
        for pkg in pkgs:
            # Run an empty patch on the package - this will trigger run_on_single_entity to be be run 
            # afterwards which does the actual work of updating the extras
            try:
                patch_package({ 'ignore_auth': True, 'user': None }, 
                              { 'id': pkg['id'] })
            except Exception as e:
                log.error(f"Could not patch package: {pkg['name']}, {e}")

    def run_on_single_entity(self, entity):
        # Get the required API actions
        patch_package = tk.get_action('package_patch')
        show_package = tk.get_action('package_show')
        
        # Add/update QA property for each package
        pkg = show_package({ 'ignore_auth': True, 'user': None }, 
                           { 'id': entity['id'] })
        log.debug(entity) # Doesn't have resources
        
        qa = {}
        try:
            qa = json.loads(entity['subak_qa'])
            if qa is None:
                qa = {}
        except Exception as e:
            log.debug(e)
        
        log.debug(qa)
        
        # True if no resources, False if 1 or more resources
        qa_key = QaNoResourcesProperty.name
        qa_value = len(pkg['resources']) == 0
        
        # If qa key/value hasn't changed, don't patch the package again,
        # otherwise we end up in an endless loop
        if should_patch_entity(qa, qa_key, qa_value):
            qa[qa_key] = qa_value
            log.debug(qa)
            
            try:
                patch_package({ 'ignore_auth': True, 'user': None }, 
                            { 'id': pkg['id'], 'subak_qa': json.dumps(qa) })
            except Exception as e:
                log.error(f"Could not patch package: {pkg['name']}, {e}")
        
    def run(self):
        func = self.task_job
        tk.enqueue_job(func)
            
        
class QaNoResourcesProperty(IQaProperty):
    name = 'qa_no_resources'

    
class QaNoResourcesReport(IQaReport):
    @classmethod
    def generate(cls):
        # Get all packages
        pkgs = get_all_pkgs()
        
        # Build report table detailing packages with no resources
        report_table = []
        fields = ['id', 'title', 'num_resources']
        for pkg in pkgs:
            if 'subak_qa' in pkg:
                if QaNoResourcesProperty.name in pkg['subak_qa'] and pkg['subak_qa'][QaNoResourcesProperty.name]:
                    report_table.append({ k: pkg[k] for k in fields})
                
        return {
            'table': list(report_table),
            'total_num_packages': len(pkgs),
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