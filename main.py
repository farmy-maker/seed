from flask import Flask, render_template, redirect
from flask_socketio import SocketIO
from models.plant import Plant, PlantFactorTrigger, PlantFactor
from models.device import DeviceController
from models.base import Session
from init import init_all
from forms import TriggerForm
from flask_wtf.csrf import CSRFProtect

session = Session()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
csrf = CSRFProtect(app)


@app.route('/')
def top():
    plant = session.query(Plant).first()
    if not plant:
        init_all(session)
        plant = session.query(Plant).first()
    trigger_form = TriggerForm()
    trigger_form.controller.choices = [(c.id, c.control_type) for c in session.query(DeviceController).all()]
    context = dict(
        plant=plant,
        trigger_form=trigger_form
    )
    return render_template('plant_top.html', **context)


@app.route('/factors/<int:factor_id>/triggers', methods=('POST',))
def create_trigger(factor_id):
    trigger_form = TriggerForm()
    trigger_form.controller.choices = [(c.id, c.control_type) for c in session.query(DeviceController).all()]
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
        session.add(trigger)
        session.commit()
        return redirect('/')
    context = dict(
        plant=plant,
        trigger_form=trigger_form
    )
    return render_template('plant_top.html', **context)


@app.route('/triggers/<int:trigger_id>', methods=('POST', ))
def delete_trigger(trigger_id):
    trigger = session.query(PlantFactorTrigger).filter(PlantFactorTrigger.id == trigger_id).one_or_none()
    if trigger:
        session.delete(trigger)
        session.commit()
    return redirect('/')


if __name__ == '__main__':
    socketio.run(app, debug=True)
