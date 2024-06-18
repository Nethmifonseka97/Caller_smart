from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

app = Flask(__name__)
api = Api(app)

audio_path ={

}

result = {
    
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("path", type=str)
task_post_args.add_argument("audio", type=str)

task_post_args.add_argument("major_emotion", type=str)
task_post_args.add_argument("Happy", type=str)
task_post_args.add_argument("Satisfied", type=str)
task_post_args.add_argument("Interested", type=str)
task_post_args.add_argument("Neutral", type=str)
task_post_args.add_argument("Angry", type=str)
task_post_args.add_argument("Unsatisfied", type=str)
task_post_args.add_argument("Unhappy", type=str)

class Audio_list(Resource):
    def get(self):
        return audio_path


class Audio_analysis(Resource):
    def post(self, audio_id):
        args =  task_post_args.parse_args()
        if audio_id in audio_path:
            abort(409, "Audio ID is already taken")
        audio_path[audio_id] =  {"path": args["path"], "audio":args["audio"]}
        return audio_path[audio_id]
    
class Result(Resource):
    def post(self, result_id):
        args =  task_post_args.parse_args()
        result[result_id] ={"major_emotion": args["major_emotion"], 
                            "Happy":args["Happy"], "Satisfied":args["Satisfied"], 
                            "Interested":args["Interested"], "Neutral":args["Neutral"], 
                            "Angry":args["Angry"], "Unsatisfied":args["Unsatisfied"], "Unhappy":args["Unhappy"]
                           
                           }
        #self._emotion = {0:'Happy', 1:'Satisfied', 2:'Interested', 3:'Neutral', 4:'Angry', 5:'Unsatisfied', 6:'Unhappy'}

        
        return result[result_id]

class Result_list(Resource):
    def get(self):
        return result
    
api.add_resource(Audio_list, "/audio") 
api.add_resource(Audio_analysis, "/audio/<int:audio_id>")
api.add_resource(Result, "/result/<int:result_id>")
api.add_resource(Result_list, "/result") 

if __name__ == "__main__":
    app.run(debug=True)