#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2013-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

#from django.db import models
from django.contrib.gis.db import models # For GeoDjango.
import hashlib

class SpeciesObs(models.Model):
    """ Database table definition for species observations. 
        These observations are mostly extracted from environmental monitoring data.
    """
    # DarwinCore id for observation. MD5 value generated by us.
    occurrence_id = models.CharField(max_length=32, primary_key=True)
    status = models.CharField(max_length=10) # ACTIVE or DELETED
    last_update_date = models.CharField(max_length=10)
    last_status_change_date = models.CharField(max_length=10)
    #
    data_type = models.CharField(max_length=31)
    scientific_name = models.CharField(max_length=255, db_index=True)
    scientific_authority = models.CharField(max_length=255)
    latitude_dd = models.CharField(max_length=31)
    longitude_dd = models.CharField(max_length=31)
    sampling_date = models.CharField(max_length=10)
    sampling_year = models.CharField(max_length=4, db_index=True)
    sampling_month = models.CharField(max_length=2)
    sampling_day = models.CharField(max_length=2)
    sample_min_depth = models.CharField(max_length=31)
    sample_max_depth = models.CharField(max_length=31)
    sampler_type = models.CharField(max_length=255)
    dyntaxa_id = models.CharField(max_length=31)
    taxon_kingdom = models.CharField(max_length=127, db_index=True)
    taxon_phylum = models.CharField(max_length=127, db_index=True)
    taxon_class = models.CharField(max_length=127, db_index=True)
    taxon_order = models.CharField(max_length=127, db_index=True)
    taxon_family = models.CharField(max_length=127, db_index=True)
    taxon_genus = models.CharField(max_length=127, db_index=True)
    taxon_species = models.CharField(max_length=127, db_index=True)
    orderer = models.CharField(max_length=1023)
    reporting_institute = models.CharField(max_length=1023)
    sampling_laboratory = models.CharField(max_length=1023)
    analytical_laboratory = models.CharField(max_length=1023)
    # Datset info.
    dataset_name  = models.CharField(max_length=255, db_index=True)
    dataset_file_name  = models.CharField(max_length=255)
    # GeoDjango:Override the default manager with a GeoManager instance.
    geometry = models.PointField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()    

    def calculateDarwinCoreObservationIdAsMD5(self):
        """ Calculates DarwinCore Observation Id. It is based on fields that makes the observation unique
            and a MD5 hash value is calculated based on that unique content.
            This strategy is useful because an observation id does no exists in our datasets and this will work
            when the same data is imported multiple times by producing the same id. It will also work if
            the observation is resubmitted in another dataset or with other corrections made to aditional data.  
        """
        tmp_id = self.data_type + u'+' + \
                 self.sampling_date + u'+' + \
                 self.latitude_dd + u'+' + \
                 self.longitude_dd + u'+' + \
                 self.scientific_name + u'+' + \
                 self.sample_min_depth + u'+' + \
                 self.sample_max_depth
        # Generates MD5 string of 32 hex digits.
        md5_id = u'MD5 not calculated'
        try:
            md5_id = hashlib.md5(tmp_id).hexdigest()
        except:
            md5_id = u'ERROR in MD5 generation.'
        #
        return md5_id

    def __unicode__(self):
        return self.data_type + u' ' + \
               self.sampling_date + u' ' + \
               self.latitude_dd + u' ' + \
               self.longitude_dd + u' ' + \
               self.scientific_name

    class Meta:
        ordering = ["occurrence_id"]




# class OccurrenceIdHistory(models.Model):
#     """ Database table definition for history of species observations. 
#         Addition date and deletion date is stored for each observation id.
#         This is needed since GBIF wants to know what is added and what is 
#         deleted when BIF data is updated.
#         State: 
#     """
#     #
#     generated_occurrence_id = models.CharField(max_length=32, primary_key=True)
#     state = models.CharField(max_length=10)
#     added_date = models.CharField(max_length=10)
#     deleted_date = models.CharField(max_length=10)
# 
#     def __unicode__(self):
#         return self.generated_occurrence_id + u' ' + \
#                self.state + u' ' + \
#                self.added_date + u' ' + \
#                self.deleted_date
