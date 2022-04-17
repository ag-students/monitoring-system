from app import app, db, cli
from app.models import Tmp, myData, sampleData, Users, Rooms

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Users': Users,
            'Rooms': Rooms,
            'Tmp': Tmp,
            'myData': myData,
            'sampleData': sampleData}
            