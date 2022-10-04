from flask import Flask, make_response, jsonify, request
from Analyzer18_5_1 import Analyzer


app = Flask(__name__)
# app.secret_key = 'abcd'
# api = Api(app)

@app.route("/getContent", methods=["POST"])
def getContent():

   data = request.get_json()

   inc=data['inquiry']
   inc=inc['id']
   
   conv_list = data['conversationList']
   #  print(conv_list)
   
   filterd_conv_list = []
   for conv in conv_list:

      _id   = conv['id']
      inquiryId = conv['inquiryId']
      subject = conv['subject']
      content = conv['content']

      A = Analyzer()
      filterd_content = A.execute(content)#get filterd content through Analyzer
      bubble_content = filterd_content

      dic = {
             "id": _id,
            "inquiryId": inquiryId,
            "bubbleContent": bubble_content,
            "subject": subject
      }
      filterd_conv_list.append(dic)
   
   return jsonify(({
     "inquiry": {
        "id": inc
   },"conversationList":filterd_conv_list}))

   
   # return data




if __name__ == "__main__":

   app.run(host = '0.0.0.0', port = 5000, debug=False)
