from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from content import synopsis_generate, topic_generate, plan_generate, first_generate, character_generate, character_nudge_generate, synop_nudge_generate, first_nudge_generate, brain_nudge_generate, brain_generate
import re

app = Flask(__name__)
cors = CORS(app, resources={r"/*":{"origins":"*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/gen', methods=['POST'])
@cross_origin()
def hello_world():
    req_data = request.get_json()
    print("Got data from client : ", req_data)
    return jsonify("")


@app.route('/brain_ask', methods=['POST'])
@cross_origin()
def brain_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    output = brain_generate(info=req_data['info'], brainDump=req_data['brainDump'], prompt=req_data['prompt'])

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


@app.route('/brain_nudge', methods=['POST'])
@cross_origin()
def brain_nudge_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    output = brain_nudge_generate(info=req_data['info'], brainDump=req_data['brainDump'])

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


@app.route('/topic', methods=['POST'])
@cross_origin()
def topic_gen():
    # 입력 목록 : (선택적) 기존 토픽 리스트, (선택적) 프롬프트, 브레인 덤프. 키워드, 타입, info
    req_data = request.get_json()
    print("토픽 생성")
    originalList, prompt, type, info, chosenKeywords, brainDump = req_data['originalList'], req_data['prompt'], req_data['type'], req_data['info'], req_data['chosenKeywords'], req_data['brainDump']
    output = topic_generate(originalList=originalList, prompt=prompt, type=type, info=info, chosenKeywords=chosenKeywords, brainDump=brainDump)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    print("토픽 생성 결과물", response)
    
    return jsonify(response)


@app.route('/synopsis', methods=['POST'])
@cross_origin()
def synopsis_gen():
    req_data = request.get_json()

    prompt, synopsis, info = req_data['prompt'], req_data['synopsis'], req_data['info']
    output = synopsis_generate(prompt=prompt, synopsis=synopsis, info=info, type=req_data['type'])

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    
    return jsonify(response)


@app.route('/synop_nudge', methods=['POST'])
@cross_origin()
def synop_nudge_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    output = synop_nudge_generate(info=req_data['info'], synopsis=req_data['synopsis'])
    print("아웃풋", output)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


@app.route('/char', methods=['POST'])
@cross_origin()
def char_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    info = req_data['info']

    output = character_generate(info=info)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


@app.route('/char_nudge', methods=['POST'])
@cross_origin()
def char_nudge_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    info, characters = req_data['info'], req_data['characters']

    output = character_nudge_generate(info=info, characters=characters)
    print("아웃풋", output)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


@app.route('/plan', methods=['POST'])
@cross_origin()
def plan_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    dump, keywords, planList = req_data['dump'], req_data['keywords'], req_data['planList']

    output = plan_generate(dump=dump, keywords=keywords)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)

@app.route('/first', methods=['POST'])
@cross_origin()
def first_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    info = req_data['info']

    output = first_generate(info=info)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


@app.route('/first_nudge', methods=['POST'])
@cross_origin()
def first_nudge_gen():
    req_data = request.get_json()
    print("Got data from client : ", req_data)

    info, first = req_data['info'], req_data['first']

    output = first_nudge_generate(info=info, first=first)

    response = {
        "data": output['data'],
        "total_tokens": output['total_tokens']
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
