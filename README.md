# Assignments

## Files Description

LabeledDB_new: Meshes dataset.  
data: all Excel files  
visualization: all figures  

Step2 – pre-processing  
>|-- filter.py: Load the original meshes' detail into an Excel file (filter.xlsx in directory /data).  
>|-- resampling.py: Resample all meshes.  
>|-- transform.py: Pose alignment, Flipping, and Scaling for resampled meshes.

>The shape files after resampling and transforming will be saved in a new directory "/Remesh". Step 3 and step 4 will use shapes in "/Remesh".

Step3 – feature extraction  
>|-- features.py: Extract features and story in the Excel files.  
>|-- visualize.py: Features’ visualization.  

Step4 – query  
>|-- matching.py: Features matching. Include matching by ANN.  
>|-- query_gui.py: System GUI.  

Step5 –  
>|-- ann_timer.py: Compare querying time of ANN to KNN.  
>|-- tsne.py: Scatter plot by t-SNE.  

Step6 – evaluation  
>|-- step6.py: ROC curve.  

## How to run the code  

Main part:  
>1.	Pre-processing (execute only one time):   
>>a.	All files in step2. Sequence: filter.py -> resampling.py -> transform.py   
>>b.	Save_data.py in step3.  
>2.	Query matching: execute query_gui.py in step4.

T-SNE:  
>Execute t_sne.py in step5. (Make sure you have done the pre-processing before this step)  

Evaluation:  
>Execute step6.py in step6. (Make sure you have done the pre-processing before this step)  
