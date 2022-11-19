# Assignments

Files Description

LabeledDB_new: Meshes dataset.

Step2 –
	|-- filter.py: Load the original meshes’ detail into Excel files.
	|-- resampling.py: Resample all meshes and story them in Resample file.
	|-- transform.py: Pose alignment and Flipping for the Resample meshes.
Step3 –
	|-- features.py: Extract features and story in the Excel files.
	|-- visualize.py: Features’ visualization.
Step4 –
	|-- matching.py: Features matching.
	|-- query_gui.py: System GUI.
Step5 –
	|-- ann_timer.py: Compare ANN to KNN.
	|-- tsne.py: t-SNE.
Step6 –
	|-- step6.py: ROC curve.

How to run the code
Main part:
	1.	Pre-processing (execute only one time): 
		a.	All files in step2.
		b.	Save_data.py in step3.
	2.	Query matching: execute query_gui.py in step4.

T-SNE part:
	Execute t_sne.py in step5. (Make sure you have done the pre-processing before this step)

Evaluation:
	Execute Step6.py in step6. (Make sure you have done the pre-processing before this step)
