###################
# This script trains a tensorflow model to predict annual melt rates
# from summer (JJA) global climate input.
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
###################


import sys, os
import tensorflow as tf
import xarray as xr
import numpy as np
import math


var = "PSL"

### Load climate data
topo = xr.open_dataset("../data/topo.nc")["topo"].values

# Load data maps
data_train = xr.open_dataset("/glade/scratch/raymonds/AImelt/ALL/atm/rproc/JJAavg/{}.nc".format(var))[var]#.sel(lat=slice(0,90))
lon = data_train.lon
lat = data_train.lat

if var=="PSL": # Mask out values where topography > 1000 m
    data_train.values[np.broadcast_to(topo, data_train.values.shape)>=1000] = 0


# Normalize in range (0.2, 0.8)
data_train.values = (data_train.values/100 - 920) / 140

data_train_tf = tf.convert_to_tensor(data_train.values, dtype=tf.float32)


areascale = 1e+12 / (1844610 * 1e+6)
areascale = areascale * (1693952*1e+6)/1e+12


# Load labels
labels_train = xr.open_dataset("/glade/scratch/raymonds/AImelt/ALL/lnd/rproc/timeseries/GrIS_integrated.annavg.nc")["MELT_ICE"].values * areascale
labels_train_tf = tf.convert_to_tensor(labels_train, dtype=tf.float32)



# Create model
def create_model(lamb):
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(192,288)),
        tf.keras.layers.Dense(4, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(lamb)),
        tf.keras.layers.Dense(1)])
    print(model.summary())
    return model



# Compile the model
model = create_model(1e-2)
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001), loss='mean_squared_error')


# Save model checkpoints
EPOCHS = 20000
checkpoint_filepath = "/glade/scratch/raymonds/checkpoints/checkpoints"
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor="val_loss",
        mode="min",
        save_best_only=True)

# Train the model
batch_size=30
steps = math.ceil(data_train.values.shape[0]/batch_size)
data_train_tf = tf.convert_to_tensor(data_train.values, dtype=tf.float32)
labels_train_tf = tf.convert_to_tensor(labels_train, dtype=tf.float32)
hist = model.fit(data_train_tf,
        labels_train_tf,
        epochs=EPOCHS,
        shuffle=True,
        batch_size=batch_size,
        steps_per_epoch=steps,
        validation_split=0.1,
        callbacks=[model_checkpoint_callback])

del(model)


# Get the best weights for model
model = create_model()
model.load_weights(checkpoint_filepath)


# Save the model
os.system("mkdir -p saved/nn_4/{}".format(var))
tf.keras.models.save_model(model, "saved/nn_4/{}/model2.tf".format(var))


# Save training history
np.save("saved/nn_4/{}/hist_loss.npy".format(var), np.array(hist.history["loss"]))
np.save("saved/nn_4/{}/hist_val.npy".format(var), np.array(hist.history["val_loss"]))
