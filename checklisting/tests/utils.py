"""Utility functions for tests."""

import json

from scrapy.http import TextResponse, Request


def response_for_content(content, encoding, url='http://example.com',
                         metadata=None):
    """Create a Scrapy Response containing the content.

    This function is used for unit-testing to verify that spiders can
    parse the contents provided.

    Args:
        content (str): the contents of the response.
        encoding (str): the character encoding of the content, e.g. 'utf-8'.

    Kwargs:
        url (str): the URL from the request that created the response.
        metadata (dict): parameters to pass to the response.

    Returns:
        TextResponse. A scrapy response object.

    """
    request = Request(url=url, meta=metadata)
    return TextResponse(url=url, request=request, body=content,
                        encoding=encoding)


def response_for_data(data, url='http://example.com', metadata=None):
    """Create a Scrapy Response for the json encode-able data.

    This function is used for unit-testing to verify that spiders can
    parse the JSON encode-able data provided.

    Args:
        data (list): the contents of the response.

    Kwargs:
        url (str): the URL from the request that created the response.
        metadata (dict): parameters to pass to the response.

    Returns:
        TextResponse. A scrapy response object.

    """
    content = json.dumps(data)
    encoding = 'utf-8'
    return response_for_content(content, encoding, url=url, metadata=metadata)
