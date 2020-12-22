import uuid
import requests
import structlog


def _model_to_json(obj):
    """
    This method is used when describing request. It's possible to use json or Model transforming request object into
    json.

    Parameters
    ----------
    obj : json or Model
        Object that represents request data

    Returns
    -------
    out : json
        Json for request data
    """
    if hasattr(obj, 'json'):
        return obj.json()
    return obj


def request_to_json(obj):
    """
    This method is used when describing request. It's possible to use json or Model transforming request object into
    json.

    Parameters
    ----------
    obj : list(json) or list(Model) or json or Model
        Object that represents request data

    Returns
    -------
    out : list(json) or json
        List(json) for request data if obj list(json) or list(Model).
        Json for request data if obj is json or Model.
    """
    if isinstance(obj, list):
        return [_model_to_json(x) for x in obj]
    return _model_to_json(obj)


class RestClient:

    def __init__(self, host: str, headers: dict = None, proxies: dict = None):
        if not host:
            raise AttributeError('Attribute host should not be empty.')
        self.host = host
        self.headers = headers
        self.proxies = proxies
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='api')

    def get(self, path: str, params=None, **kwargs):
        return self._send_request(
            'GET', path,
            params=request_to_json(params),
            **kwargs
        )

    def post(self, path: str, json=None, **kwargs):
        return self._send_request(
            'POST', path,
            json=request_to_json(json),
            **kwargs
        )

    def _send_request(self, method: str, path: str, **kwargs):
        url = f'{self.host}{path}'

        log = self.log.bind(request_id=str(uuid.uuid4()))
        log.msg(
            'request',
            # caller=inspect.stack()[2][3],
            method=method,
            url=url,
            json=kwargs.get('json', None),
            params=kwargs.get('params', None),
            data=kwargs.get('data', None),
            headers=kwargs.get('headers', self.headers),
            proxies=kwargs.pop('proxies', self.proxies),
        )
        response = requests.request(
            method=method,
            url=url,
            headers=kwargs.pop('headers', self.headers),
            proxies=kwargs.pop('proxies', self.proxies),
            **kwargs
        )
        log.msg(
            'response',
            url=response.url,
            status_code=response.status_code,
            text=response.text,
            headers=response.headers,
            elapsed=(response.elapsed.microseconds / 1000),
            # curl=request_to_curl(response.request),
        )
        return response
