#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticfeeds.manager import Manager
from elasticfeeds.network import Link, LinkedActivity
from elasticfeeds.activity import Actor, Object, Origin, Target, Activity
import datetime
import time
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

from elasticfeeds.aggregators import (
    UnAggregated,
    RecentTypeAggregator,
    RecentTypeObjectAggregator,
    RecentObjectTypeAggregator,
    DateWeightAggregator,
    YearMonthTypeAggregator,
    YearMonthAggregator,
)

def test_manager():
    es_host = "0.0.0.0"
    es_port = 9200
    use_ssl = True  # Set to True if you are using SSL
    scheme = 'https' if use_ssl else 'http'
    username = 'admin'
    password = 'admin'
    es_url = f"{scheme}://{username}:{password}@{es_host}:{es_port}"
    
    print("Waiting for ES to be ready check at:", es_url)

    # Setup requests session to retry on failure and ignore SSL verification
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    # Check Elasticsearch health
    health_url = f"{scheme}://{es_host}:{es_port}/_cluster/health"
    ready = False
    while not ready:
        try:
            resp = session.get(health_url, auth=(username, password), verify=False)  # Disable SSL cert verification
            data = resp.json()
            print("json:", data)
            if data["status"] in ["yellow", "green"]:
                ready = True
            else:
                time.sleep(30)
        except Exception as e:
            print(str(e))
            time.sleep(30)

    print("ES is ready")

    # Create the Manager instance with the correct connection settings
    tst_manager = Manager(
        "testfeeds",
        "testnetwork",
        host=es_host,
        port=es_port,
        use_ssl=use_ssl,
        username="admin",
        password="admin",
        delete_network_if_exists=True,
        delete_feeds_if_exists=True
    )


    now = datetime.datetime.now()
    # Creates a linked activity
    tst_linked_activity = LinkedActivity("cquiros")
    # Testing properties
    tst_linked_activity.activity_id = "cquiros"
    tst_linked_activity.activity_class = "actor"
    tst_linked_activity.activity_type = "person"

    # Creates a link
    tst_link = Link("cquiros", tst_linked_activity)
    # Testing properties
    tst_link.actor_id = "cquiros"
    tst_link.linked_activity = tst_linked_activity
    tst_link.linked = now
    tst_link.link_type = "follow"
    tst_link.link_weight = 1
    tst_link.extra = {"some_extra_data": "test"}

    # Adds the network link
    # tst_manager.delete_feeds_index()
    # tst_manager.delete_network_index()
    
    tst_manager.add_network_link(tst_link)

    # Carlos follow Eduardo. Test of convenience function
    tst_manager.follow("cquiros", "edoquiros", now)

    # --------------------------- Adds some activity feeds ------------------------------

    # An actor called cquiros adds project A

    # Creates an actor
    tst_actor = Actor("cquiros", "person")
    # Creates an object
    tst_object = Object("50a808d3-1227-4149-80e9-20922bded1cf", "project")
    # Creates an Activity
    tst_activity = Activity(
        "add", tst_actor, tst_object, published=now + datetime.timedelta(minutes=12)
    )
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # cquiros adds project B

    # Creates an object
    tst_object = Object("152a3304-e78d-4fdf-9449-0943d6072596", "project")
    # Creates an Activity
    tst_activity = Activity(
        "add", tst_actor, tst_object, published=now + datetime.timedelta(minutes=24)
    )
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # cquiros adds Form 1 in project A

    # Creates an object
    tst_object = Object("326c1f4e-a489-4e36-9d0c-5638ef193f6f", "form")
    # Creates a target
    tst_target = Target("50a808d3-1227-4149-80e9-20922bded1cf", "project")
    # Creates an Activity
    tst_activity = Activity(
        "add",
        tst_actor,
        tst_object,
        activity_target=tst_target,
        published=now + datetime.timedelta(minutes=48),
    )
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # An actor called cquiros moves Form 1 from Project A to Project B

    # Creates an actor
    tst_actor = Actor("cquiros", "person", {"some_extra_data": "test"})
    # Testing properties
    tst_actor.actor_id = "cquiros"
    tst_actor.actor_type = "person"
    tst_actor.extra = {"some_extra_data": "test"}
    # Creates an object
    tst_object = Object(
        "326c1f4e-a489-4e36-9d0c-5638ef193f6f", "form", {"some_extra_data": "test"}
    )
    # Testing properties
    tst_object.object_id = "326c1f4e-a489-4e36-9d0c-5638ef193f6f"
    tst_object.object_type = "form"
    tst_object.extra = {"some_extra_data": "test"}
    # Creates an origin
    tst_origin = Origin(
        "50a808d3-1227-4149-80e9-20922bded1cf", "project", {"some_extra_data": "test"}
    )
    # Testing properties
    tst_origin.origin_id = "50a808d3-1227-4149-80e9-20922bded1cf"
    tst_origin.origin_type = "project"
    tst_origin.extra = {"some_extra_data": "test"}
    # Creates a target
    tst_target = Target(
        "152a3304-e78d-4fdf-9449-0943d6072596", "project", {"some_extra_data": "test"}
    )
    # Testing properties
    tst_target.target_id = "152a3304-e78d-4fdf-9449-0943d6072596"
    tst_target.target_type = "project"
    tst_target.extra = {"some_extra_data": "test"}
    # Creates an Activity
    tst_activity = Activity(
        "move",
        tst_actor,
        tst_object,
        activity_origin=tst_origin,
        activity_target=tst_target,
        extra={"some_extra_data": "test"},
    )
    # Testing properties
    tst_activity.activity_type = "move"
    tst_activity.activity_actor = tst_actor
    tst_activity.activity_object = tst_object
    tst_activity.published = datetime.datetime.now() + datetime.timedelta(minutes=72)
    tst_activity.activity_origin = tst_origin
    tst_activity.activity_target = tst_target
    tst_activity.extra = {"some_extra_data": "test"}
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # Carlos Watches project A. Test of convenience function
    tst_manager.watch("cquiros", "50a808d3-1227-4149-80e9-20922bded1cf", "project")
    # Wait 2 seconds for ES to store previous data. This is only for this testing script
    time.sleep(2)



    # Test Un-aggregated aggregator
    tst_base_aggregator = UnAggregated("cquiros")
    # This will bring 5 records
    test = tst_manager.get_feeds(tst_base_aggregator)
    print("test:",test)

    # Test recent type aggregator
    tst_recent_type_aggregator = RecentTypeAggregator("cquiros")
    test = tst_manager.get_feeds(tst_recent_type_aggregator)
    print("test:",test)

    # Test recent type object aggregator
    tst_recent_type_object_aggregator = RecentTypeObjectAggregator("cquiros")
    test = tst_manager.get_feeds(tst_recent_type_object_aggregator)
    print("test:",test)
    
    # Test recent object type aggregator
    tst_recent_object_type_aggregator = RecentObjectTypeAggregator("cquiros")
    test = tst_manager.get_feeds(tst_recent_object_type_aggregator)
    print("test:",test)
    
    # Test recent object type aggregator
    tst_date_weight_aggregator = DateWeightAggregator("cquiros")
    test = tst_manager.get_feeds(tst_date_weight_aggregator)
    print("test:",test)
    
    # Test year, month, type aggregator
    tst_year_month_type_aggregator = YearMonthTypeAggregator("cquiros")
    test = tst_manager.get_feeds(tst_year_month_type_aggregator)
    print("test:",test)
    
    # Test year, month, type aggregator
    tst_year_month_aggregator = YearMonthAggregator("cquiros")
    test = tst_manager.get_feeds(tst_year_month_aggregator)
    print("test:",test)
    


if __name__ == "__main__":
    test_manager()