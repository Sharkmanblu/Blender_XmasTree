# Blender 500 LED XmasTree
Blender Add-on and example file for Matt Parker [@standupmath](https://github.com/standupmaths/xmastree2021) 500 LED Xmas Tree

This repo (my first one) contains the file necessary to animate/create/preview/import and export CSV file for the "500-LED Xmas Tree" created by Matt Parker ( watch the video at the link belove) directly in Blender.

NOTE: Working Blender version 3.0 or above 

LINK blender download : https://www.blender.org/download/ 

LINK Stand-up Maths Youtube Video : https://www.youtube.com/watch?v=WuMRJf6B5Q4

# File and Folder Description

  * /XmasTree_2021.blend :  Blender example file ready to production ; open the file and you will find two readme notes on how to use and understand the file structure and add-on

 * /Add-on/XmasTree_Import-Export.py : Add-on installation file
  
 * /Coords/coords_2021.csv :  Matt Parker LED coordinates [@standupmath](https://github.com/standupmaths/xmastree2021)                                                                                                                
 * /coords_adjusted.csv : Harvard LED coordinates [@GSD6338-Harvard](https://github.com/GSD6338/XmasTree)
  
 * /Example_Effect/Fire_Effect.csv : fire effect created with geometry node and exported with add-on
                   /....  
  
#Basic Usage to create new effect
Open blender example file and strat the animation with he play button or with the spacebar key, you will see the Fire_Effect in real time calculated by the geometry node group.
Install the add-on via "Edit->Preferences->Add-Ons->install", selecting the downloaded "XmasTree_Import-Export.py", install it and activate it.
In the geometry node editor try to connect other output node to the color input node and watch the other example live.
Modify or create new effect as you like.
When you're happy with the result open the Xmas Tree panel and the export subpanel, select a folder and a filename and click "Save CSV RGB Value" to save your personal .csv file.
##IMPORTANT! FILENAME EXTENSION IS MANDATORY eg. test.csv 

#Basic Usage to load effect
Hide GeoNode collecion and unhide Import Tree one. 
With the example file open and the add-on installed, hide "GeoNode" collecion and unhide "Import Tree" one.
Go to the Xmas Tree panel and the import subpanel, select a .csv file in "Select LED CSV File" field  and click the "Load Led CSV animation" button.
Wait a few seconds and then start the animation with the play button or spacebar key.







