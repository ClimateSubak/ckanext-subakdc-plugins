import ckan.plugins as p
import ckan.plugins.toolkit as toolkit


class SearchPlugin(p.SingletonPlugin):
    p.implements(p.IFacets)
    p.implements(p.ITemplateHelpers)

    # Ifacets
    def dataset_facets(self, facets_dict, package_type):    
        facets_dict['countries'] = p.toolkit._('Countries')
        facets_dict['start_date'] = p.toolkit._('Start date')
        return facets_dict

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'subakdc_plugins')
