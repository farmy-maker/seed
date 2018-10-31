# utf-8
from flask import Flask, render_template, redirect, request, send_file
from models.plant import Plant, PlantFactorTrigger, PlantFactor
from models.device import DeviceController
from models.base import session
from init import init_all
from forms import TriggerForm
from flask_wtf.csrf import CSRFProtect
from apscheduler.scheduler import Scheduler
from config import FETCH_DATA_INTERVAL, FETCH_IMAGE_INTERVAL, TRIGGER_INTERVAL, MODE, DEBUG
from data import socketio, fetch_and_save_data, fetch_and_save_image, trigger_led, trigger_pump
from device import device
from auth import verify_key, get_qr_key
import qrcode
from io import BytesIO


app = Flask(__name__)
socketio.init_app(app)
app.config['SECRET_KEY'] = 'secret!'
csrf = CSRFProtect(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.route('/')
def top():
    session.commit()
    plant = session.query(Plant).first()
    trigger_form = TriggerForm()
    trigger_form.controller.choices = [(c.id, c.controller_type) for c in session.query(DeviceController).all()]
    context = dict(
        plant=plant,
        trigger_form=trigger_form
    )
    return render_template('top.html', **context)


@app.route('/factors/<int:factor_id>/triggers', methods=('POST',))
def create_trigger(factor_id):
    trigger_form = TriggerForm()
    trigger_form.controller.choices = [(c.id, c.controller_type) for c in session.query(DeviceController).all()]
    plant = session.query(Plant).first()
    factor = session.query(PlantFactor).filter(PlantFactor.id == factor_id).one_or_none()
    if trigger_form.validate():
        trigger = PlantFactorTrigger(
            plant_id=plant.id,
            factor_id=factor.id,
            threshold=trigger_form.threshold.data,
            operator=trigger_form.operator.data,
            controller_id=trigger_form.controller.data,
            action_type=trigger_form.action_type.data
        )
        try:
            session.add(trigger)
            session.commit()
        except:
            session.rollback()
            raise
        return redirect('/')
    context = dict(
        plant=plant,
        trigger_form=trigger_form
    )
    return render_template('top.html', **context)


@app.route('/triggers/<int:trigger_id>', methods=('POST', ))
def delete_trigger(trigger_id):
    trigger = session.query(PlantFactorTrigger).filter(PlantFactorTrigger.id == trigger_id).one_or_none()
    if trigger:
        try:
            session.delete(trigger)
            session.commit()
        except:
            session.rollback()
            raise
    return redirect('/')


@csrf.exempt
@app.route('/control/', methods=['POST', 'GET'])
def control():
    key = request.args.get('key')
    key_valid = verify_key(key)
    if request.method == 'POST':
        token = request.json['token']
        if verify_key(token):
            controller_type = request.json['controller_type']
            action_type = request.json['action_type']
            if controller_type == 'led':
                getattr(device.led_controller, action_type)()
            elif controller_type == 'pump':
                getattr(device.pump_controller, action_type)()
            return "OK", 200
        else:
            return "403 Forbidden", 403
    else:
        return render_template('control.html', key=key, valid=key_valid)


@app.route('/qrcode/')
def qr():
    return render_template('qrcode.html')


@app.route('/qrcode.jpg')
def qr_jpg():
    key = get_qr_key()
    f = BytesIO()
    img = qrcode.make(request.url_root + 'control/?key=' + key)
    img = img.convert('RGB').resize((240, 240))
    img.save(f, format='jpeg')
    f.seek(0)
    return send_file(f, mimetype='image/jpeg')


if __name__ == '__main__':
    print('Starting...')
    plant = session.query(Plant).first()
    if not plant:
        init_all(session)
        plant = session.query(Plant).first()
    sched = Scheduler()
    sched.start()
    sched.add_cron_job(fetch_and_save_data, minute="*/{}".format(FETCH_DATA_INTERVAL), args=[session, plant])
    sched.add_cron_job(fetch_and_save_image, minute="*/{}".format(FETCH_IMAGE_INTERVAL), args=[session, plant])
    if MODE != 'demo':
        sched.add_cron_job(trigger_led, minute="*/{}".format(TRIGGER_INTERVAL), args=[plant])
        sched.add_cron_job(trigger_pump, minute="*/{}".format(TRIGGER_INTERVAL), args=[plant])
    socketio.run(app, host='0.0.0.0', debug=DEBUG)
