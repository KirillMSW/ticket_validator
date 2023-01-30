from flask import Flask, jsonify, make_response, send_file, render_template
from flask import request
from flask import Response
import json

from ticket_generator import generate_ticket_id, generate_ticket


app = Flask(__name__)

@app.route('/validate')
def home():
   return render_template('index.html')

@app.route('/generate')
def generator():
   return render_template('generator.html')

@app.get("/api/validate")
def validate():
    ticket_id=request.args.get('key', '')
    with open('db.json') as f:
        all_tickets=json.load(f)
        if ticket_id in all_tickets.keys():
            resp = make_response(jsonify(ticket_id=ticket_id, people_amount=all_tickets[ticket_id]["people_amount"],name=all_tickets[ticket_id]["name"]))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = make_response(jsonify({}))
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
        resp = Response("OK")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = Response("INVALID")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.post("/api/generate")
def generate():
    name=request.form.get('name')
    people_amount=request.form.get('people_amount')

    all_tickets = None
    with open('db.json') as f:
        all_tickets=json.load(f)

    new_ticket_id=generate_ticket_id()
    while new_ticket_id in all_tickets:
        new_ticket_id=generate_ticket_id()
    all_tickets[new_ticket_id]={"people_amount":int(people_amount),"name":name}
    with open('db.json','w') as f:
        f.write(json.dumps(all_tickets))
    generate_ticket(new_ticket_id,name,people_amount)
    
    resp = make_response(send_file("tickets/"+new_ticket_id+'.png'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
   app.run()