from elasticsearch import Elasticsearch
from datetime import date, datetime
from datetime import timedelta
from core.config import settings
import json
from data_connector.postgres.endpoint import translate

conn = Elasticsearch(
        [settings.ELASTIC_CLUSTER],
        http_auth=(
        	settings.ELASTIC_USER,
            settings.ELASTIC_PASS,
        ),
        port=settings.ELASTIC_PORT)

def simple_query(dataset, x, value, calculate):
    data = conn.search(index='bantrab', size=0, body={
            "query": {
            "match": {
                "type": dataset
            }
        },
        "aggregations": {
            "simple_aggregation": {
                "terms": {
                    "field": x,
                    "min_doc_count":0
                },
                "aggregations": {
                    "value": {
                        calculate: {
                            "field": value
                        }
                    }
                }
            }
        }
    })

    aggregations = data["aggregations"]
    list_aggregation = aggregations["simple_aggregation"]
    value = []
    response = {}
    for agg in list_aggregation['buckets']:
        if 'key_as_string' in agg:
            key = agg['key_as_string']
        else:
            key = agg['key']
        val = agg['value']['value']
        value.append({'value':val, 'name':key})
    response['series'] = []
    response['series'].append({'name':translate(dataset, x), 'data':value}) 
    return response

def simple_nested_query(dataset, x, legend,  value, calculate):
    data = conn.search(index='bantrab', size=0, body={
            "query": {
            "match": {
                "type": dataset
            }
        },
        "aggregations": {
            "nested_aggregation": {
                "terms": {
                    "field": x,
                    "min_doc_count":0
                },
                "aggregations": {
                    "second_level":{
                        "terms": {
                            "field": legend,
                            "min_doc_count":0
                        },
                        "aggregations":{
                            "value": {
                                calculate: {
                                    "field": value
                                }
                            }
                        }
                    }
                }
            }
        }
    })

    aggregations = data["aggregations"]
    list_aggregation = aggregations["nested_aggregation"]
    key = []
    value = {}
    response = {}
    for agg in list_aggregation['buckets']:
        if 'key_as_string' in agg:
            key = key + [agg['key_as_string']]
        else:
            key = key + [agg['key']]
        for agg1 in agg["second_level"]["buckets"]:
            if 'key_as_string' in agg1:
                legend = agg1['key_as_string']
            else:
                legend = agg1['key']
            valuet = agg1['value']['value']
            if legend in value:
                temp = value[legend]
                temp.append(valuet)
                value[legend] = temp
            else:
                value[legend] = [valuet]
    response['xAxis']={}
    response['series']=[]
    response['xAxis']['name'] = translate(dataset, x)
    response['xAxis']['data'] = key
    for key in value:
        response['series'].append({"name":key, "data":value[key]}) 
    return response

def multiple_agg_query(dataset, x, y):
    aggregations = {}
    list_values = []
    dict_values={}
    for row in y:
        list_values.append(row.calculate+"_"+row.value)
        dict_values[row.calculate+"_"+row.value]=row.name
        aggregations[row.calculate+"_"+row.value]= {
                                    row.calculate: {
                                        "field": row.value
                                    }
                                }
    data = conn.search(index='bantrab', size=0, body={
            "query": {
            "match": {
                "type": dataset
            }
        },
        "aggregations": {
            "nested_aggregation": {
                "terms": {
                    "field": x,
                    "min_doc_count":0
                },
                "aggregations":aggregations
            }
        }
    })

    aggregations = data["aggregations"]
    list_aggregation = aggregations["nested_aggregation"]
    key = []
    value = {}
    response = {}
    for agg in list_aggregation['buckets']:
        if 'key_as_string' in agg:
            key = key + [agg['key_as_string']]
        else:
            key = key + [agg['key']]
        for keys in agg:
            if keys in list_values:
                legend = dict_values[keys]
                valuet = agg[keys]['value']
                if legend in value:
                    temp = value[legend]
                    temp.append(valuet)
                    value[legend] = temp
                else:
                    value[legend] = [valuet]
    response['xAxis']={}
    response['series']=[]
    response['xAxis']['name'] = translate(dataset, x)
    response['xAxis']['data'] = key
    for key in value:
        response['series'].append({"name":key, "data":value[key]}) 
    return response