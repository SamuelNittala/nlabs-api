from datetime import datetime
from flask import current_app as app
from flask import make_response, jsonify, request
from flask_jwt_extended.utils import get_jwt_identity
from .models import Advisor, User, Booking, db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

jwt = JWTManager(app)

@app.route("/admin", methods=['POST'])
def create_admin():
    user = User(username="admin", password=generate_password_hash("admin","sha256"), email="admin@admin.com", role="admin")
    db.session.add(user)
    db.session.commit()
    return "admin created"

@app.route("/admin/advisor", methods=['POST'])
@jwt_required()
def create_advisor():
    current_user = get_jwt_identity()
    req_data = request.get_json()
    user = User.query.filter_by(username= current_user).first()
    if (user.role == "admin"):
        advisor = Advisor(username=req_data["username"], photo_url=req_data["url"])
        db.session.add(advisor)
        db.session.commit()
        db.session.flush()
        if advisor:
            return make_response('Advisor added Succesfully', 201)
        else:
            return make_response("Could not add Advisor", 401)
    else:
        return make_response("Access Denied", 403)

@app.route("/user/register", methods=["POST"])
def register_user():
    req_data = request.get_json()
    user = User.query.filter_by(username= req_data["username"]).first()
    if not user:
        hash_pwd = generate_password_hash(req_data["password"],"sha256")
        user = User(
            username= req_data["username"],
            password= hash_pwd,
            role="user",
            email= req_data["email"]
        )
        db.session.add(user)
        db.session.commit()
        db.session.flush()
        access_token = create_access_token(identity=user.username)
        print(access_token)
        return make_response(jsonify({'token': access_token, 'id': user.id}), 201)
    else:
        return make_response("User already exists", 202)

@app.route("/user/login", methods=["POST"])
def login():
    req_data = request.get_json()
    user = User.query.filter_by(email= req_data["email"]).first()
    if not user:
        return make_response("User does not exist", 403)
    elif not req_data["email"] or not req_data["password"]:
        return make_response('Invalid details', 400)
    else:
        if check_password_hash(user.password,req_data["password"]):
            access_token = create_access_token(identity=user.username)
            return make_response(jsonify({'token': access_token, 'id': user.id}), 201)
        else:
            return make_response('Could not verify',401,{'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'})

@app.route("/user/<user_id>/advisor")
@jwt_required()
def get_advisors(user_id):
    advisors = Advisor.query.all()
    json_data = []
    for advisor in advisors:
        json_data.append({"advisor_id":advisor.id,"advisor_name": advisor.username, "url": advisor.photo_url})
    return make_response({"data": json_data},201)

@app.route("/user/<userid>/advisor/<advisorid>", methods=["POST"])
@jwt_required()
def book_advisor(userid, advisorid):
    req_data = request.get_json()
    timing = datetime.strptime(req_data["timing"], "%d/%m/%y %H:%M:%S")
    booking = Booking(userid,advisorid,timing)
    db.session.add(booking)
    db.session.commit()
    all_bookings = Booking.query.all()
    for booking in all_bookings:
        print(booking.user_id,booking.advisor_id, booking.timing)
    print(all_bookings)
    return {"data": "Success"}
