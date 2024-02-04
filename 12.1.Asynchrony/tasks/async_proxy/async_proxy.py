from aiohttp import ClientSession
from yarl import URL
from aiohttp import web


async def proxy_handler(request: web.Request) -> web.Response:
    """
    Check request contains http url in query args:
        /fetch?url=http%3A%2F%2Fexample.com%2F
    and trying to fetch it and return body with http status.
    If url passed without scheme or is invalid raise 400 Bad request.
    On failure raise 502 Bad gateway.
    :param request: aiohttp.web.Request to handle
    :return: aiohttp.web.Response
    """
    get_url = request.query.get('url')
    if not get_url:
        return web.Response(text='No url to fetch', status=400)

    url = URL(get_url)
    if not url.scheme:
        return web.Response(text='Empty url scheme', status=400)
    if url.scheme != 'http':
        return web.Response(text=f'Bad url scheme: {url.scheme}', status=400)

    async with ClientSession() as session:
        async with session.get(url) as response:
            body = await response.text()
            return web.Response(text=body, status=response.status)


async def setup_application(app: web.Application) -> None:
    """
    Setup application routes and aiohttp session for fetching
    :param app: app to apply settings with
    """
    app.router.add_get('/fetch', proxy_handler)
    app['session'] = ClientSession()


async def teardown_application(app: web.Application) -> None:
    """
    Application with aiohttp session for tearing down
    :param app: app for tearing down
    """
    if 'session' in app:
        await app['session'].close()
