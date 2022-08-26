# Deep Object Pose Estimation (DOPE) - Evaluation 

This repo contains a simplified version of the **evaluation** script for DOPE.
The original repo for DOPE [can be found here](https://github.com/NVlabs/Deep_Object_Pose). 

## Running Evaluation

After running inference with trained model weights, you can measure the performance of the model.

Below is an example of running the evaluation script:
```
python evaluate.py --data_prediction ../inference/output --data ../sample_data 
```
## Arguments 
### `--data`:
Path to groundtruth data for the predictions that you want to evaluate. 

### `--data_prediction`:
Path to predictions that were outputted from running inference. To support the evaluation of multiple sets of weights at once, this path can point to a folder containing the **outputs of multiple inference results**. 

### `--models`: 
Path to 3D model files. See the sample folder `YCB_models` for reference on what needs to be included. 
These models are loaded before running evaluation and are rendered to compute the 3D error between the predicted results and ground truth. 

If you trained DOPE on a new object and want to evaluate its performance, make sure to include the 3D model files in a folder that matches `"class_name"` in the ground truth `.json` file. 

Multiple models can be loaded at once as the script will recursively search for any 3D models in the folder specified in `--models`.

### `--adds`:
To be added.

### `--cuboid`:
To be added.
