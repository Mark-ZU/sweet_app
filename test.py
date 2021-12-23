from app import db, create_app, models
import numpy as np

if __name__ == '__main__':
    app=create_app()
    app.app_context().push()

    # keys = [2,3,4]
    # for k in keys:
    #     guest = models.Guest.query.get(k)
    #     print(guest.name)
    #     guest.name = guest.name+"c"
    # db.session.commit()
    # print("-----\nafter changed\n")
    # for k in keys:
    #     guest = models.Guest.query.get(k)
    #     print(guest.name)