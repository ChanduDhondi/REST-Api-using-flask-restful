from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

song_args = reqparse.RequestParser()
song_args.add_argument('name', type=str, help='name of the song should be there')
song_args.add_argument('singer', type=str, required=False)
song_args.add_argument('movie', type=str, required=False)

song_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'singer' : fields.String,
    'movie' : fields.String
}


class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True, nullable = True)
    singer = db.Column(db.String)
    movie = db.Column(db.String)

    def __repr__(self):
        return f'Name : {self.name}, Singer : {self.singer}, Movie : {self.movie}'
    
class Songs(Resource):

    @marshal_with(song_fields)
    def post(self):
        args = song_args.parse_args()
        song = SongModel(name=args['name'], singer=args['singer'], movie=args['movie'])
        db.session.add(song)
        db.session.commit()
        songDetails = SongModel.query.all()
        return songDetails
    
class Song(Resource):

    @marshal_with(song_fields)
    def get(self, id):
        song = SongModel.query.filter_by(id=id).first()
        if not song:
            abort(404, message=f'Song with {id} is not exist')
        return song
    
    @marshal_with(song_fields)
    def put(self, id):
        args = song_args.parse_args()
        song = SongModel.query.filter_by(id=id).first()
        if not song:
            abort(404, message=f'Song with {id} is not exist')
        song.name = args['name']
        song.singer = args['singer']
        song.movie = args['movie']
        db.session.commit()
        return song, 201
    
    @marshal_with(song_fields)
    def delete(self, id):
        song = SongModel.query.filter_by(id=id).first()
        if not song:
            abort(404, message=f'Song with {id} is not exist')
        db.session.delete(song)
        db.session.commit()
        return song, 204

class songslist(Resource):

    @marshal_with(song_fields)
    def get(self):
        song = SongModel.query.all()
        return song
         
api.add_resource(Songs, '/songs')
api.add_resource(Song, '/song/<int:id>')
api.add_resource(songslist, '/songslist')

if __name__ == '__main__':
    app.run()