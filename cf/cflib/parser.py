#!/usr/bin/python3
from html.parser import HTMLParser

class FormExtractor(HTMLParser):
    _attrs = {}
    _record = False
    _data = {} 

    def __init__(self, attrs):
        HTMLParser.__init__(self)
        self.reset()
        self._attrs = {}
        self._record = False
        self._data = {}
        for key, val in attrs:
            self._attrs[key] = val 

    def handle_starttag(self, tag, attrs):
        if tag == "form" or tag == "input":
            d_attrs = {}
            for key, val in attrs:
                d_attrs[key] = val

            if tag == "form":
                match_attrs = True
                for key in self._attrs:
                    if d_attrs.get(key) is None or \
                       d_attrs[key] != self._attrs[key]:
                        match_attrs = False
                        break
                self._record = match_attrs

            if self._record and (tag == "input" or tag == "select"):
                if "name" in d_attrs and "value" in d_attrs:
                    self._data[d_attrs["name"]] = d_attrs["value"]

    def handle_endtag(self, tag):
        if tag == 'form':
            self._record = False

    def get_data(self):
        return self._data
