#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticfeeds.manager import Manager
from elasticfeeds.network import Link, LinkedActivity
from elasticfeeds.activity import Actor, Object, Origin, Target, Activity
import datetime


def test_manager():
    tst_manager = Manager('testfeeds', 'testnerwork', delete_network_if_exists=True, delete_feeds_if_exists=True)
    # Creates a linked activity
    tst_linked_activity = LinkedActivity('cquiros')
    # Testing properties
    tst_linked_activity.activity_id = 'cquiros'
    tst_linked_activity.activity_class = 'actor'
    tst_linked_activity.activity_type = 'person'

    # Creates a link
    tst_link = Link('cquiros', tst_linked_activity)
    # Testing properties
    tst_link.actor_id = 'cquiros'
    tst_link.linked_activity = tst_linked_activity
    tst_link.linked = datetime.datetime.now()
    tst_link.link_type = 'follow'
    tst_link.link_weight = 1
    tst_link.extra = {'some_extra_data': 'test'}

    # Adds the network link
    tst_manager.add_network_link(tst_link)

    # --------------------------- Adds some activity feeds ------------------------------

    # An actor called cquiros adds project A

    # Creates an actor
    tst_actor = Actor('cquiros', 'person')
    # Creates an object
    tst_object = Object('50a808d3-1227-4149-80e9-20922bded1cf', 'project')
    # Creates an Activity
    tst_activity = Activity('add', tst_actor, tst_object)
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # cquiros adds project B

    # Creates an object
    tst_object = Object('152a3304-e78d-4fdf-9449-0943d6072596', 'project')
    # Creates an Activity
    tst_activity = Activity('add', tst_actor, tst_object)
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # cquiros adds Form 1 in project A

    # Creates an object
    tst_object = Object('326c1f4e-a489-4e36-9d0c-5638ef193f6f', 'form')
    # Creates a target
    tst_target = Target('50a808d3-1227-4149-80e9-20922bded1cf', 'project')
    # Creates an Activity
    tst_activity = Activity('add', tst_actor, tst_object, activity_target=tst_target)
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)

    # An actor called cquiros moves Form 1 from Project A to Project B

    # Creates an actor
    tst_actor = Actor('cquiros', 'person', {'some_extra_data': 'test'})
    # Testing properties
    tst_actor.actor_id = 'cquiros'
    tst_actor.actor_type = 'person'
    tst_actor.extra = {'some_extra_data': 'test'}
    # Creates an object
    tst_object = Object('326c1f4e-a489-4e36-9d0c-5638ef193f6f', 'form', {'some_extra_data': 'test'})
    # Testing properties
    tst_object.object_id = '326c1f4e-a489-4e36-9d0c-5638ef193f6f'
    tst_object.object_type = 'form'
    tst_object.extra = {'some_extra_data': 'test'}
    # Creates an origin
    tst_origin = Origin('50a808d3-1227-4149-80e9-20922bded1cf', 'project', {'some_extra_data': 'test'})
    # Testing properties
    tst_origin.origin_id = '50a808d3-1227-4149-80e9-20922bded1cf'
    tst_origin.origin_type = 'project'
    tst_origin.extra = {'some_extra_data': 'test'}
    # Creates a target
    tst_target = Target('152a3304-e78d-4fdf-9449-0943d6072596', 'project', {'some_extra_data': 'test'})
    # Testing properties
    tst_target.target_id = '152a3304-e78d-4fdf-9449-0943d6072596'
    tst_target.target_type = 'project'
    tst_target.extra = {'some_extra_data': 'test'}
    # Creates an Activity
    tst_activity = Activity('move', tst_actor, tst_object, activity_origin=tst_origin, activity_target=tst_target,
                            extra={'some_extra_data': 'test'})
    # Testing properties
    tst_activity.activity_type = 'move'
    tst_activity.activity_actor = tst_actor
    tst_activity.activity_object = tst_object
    tst_activity.published = datetime.datetime.now()
    tst_activity.activity_origin = tst_origin
    tst_activity.activity_target = tst_target
    tst_activity.extra = {'some_extra_data': 'test'}
    # Adds the activity
    tst_manager.add_activity_feed(tst_activity)




