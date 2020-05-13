# import json
# from flask import Flask, g, request, jsonify, Response, send_file
# import jsonpickle
# import numpy as np
# import cv2

# app = Flask(__name__)


# @app.route('/', methods=['POST'])
# def home():
#     r = request
#     nparr = np.fromstring(r.data, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0],)
#                 }
#     response_pickled = jsonpickle.encode(response)
#     filename = 'C:/AppFullStack/backend/image.png'
#     filename2 = 'C:/AppFullStack/backend/image2.png'
#     cv2.imwrite(filename, img)
#     img2 = cv2.imread(filename, 0)
#     cv2.imwrite(filename2, img2)
#     print('gravou')
#     return Response(response=response_pickled, status=200, mimetype="application/json",)


# @app.route('/get_image')
# def get_image():
#     filename2 = 'C:/AppFullStack/backend/image2.png'
#     print('pegou')
#     return send_file(filename2, mimetype='image/png')


# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=5000)


import tkinter as tk

rootInputComBotao = tk.Tk()

inputTela = tk.Canvas(rootInputComBotao, width=400, height=300)
inputTela.pack()

entry1 = tk.Entry(rootInputComBotao)
inputTela.create_window(200, 140, window=entry1)


def getText():
    get = entry1.get()
    print(get)
    rootInputComBotao.destroy()


button1 = tk.Button(text='Get Text', command=getText)
inputTela.create_window(200, 180, window=button1)

rootInputComBotao.mainloop()
