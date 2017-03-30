from __future__ import unicode_literals

import sys
from functools import reduce
import time as t
from datetime import datetime, date, time

from bawel.action.Action import Action
from bawel.model.Event import Event

def checkInputWaktu(jam, menit):
    return time(int(jam)-1, int(menit))

def checkInputTanggal(hari, bulan, tahun, jam, menit):
    d = date(int(tahun), int(bulan), int(hari))
    t = checkInputWaktu(jam, menit)
    dt = datetime.combine(d,t)
    return dt

# def normalizeParamJadwal(param, reminder):
#     if len(param) == 8:
#         param.append(1)         # default
#     param.append(reminder)
#     return param

# TODO: import job yang dilakukan

class TambahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, urgensi=1):
        try:
            dt = checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            ev1.create()
            def job(eid, text, lineid, stickerid=180):
                reminder.push(text, stickerid, lineid)
            print (dt.timetuple())
            reminder.add(namajadwal, t.mktime(dt.timetuple()), job, ("jangan lupa 1 jam lagi ada "+namajadwal,state['id'], ))
            return (state, "Event successfuly added")

        except ValueError:
            print(sys.exc_info())
            return (state, "Maaf kak, bawel ga ngerti, coba nambahjadwalnya kaya gini ya kak'si bawel tolong tambah acara/event/jadwal nonton bareng tanggal 29 Maret jam 5.50 sore'")

class LihatJadwal(Action):
    def act(self, state):
        ev1 = Event(state['id'],"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":state['id']})

        def printEvent(prev, ev):
            L = [ev['about'],str(ev['datetime']),str(ev['fullfiled'])]
            S = '\n'.join(L)
            return '{0}\n{1}'.format(prev, S)

        if events.count() == 1:
            ev = events[0]
            L = [ev['about'],str(ev['datetime']),str(ev['fullfiled'])]
            S = '\n'.join(L)
            output = '{0}'.format(S)
        elif events.count() > 1:
            output = reduce(printEvent, events)
        else :
            output = "Maaf tidak ada jadwal di database bawel :("

        return (state, output)

class UbahJadwal(Action):
    def act(self, namajadwal, hari, bulan, tahun, jam, menit, reminder, state, urgensi=1):
        try:
            dtime = checkInputTanggal(hari, bulan, tahun, jam, menit)
            ev1 = Event(state['id'],namajadwal,urgensi,hari,bulan,tahun,jam,menit,0)
            ev1.update()
            reminder.modify(namajadwal, t.mktime(dtime.timetuple()))
            return (state, "Event changed successfully")

        except ValueError:
            return (state, "format penulisan '/ubahjadwal namajadwal hari bulan tahun jam menit'  \nnama jadwal tidak dapat diubah")

class HapusJadwal(Action):
    def act(self, namajadwal, reminder, state):
        ev1 = Event(state['id'],namajadwal,10,1,1,1,1,1,0)
        ev1.removeQuery({"lineid":state['id'],"about":namajadwal})
        reminder.remove(namajadwal)
        return (state, "Event removed successfully")

# class SelesaiJadwal(Action):
#     def act(self, namajadwal, state):
#         ev1 = Event(state['id'],"lol",10,1,1,1,1,1,0)
#         eve = ev1.searchOne({"lineid":state['id'],"about":namajadwal})
#         ev1.set(eve)
#         ev1.setFulfilled(1)
#         ev1.update()

class ReportJadwal(Action):
    def act(self, state):
        ev1 = Event(state['id'],"lol",10,1,1,1,1,1,0)
        events = ev1.search({"lineid":state['id']})
        i = 0
        total = 0
        for event in events:
            total += 1
            if int(event['fullfiled']) == 1:
                i += 1
        percentage = i / total * 100
        return (state, "%.2f".format(percentage))