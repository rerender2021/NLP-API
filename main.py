import argparse
import os
import sys
import textwrap

from mugwort import Logger

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

# args parse
parser = argparse.ArgumentParser(
    description='This is a project that wraps NLP API by FastAPI.',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=r'''
  NLP API Helper

    Request params:

    Request examples:

''')
parser.add_argument('--host', type=str, help='listen host')
parser.add_argument('--port', type=int, help='listen port')
parser.add_argument('--lang-from', type=str, help='source lang')
parser.add_argument('--lang-to', type=str, help='target lang')
parser.add_argument('--model-dir', type=str, help=r'model folder')
parser.set_defaults(host='127.0.0.1', port=8100, lang_from='en', lang_to="zh", model_dir="./model")
params = parser.parse_args()

# init logger
log = Logger('NLP-API', Logger.INFO)
log.info('NLP API is starting, please wait...')

# init model dir
abs_model_dir = sys.executable
if params.model_dir:
    os.makedirs(params.model_dir, exist_ok=True)
    if os.path.isdir(params.model_dir):
        abs_model_dir = os.path.join(os.path.abspath(params.model_dir))
log.info('NLP-API model dir: %s', abs_model_dir)

# init fastapi & init NLP backend
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import PlainTextResponse
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

    app = FastAPI(openapi_url=None)
    model_path = os.path.join(abs_model_dir, 'opus-mt-' + params.lang_from + "-" + params.lang_to)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pipeline_name = "translation_" + params.lang_from + "_to_" + params.lang_to
    translation = pipeline(pipeline_name, model=model, tokenizer=tokenizer)

except Exception as exc:
    log.exception(exc)
    sys.exit(1)


@app.on_event('startup')
async def print_startup_config():
    log.info(
        textwrap.dedent('''
            NLP API has been started
              Endpoint: POST http://%s:%d/translate
              Language: %s
        ''').strip(),
        params.host,
        params.port,
        params.lang_from + " to " + params.lang_to
    )


@app.get('/ping')
async def pingpong_endpoint():
    return PlainTextResponse('pong')


@app.post('/translate')
async def ocr_endpoint(
        *, request: Request
):
    if 'content-type' in request.headers:
        content_type = request.headers.get('content-type').lower()
        log.info('Request ContentType: %s', content_type)

        response = {}
        if content_type == 'application/json':
            data = await request.json()
            text = data["text"]
            log.info(
                'length: %d',
                len(text)
            )
            response["result"] = translation(text)
            return response
        else:
            log.warning('Unsupported Content-Type: %s', type(content_type))
            return response
    else:
        log.warning('No Content-Type')
        return None


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app,
        host=params.host,
        port=params.port,
        log_level='error',
        access_log=False,
    )
