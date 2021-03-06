
import urllib.parse
import unicodedata
import logging
from slugify import slugify

from googletrans import Translator

translator = Translator()

internalTagIdChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                      'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                      '\\', '-', '_']


class Tag:
    def __init__(self, request_maker, customer, business_unit=None):
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def post_tag(self, tag_id, tag_type_id, titles):  # TODO Add 'create tag type if not exists' option
        # TODO Add option to guess at language, with override if not English (e.g. russian not polish)
        # TODO Add option to translate title to other languages
        if self._business_unit is None:
            url = 'v1/customer/{0}/tag'
            url = url.format(self._customer)
        else:
            url = 'v1/customer/{0}/businessunit/{1}/tag'
            url = url.format(self._customer, self._business_unit)

        tag_id = slugify(tag_id)

        tag_name_xml = '<tagName language="{0}">{1}</tagName>'
        tag_names = []
        for key in titles.keys():
            tag_names.append(tag_name_xml.format(key, titles[key]))
        tag_names = ''.join(tag_names)

        tag_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <publish-metadata
          xmlns="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1
                              ../xsd/publish-metadata.xsd ">
          <data>
            <tag id="{0}" type="{1}">
              <tagNames>
                {2}
              </tagNames>
            </tag>
          </data>
        </publish-metadata>"""
        body = tag_xml.format(tag_id, tag_type_id, tag_names)
        logging.debug(body)

        response = self._request_maker.post(url=url, data=body)
        return response

    def get_tag(self, tag_id):
        raise NotImplementedError
        if self._business_unit is None:
            url = 'v1/customer/{0}/tag/{1}'
            url = url.format(self._customer, tag_id)
        else:
            url = 'v1/customer/{0}/businessunit/{1}/tag/{2}'
            url = url.format(self._customer, self._business_unit, tag_id)

        response = self._request_maker.get(url=url)
        return response
