import xml.etree.cElementTree as ET
from collections import defaultdict
import re


street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive",
            "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]


def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v)


def audit_street_type(street_types, street_types_count, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types_count[street_type] += 1
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")


def audit(input_file):
    osm_file = open(input_file, "r")
    street_types = defaultdict(set)
    street_types_count = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types,
                                      street_types_count,
                                      tag.attrib['v'])
    osm_file.close()
    return street_types, street_types_count
