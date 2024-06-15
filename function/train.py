
def train(_global, _data):
    from ultralytics import YOLO
    # Load a model
    model = YOLO(_data["RAW"])  # build a new model from scratch
    # Use the model
    def _dtrain_(_):
        _global["TRAIN_X"] = _.train_x
        _global["TRAIN_Y"] = _.train_y
        _global["CURRENTEPOCH"] = _.current_epoch
    model.add_callback("dtrain",_dtrain_)
    model.train(data=_data["YAML"], epochs=_data["EPOCHS"])  # train the model
    # metrics = model.val()  # evaluate model performance on the validation set