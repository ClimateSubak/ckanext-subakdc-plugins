from abc import ABC, abstractmethod

class IQaTask(ABC):
    """
    A task that operates over all or a subset of entities and produces a QA property for each entity e.g. A “broken links” task to test all links associated with a dataset
    """
    
    @abstractmethod
    def run(self):
        """
        Runs a QA task over all entities (consider running the contents of this function in a queue, e.g. tk.enqueue_job(job_func))
        """
        pass
    
    @abstractmethod
    def run_on_single_entity(self, entity_id):
        """
        Run the QA task on a single entity
        """
        pass
        
        
class IQaProperty(ABC):
    """
    A record in the entity’s extra table/field prefixed with qa_. This stores the result of the QA task output. e.g. qa_broken_links stores a dict of links that the “broken links” task identified
    """
    pass


class IQaReport(ABC):
    """
    A tabular report generated with the ckanext-report plugin that gathers the QA property for all entities for a given QA task. e.g. Details a summary of all entities with 'Broken links'
    """
    
    @classmethod
    @abstractmethod
    def generate(self):
        pass
    
    @classmethod
    @abstractmethod
    def get_qa_actions(self):
        pass


class IQaAction(ABC):
    """
    An action that can be taken using information in the QA report to modify the entities for a given QA task. e.g. Remove the links, or mark the datasets as 'stale'. A QA action should also be able to be run from the command line as a ckan command
    """
    
    @abstractmethod
    def run(self):
        pass