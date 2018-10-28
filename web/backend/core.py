from flask import Flask, make_response, request
import os
import json

from whoosh import qparser, query
from whoosh.highlight import HtmlFormatter
from whoosh.lang.morph_en import variations
import whoosh.index as index

path = "financial-corpus"

ix = index.open_dir(path + "/index")
qp = qparser.QueryParser("content", schema=ix.schema, termclass=query.Variations)

app = Flask(__name__)


@app.route('/')
def search():
    q = qp.parse(u"politicians")
    results_list = []

    with ix.searcher() as searcher:
        results = searcher.search(q)
        results.formatter = HtmlFormatter(tagname="span")
        n_results = len(results)
        for hit in results:
            result = dict()
            result["filename"] = hit["title"]

            with open(os.path.join(path, "data", hit["filename"]), encoding="utf-8") as file:
                filecontents = file.read()
            result["text"] = hit.highlights("content", text=filecontents, )
            result["path"] = os.path.join(path, "data", hit["filename"])
            results_list.append(result)

    response = make_response(json.dumps({
        'results': results_list,
        'n_results': n_results
    }))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'text/json'
    return response
