Workshop data cleaning

Work in process!  
To add: Information on data structure (float/meters)

#Background
Kolumbus is creating a project to predict delays in traffic... (add more)

#Task
You have been given one day of bus data. Your task is to clean this data and then train a machine learning model with it.

##Setup
### VM

### Conda

```sh
conda env create -f datavask_workshop.yml
```

```sh
# To activate this environment
source activate datavask_workshop
# to deactivate the environment use
source deactivate
```

Start the jupyter lab from the current directory of this repo:
```sh
jupyter lab
```
You will get a token link to the jupyter server. Open this in your browser.

## Where do I start?

Go to [Welcome.ipynb](http://localhost:8888/lab/tree/Welcome.ipynb) and follow instructions from there.

# (should we remove this part?)

##Folder structure
+ Workshop root  
  + Data\
  + read_json.py - The entry point to your application
  + DataCleaner.py - Where you implement all the data cleaning rules
  + test_dataCleaner.py - The script that tests your rules, no sneak peaking!
    

##Hints a.k.a Where do I start?!
To print the first 10 records in the dataframe:
```
print(frame.head(10))
```

To get the maximum value of a column:
```
print(frame['column'].max())
```

The same can be done for minimum, mean and standard deviation. 

There are hints placed in the code, specifically in the rules,
to help you on your way. 

The test script is not super strict, it simply contains the minimum requirements for the cleaning,
such as which columns need to stay and which should be removed etc. 
Therefore, you will not have to do it exactly the same way as we have. 

Your first step should be to look at the data...

#Extra task/If you have time (?)
