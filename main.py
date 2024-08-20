from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import SQLAlchemyError
import base64
from . import database
from .models import *
from sqlalchemy.orm import joinedload

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import send_file
import mimetypes
from io import BytesIO


main = Blueprint('main', __name__,template_folder='templates')
UPLOAD_FOLDER = main.root_path + '/files/'

@main.route('/')
def home():
    services = database.session.query(Service).all()  
    return render_template(
        'homepage.html',
        services=services
    )

@main.route('/dashboard/')
@login_required
def dashboard():
    me = User.query.filter_by(email=current_user.email).first()
    t_approved_req = len(ServiceRequestForm.query.filter_by(active=True).all())
    t_peding_req = len(ServiceRequestForm.query.filter_by(active=False).all())
    services = Service.query.options(joinedload(Service.publisher)).all() 
    servicerequest = ServiceRequestForm.query.options(joinedload(ServiceRequestForm.service),joinedload(ServiceRequestForm.user)).all()

    # publisher
    users = database.session.query(User).all()  
    servicerequest = ServiceRequestForm.query.options(joinedload(ServiceRequestForm.service),joinedload(ServiceRequestForm.user)).all()
    t_services = len(services)   
    t_users = len(users)  
    t_servicerequest = len(servicerequest)

    return render_template(
        'dashboard/index.html',
        me=me, services=services,
        users=users,servicerequest=servicerequest,
        t_services=t_services,t_users=t_users,
        t_servicerequest=t_servicerequest,t_approved_req=t_approved_req,
        t_peding_req=t_peding_req
    )

@main.route('/dashboard/services/')
@login_required
def services():
    me = User.query.filter_by(email=current_user.email).first()
    services = database.session.query(Service).all()  
    return render_template(
        'dashboard/services.html',
        me=me,       
        services=services                
    )

@main.route('/dashboard/services/create/',methods=['POST','GET'])
@login_required
def create_services():
    me = User.query.filter_by(email=current_user.email).first()
    if request.method == 'POST':
        name= request.form['name']
        description=request.form['description']

        service = Service(
            name=name,
            description=description,
            author=me.id,
        )
        database.session.add(service)
        database.session.commit()
        flash(f'Created service {name} with success') 
        return redirect(url_for('main.services'))
    return render_template(
        'dashboard/create_service.html',
        me=me,                        
    )

@main.route('/dashboard/clients/')
@login_required
def clients():
    me = User.query.filter_by(email=current_user.email).first()
    users = database.session.query(User).all()  
    return render_template(
        'dashboard/clients.html',
        me=me,       
        users=users                
    )

@main.route('/dashboard/service/request/',methods=['POST','GET'])
def services_request_form():
    me = User.query.filter_by(email=current_user.email).first()
    if request.method == 'POST':
        service = request.form['service']
        pdf_file = request.files['pdf_file']
        file = pdf_file.read()
        file_name = pdf_file.filename
        reason = request.form['reason']
        # print('--------------------',type(service))
        srf = ServiceRequestForm(
            service_id=int(service),
            reason=reason,pdf_file=file,
            file_name=file_name, 
            client=me.id,
        )
        database.session.add(srf)
        database.session.commit()
        flash(f'Created service {service} with success') 
        return redirect(url_for('main.service_request'))
    return redirect(url_for('main.service_request'))

@main.route('/dashboard/services/request/')
@login_required
def service_request():
    me = User.query.filter_by(email=current_user.email).first()
    services = database.session.query(Service).all()  
    servicerequest = ServiceRequestForm.query.options(joinedload(ServiceRequestForm.service),joinedload(ServiceRequestForm.user)).all()
    return render_template(
        'dashboard/service_requests.html',
        me=me, services=services,
        servicerequest=servicerequest                
    )


@main.route('/download_file/<int:request_id>')
@login_required
def download_file(request_id):
    request_form = ServiceRequestForm.query.get(request_id)
    if request_form and request_form.pdf_file:
        file_data = BytesIO(request_form.pdf_file)
        mime_type = mimetypes.guess_type(request_form.file_name)[0] if request_form.file_name else 'application/octet-stream'
        return send_file(
            file_data,
            as_attachment=True,
            download_name=request_form.file_name,  # Use the stored file name
            mimetype=mime_type
        )
    else:
        flash('File not found for this service request.')
        return redirect(url_for('main.service_request'))



@main.route('/approve_service_request/<int:request_id>', methods=['POST'])
@login_required
def approve_service_request(request_id):
    # Retrieve the service request form from the database
    request_form = ServiceRequestForm.query.get(request_id)
    if request_form:
        # Update the status of the service request form
        request_form.active = True
        # Commit the changes to the database
        database.session.commit()
        flash(f'Status updated successfully') 
    else:
        flash(f'Service request form not found') 
    return redirect(url_for('main.service_request'))
 
@main.route('/disapprove_service_request/<int:request_id>', methods=['POST'])
@login_required
def disapprove_service_request(request_id):
    # Retrieve the service request form from the database
    request_form = ServiceRequestForm.query.get(request_id)
    if request_form:
        # Update the status of the service request form
        request_form.active = False
        # Commit the changes to the database
        database.session.commit()
        flash(f'Status updated successfully') 
    else:
        flash(f'Service request form not found') 
    return redirect(url_for('main.service_request'))
 
@main.route('/dashboard/privacy-policy/')
@login_required
def  policy():
    me = User.query.filter_by(email=current_user.email).first()
            
    return render_template('dashboard/policy.html',  me=me, )
 
@main.errorhandler(ProgrammingError)
def handle_db_error(e):
    print(str(e.__dict__))
    return "An error occurred while processing your request.", 500
