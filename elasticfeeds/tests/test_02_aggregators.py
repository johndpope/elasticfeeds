#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticfeeds.manager import Manager
from elasticfeeds.aggregators import (
    UnAggregated,
    RecentTypeAggregator,
    RecentTypeObjectAggregator,
    RecentObjectTypeAggregator,
    DateWeightAggregator,
    YearMonthTypeAggregator,
    YearMonthAggregator,
)


def test_aggregator():

    tst_manager = Manager("testfeeds", "testnetwork")

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
    test_aggregator()