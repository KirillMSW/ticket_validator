from flask import Flask, jsonify, make_response, send_file, render_template
from flask import request
from flask import Response
import json

from ticket_generator import generate_ticket_id, generate_ticket

from table_exporter import add_new, void_table, update_status

app = Flask(__name__)

@app.route('/validate')
def validator():
   return render_template('index.html')

@app.route('/generate')
def generator():
   return render_template('generator.html')

@app.route('/void')
def voider():
   return render_template('void_ticket.html')

@app.get("/api/validate")
def validate():
    ticket_id=request.args.get('key', '')
    with open('db.json') as f:
        all_tickets=json.load(f)
        if ticket_id in all_tickets.keys():
            resp = make_response(jsonify(ticket_id=ticket_id, people_amount=all_tickets[ticket_id]["people_amount"],
                                    surname=all_tickets[ticket_id]["surname"],name=all_tickets[ticket_id]["name"],patronymic=all_tickets[ticket_id]["patronymic"]))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = make_response(jsonify({}))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

@app.post("/api/void")
def void():
    ticket_id=request.form.get('ticket_id')
    all_tickets = None
    with open('db.json') as f:
        all_tickets=json.load(f)
    if ticket_id in all_tickets:
        all_tickets[ticket_id]["people_amount"]=-1
        with open('db.json','w') as f:
            f.write(json.dumps(all_tickets))
        update_status(ticket_id,"АННУЛИРОВАН")

        resp = Response("OK")
        return resp
    else:
        resp = Response("INVALID")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    



@app.post("/api/checkin")
def checkin():
    ticket_id=request.form.get('ticket_id')
    people_to_pass=request.form.get('people_to_pass')
    all_tickets = None
    with open('db.json') as f:
        all_tickets=json.load(f)
    print(ticket_id,people_to_pass)
    if ticket_id in all_tickets.keys():
        all_tickets[ticket_id]["people_amount"]-=int(people_to_pass)
        with open('db.json','w') as f:
            f.write(json.dumps(all_tickets))
        update_status(ticket_id,"ИЗРАСХОДОВАН")
        resp = Response("OK")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = Response("INVALID")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.post("/api/generate")
def generate():
    surname=request.form.get('surname').capitalize()
    name=request.form.get('name').capitalize()
    patronymic=request.form.get('patronymic').capitalize()
    phone=request.form.get('phone')
    email=request.form.get('email')

    full_name=surname+' '+name+' '+patronymic
    full_name_ticket=surname+'\n'+name+'\n'+patronymic
    all_tickets = None
    with open('db.json') as f:
        all_tickets=json.load(f)

    new_ticket_id=generate_ticket_id()
    while new_ticket_id in all_tickets:
        new_ticket_id=generate_ticket_id()
    all_tickets[new_ticket_id]={"people_amount":1,"name":name,
                                "surname":surname,"patronymic":patronymic,"phone":phone,"email":email}
    with open('db.json','w') as f:
        f.write(json.dumps(all_tickets))
    generate_ticket(new_ticket_id,full_name_ticket)
    
    add_new(new_ticket_id,surname,name,patronymic,phone,email)

    resp = make_response(send_file("tickets/"+new_ticket_id+'.png'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
   app.run()