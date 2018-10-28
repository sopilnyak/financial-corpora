from flask import Flask, make_response, request
import os
import json

from whoosh import qparser, query
from whoosh.highlight import HtmlFormatter
import whoosh.index as index

path = "financial-corpus"

ix = index.open_dir(path + "/index")
qp = qparser.QueryParser("content", schema=ix.schema, termclass=query.Variations)

app = Flask(__name__, static_url_path="/static", static_folder="../../financial-corpus/data")


@app.route('/')
def search():
    q = qp.parse(request.args.get('query'))
    limit = int(request.args.get('max_docs'))
    if limit is None or limit < 1:
        limit = 10

    results_list = []

    with ix.searcher() as searcher:
        results = searcher.search(q, limit=limit)
        results.formatter = HtmlFormatter(tagname="span")
        n_results = len(results)
        for hit in results:
            result = dict()
            result["filename"] = hit["title"]

            with open(os.path.join(path, "data", hit["filename"]), encoding="utf-8") as file:
                filecontents = file.read()
            result["text"] = hit.highlights("content", text=filecontents, )
            result["path"] = "static/" + hit["filename"]
            results_list.append(result)

    response = make_response(json.dumps({
        'results': results_list,
        'n_results': n_results
    }))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'text/json'
    return response
