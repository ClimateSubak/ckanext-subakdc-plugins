from datetime import datetime
import logging

from ckanext.qa.interfaces import IQaTask, IQaReport, IQaAction

log = logging.getLogger(__name__)

QA_PROPERTY_NAME = 'qa_stale'
QA_STALESNESS_THRESHOLD = 720 # in days


class QaStaleTask(IQaTask):
    qa_property_name = QA_PROPERTY_NAME
    
    @classmethod
    def evaluate(cls, pkg):
        # The `metadata_updated` attribute of both the package and resources gets updated whenever
        # the QA tasks run, so should not be used to judge staleness. This leaves the `last_modified`
        # attribute on resources as the sole method for determining if a dataset is stale (we use
        # the same logic for the freshness plugin)
        try:
            resources = pkg['resources']
        
            # No resources -> evaluate False
            if len(resources) < 1:
                return False
            
            # Find the last_modified (or created) datetimes for each resources in the package
            last_modified_dts = []
            for res in resources:
                dt = None
                datetime_format = "%Y-%m-%dT%H:%M:%S"
                if 'last_modified' in res and res['last_modified'] is not None:
                    try:
                        lm = res['last_modified'].split('.')[0] # Ignore milliseconds
                        dt = datetime.strptime(lm, datetime_format)
                    except ValueError as e:
                        log.error(f"Cannot parse resource last_modified datetime in QaStaleTask: {e}")
                        
                else:
                    try:
                        created = res['created'].split('.')[0] # Ignore milliseconds
                        dt = datetime.strptime(created, datetime_format)
                    except ValueError as e:
                            log.error(f"Cannot parse resource created datetime in QaStaleTask: {e}")
                
                if dt is not None:                 
                    last_modified_dts.append(dt)
            
            # If at least one datetime is found and the most recent datetime is older than threshold,
            # then evaluate as True
            if len(last_modified_dts) >= 1:
                last_modified_dts = sorted(last_modified_dts, reverse=True)
                age = (datetime.now() - last_modified_dts[0]).days
                
                if age > QA_STALESNESS_THRESHOLD:
                    # return { 'is_stale': True, 'age': age }
                    return True
            
            return False
                
        except Exception as e:
            log.error(f"Could not evaluate pkg in QaStaleTask: {e}")
            return False
            
            
class QaStaleReport(IQaReport):
    @classmethod
    def generate(cls):
       fields = ['id', 'title', 'num_resources']
       return cls.build(QA_PROPERTY_NAME, fields)
    
    @classmethod
    def should_show_in_report(cls, value):
        # Only show in report if value is set to true
        if value is None:
            return False
        else:
            return value
        
    @classmethod
    def get_qa_actions(cls):
        # TODO add some actions (e.g. remove dataset or set to private visibility)
        return []
    
qa_stale_report_info = {
    'name': 'stale-datasets',
    'description': 'Stale datasets',
    'option_defaults': None,
    'option_combinations': None,
    'generate': QaStaleReport.generate,
    'template': 'report/qa_stale.html'
}