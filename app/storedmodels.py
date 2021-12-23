from secrets import choice
from flask_table.html import element
from .models import Guest, Table
import numpy as np
from math import pi
from flask_table import Table as FTable, Col, OptCol, ButtonCol
from . import db
# class CCol(Col):
#     def __init__(self,name,callback,**kwargs):
#         super(CCol,self).__init__(name)
#         self.cb = callback
#     def td_format(self,content):
#         return element('span',attrs={"class":"tag {}".format(self.cb(content))},content=content,escape_content=False)
#         return content

#     @staticmethod
#     def bool(d):
#         if d == 1:
#             return "is-info"
#         else:
#             return "is-danger"
# class GuestTable(FTable):
#     classes=["table","is-striped"]
#     name = Col("姓名")
#     phone = Col("电话")

#     arranged = CCol("已分配",callback=CCol.bool,choices={True:1,False:0})
#     table = Col("桌号")
#     seat_id = Col("座号")

#     def get_tr_attrs(self,guest):
#         if guest.arranged:
#             return {'class':'is-info is-selected'}
#         else:
#             return {'class':'is-danger is-selected'}

class Chart:
    def __init__(self):
        self.init()
    def init(self):
        db_tables = Table.query.all()
        db_guests = Guest.query.order_by("arranged","table","name").all()
        self.tables = {t.id:t.to_dict() for t in db_tables}
        self.guests = {g.id:g.to_dict() for g in db_guests}
        m_tables = {t.id:np.full(t.capacity,-1) for t in db_tables}
        self.pos_seat = {}
        for t in db_tables:
            ang = np.linspace(0,2*pi,t.capacity,False)
            dx,dy = np.cos(ang),np.sin(ang)
            r = t.radius+3
            self.pos_seat[t.id] = np.vstack((dx*(r),-dy*(r))).T.tolist()

        for g in db_guests:
            if g.arranged:
                if g.table not in self.tables:
                    print("error tableid {},guest id : {}".format(g.table,g.id))
                elif g.seat_id >= self.tables[g.table]["capa"]:
                    print("error seat_id {} out of table capa {},guest id : {}".format(g.seat_id,db_tables[g.table].capacity,g.id))
                elif m_tables[g.table][g.seat_id] != -1:
                        print("error seat {}:{} already has guest{} and guest{} still need".format(g.table,g.seat_id,m_tables[g.table][g.seat_id],g.id))
                else:
                    m_tables[g.table][g.seat_id] = g.id
        #################
        for t in self.tables:
            self.tables[t]['seats_arr'] = m_tables[t].tolist()
            self.tables[t]['contain'] = np.count_nonzero(m_tables[t]!=-1)
    def deal(self,type,data):
        res,msg,data = {
            "change": self._change(**data),
        }.get(type,(False,"no such operation",{}))
        return res,msg,data
    def _change(self,guests,table_id,**kargs):
        changed = {
            "t":[],
            "c":[],
            "g":[],
        }
        print("got change request : ",guests,table_id)
        if table_id == -1:
            for k in guests:
                guest = Guest.query.get(k)
                if guest is not None:
                    if guest.arranged:
                        if guest.table == table_id:
                            continue
                        changed['t'].append([guest.table,guest.seat_id])
                        changed['c'].append(guest.table)
                        self.tables[guest.table]['contain'] -= 1
                        self.tables[guest.table]['seats_arr'][guest.seat_id] = -1
                    
                    guest.arranged = False
                    guest.table = table_id
                    guest.seat_id = 0
                    changed['g'].append(k)
                else:
                    print("error: guest_id:{} not exist!",k)
        else:
            table = Table.query.get(table_id)
            if table is None:
                return False,"err: table_id:{} not exist!".format(table_id),{}
            if len(guests) > self.__get_empty_count(table_id):
                return False,"err: table:{} capa last:{} not enough for {} guests".format(table_id,self.__get_empty_count(table_id),len(guests)),{}

            for k in guests:
                guest = Guest.query.get(k)
                if guest is not None:
                    if guest.arranged:
                        if guest.table == table_id:
                            continue
                        changed['t'].append([guest.table,guest.seat_id])
                        changed['c'].append(guest.table)
                        self.tables[guest.table]['contain'] -= 1
                        self.tables[guest.table]['seats_arr'][guest.seat_id] = -1
                    
                    guest.arranged = True
                    guest.table = table_id
                    guest.seat_id = self.__get_first_empty(table_id)
                    self.tables[table_id]['seats_arr'][guest.seat_id] = guest.id
                    self.tables[table_id]['contain'] += 1
                    changed['g'].append(k)
                    changed['t'].append([guest.table,guest.seat_id])
                    changed['c'].append(guest.table)
                else:
                    print("error: guest_id:{} not exist!",k)

        db.session.commit()
        for k in guests:
            guest = Guest.query.get(k)
            if guest is not None:
                self.guests[k] = guest.to_dict()
        
        changed['c'] = list(dict.fromkeys(changed['c']))
        changed['g'] = list(dict.fromkeys(changed['g']))
        return True,"done",changed
    def __get_first_empty(self,table_id):
        mask = np.array(self.tables[table_id]['seats_arr'])==-1
        return np.argmax(mask).item() if np.where(mask) else -1
    def __get_empty_count(self,table_id):
        return np.count_nonzero(np.array(self.tables[table_id]['seats_arr'])==-1)
