from urllib.parse import urljoin, urlparse


def remove_parameters_from_url(url):
    return urljoin(url, urlparse(url).path)
