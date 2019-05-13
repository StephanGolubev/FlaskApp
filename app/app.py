from flask import Flask
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/extention', methods=['POST'])
def extention():
    if request.method == 'POST':
        import json
        import network

        # получаем запрос
        response = request.json
        # переводим в массив
        response2 = json.dumps(response)
        response2 = json.loads(response2)
        my_list = []
        my_dict = {}
        my_string = ''


        # лупим через массив скриптов
        number = 0
        for i in response2['code']:
            x = network.classify(i)
            if x == 1:
                my_list.append(number);
                my_string = my_string + str(number) + ','
                number = number + 1
            else:
                number = number + 1

        return repr(my_string)


@app.route("/neyr")
def nayr():
    return "hello"

if __name__ == '__main__':
    app.run()
