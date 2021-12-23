from app import db, create_app, models
import numpy as np

def insert_guest(*data):
    for d in zip(*data):
        _new = models.Guest(name=d[0],table=d[1],seat_id=d[2],arranged=True)
        db.session.add(_new)
    db.session.commit()
def insert_table(*data):
    for d in zip(*data):
        _new = models.Table(pos_x=d[0],pos_y=d[1],radius=d[2],capacity=int(d[3]))
        db.session.add(_new)
    db.session.commit()

if __name__ == "__main__":
    db.create_all(app=create_app())

    app=create_app()
    app.app_context().push()
    def insertGuests():
        names = []
        table = []
        seat_id = []
        for i in range(30):
            names.append("Mark"+str(i))
            names.append("Sybil"+str(i))
            table.append(i%15)
            table.append(i%15)
            seat_id.append(i//3%7)
            seat_id.append(9-i//3%7)
        insert_guest(names,table,seat_id)

    def insertTables():
        width,height = (500,300)
        nx,ny = (5,3)
        x = np.linspace(0,width,nx)
        y = np.linspace(0,height,ny)
        xy = np.dstack([*np.meshgrid(x,y)]).reshape(-1,2)+100
        capa = np.random.randint(9,14,nx*ny,dtype=int)
        r = 35+(capa-8)*3
        insert_table(xy[:,0],xy[:,1],r,capa)

    def change_to_unarranged():
        guests = models.Guest.query.all()
        for g in guests:
            g.arranged = False
            g.table = 0
            g.seat_id = 0
        db.session.commit()
    # insertGuests()
    # insertTables()
    from app import storedmodels as M
    chart = M.Chart()

    change_to_unarranged()