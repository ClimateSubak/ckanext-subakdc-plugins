import copy
import ckan.plugins as p
import logging

log = logging.getLogger(__name__)


class SearchPlugin(p.SingletonPlugin):
    p.implements(p.IFacets, inherit=True)
    p.implements(p.IPackageController, inherit=True)


    # IFacets
    def dataset_facets(self, facets_dict, package_type):    
        facets_dict['subak_countries'] = p.toolkit._('Country')
        facets_dict['subak_geo_region'] = p.toolkit._('Region')
        facets_dict['subak_temporal_start'] = p.toolkit._('Earliest Date')
        facets_dict['subak_temporal_end'] = p.toolkit._('Latest Date')
        # facets_dict['start_date'] = p.toolkit._('Start date')
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        return facets_dict