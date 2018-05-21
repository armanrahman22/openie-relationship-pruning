from logging import getLogger
from typing import Dict, Generator, List

import logic
import ujson as json
from env import TIMEOUT
from logic import Relationship
from sanic import Sanic, response
from sanic_cors import CORS

log = getLogger(__name__)

app = Sanic(__name__)
app.config.REQUEST_TIMEOUT = TIMEOUT
app.config.RESPONSE_TIMEOUT = TIMEOUT
CORS(app, automatic_options=True)


def load_jsonl_stream(text: str) -> Generator[Dict, None, None]:
    """Takes jsonl string and returns list of dictionary objects

    Arguments:
        text {str} -- jsonl file

    Returns:
        Generator[Dict, None, None] -- list of relationship dictionaries
    """

    lines = text.splitlines()
    for line in lines:
        try:
            yield json.loads(line)
        except ValueError:
            log.exception('Error parsing JSONL input')


@app.route('/prune/form', methods=['POST'])
async def prune(request):
    """Endpoint for pruning service

    Arguments:
        request {[type]} -- must contain an uploaded jsonl file

    Returns:
        Response string -- json string of pruned relationships
    """

    upload = request.files.get('upload')
    if not upload:
        return response.text('Missing file: upload', status=400)

    text: str = upload.body.decode('utf-8')
    relations = load_jsonl_stream(text)
    pruned: List[Relationship] = logic.prune(list(relations))

    return response.text('\n'.join(relation.to_json() for relation in pruned))
