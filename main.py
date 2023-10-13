import re
from pprint import pprint


async def view_hello(receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })

    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })

async def view_test(receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })

    await send({
        'type': 'http.response.body',
        'body': b'Test!',
    })


routes = [
    (r'/', view_hello),
    (r'/test', view_test)
]

async def app(scope, receive, send):
    pprint(scope)
    assert scope['type'] == 'http'

    for route_mapping in routes:
        route_pattern = f'^{scope["path"]}$'
        view = route_mapping[1]
        path = route_mapping[0]
        result = re.match(route_pattern, path)
        print('Debug:', path, result, route_pattern)
        if result:
            await view(receive, send)
            break
    else:
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Not handled',
        })
