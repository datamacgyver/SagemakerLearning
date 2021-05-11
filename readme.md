Current task: Check that the new data conform to the old data and are 
thus useful for predicting (ie not from a different population)


# Sagemaker Learnings
This project is best opened in a "proper" IDE such as Pycharm as you 
can then follow the links between all the bits more easily. 

The data are junk data I got from an old web coding challenge. They simply
outline loan repayments over an 18 month period, along with loads of pre-made
features. This gives plenty of options to build models and new features.

## Assumptions
Many! Without access to stakeholders I've just done what the data seemed 
to suggest. I'm probably wrong in places!

## What I chose to model
Not really coming from FinTech I have very little idea! Also, timeseries are
hard! As such I am predicting:

*The proportion of debt repaid by each account over a 12 month period, 
that period running from month number 0 to 11 inclusive. If that proportion 
is over 1 I constrain to 1.* 

Based on my exploration, my best baseline for this is using the mean,
giving an RMSE of 0.20. I also note a fairly large proportion of 0s which I
have simply left as a todo I'm afraid. Let's chat!

## The. Code. 
### exploration_r
This is my initial notebook which I have knitted but it's not really
optimised for that kind of thing so it looks pretty bad. The notebook 
should be runnable (it's checkpointed). It is very much a train of 
thought.

My main observations:
* Some of the bandings (IMHO) have too few levels and others have not been 
transformed to numerics properly, there's mis-alignment and NAs.    
* Lots of features have a fair amount of skew with extreme values in 
both time and amounts. My favourite is a default date in the 80s. 
*  Settle flag does not represent all settlement events, some accounts 
will reach 0 or negative balance without the flag.  
* Similarly, settled date can be wrong and the default is in 2019 
* The sample ID is on accounts, not account-months. I approve. 
* I can't decide if transflag is feature leak or not, it's always 0 when
an account never pays. I've decided to go cautious and drop rows where 
transflag==0. This reduces my 0 inflation too. Winner. 
* Not everyone has data for all months. 
* There are more columns than the dictionary suggests. I think PrevCols is a 
duplicate of collectionstodate?

### model_training.ipynb
This is the entrypoint for training, but - and this is the key bit - it 
actually contains very little code. There is a method to this madness. 

The logic is that, if you were to "deploy" a notebook it should contain
nothing complex. That should be extracted to scripts and packages that 
are easier to manage, customise **and test**. You would then pass key 
parameters such as source data as variables to the notebook when you 
run it (probably with Airflow or similar), allowing them to be re-usable
artefacts rather than throw away bits of analysis. This approach also 
forces you to generalise and document. 

I've used AWS' implementation of XGBoost but you can also use SparkML 
and SKlearn. The advantages of those two is that it allows you to use 
pipleines for your feature engineering if that's you poison (they are 
fine but can be hard to test and debug so keep 'em simple!). 

### model_prediction.ipynb
What it says on the tin! Same philosophy as above. 

### modules
These should be relatively self-explanatory and represent the philosophy 
described above. Each module has documentation so I won't repeat all that 
here. In reality these would be more generalised and probably wrapped up in
a shared library. Also, I've tried to keep my docstrings snappy, there's 
some proper Numpy ones here and there where I needed the type inference.

### docs
This is where I stored what I'm doing and some notes on the data dictionary. 
May be some scrawlings on these, nothing I've QA'd.

### tests
Ran out out time. Should be a test for each module. There are some Data Quality
tests in the features module. 

## Model Results
Please refer to the modelTraining notebook for figures and numbers. 

### Tuning
There's not much to see in these, lower alpha values seem to perform a little
better. I could do with adding some more parameters and taking away those that 
didn't seem to help. Job for later perhaps. 

### RMSE
I have achieved an RMSE of 0.18 which is a slight improvement on 
my baseline value of 0.20. 

### Variable Importance
Standout values (weights in parentheses) are:
* percentageofbalance (26)
* DefaultAmt (15)

Which all seem to be different versions of the same thing: How much did they
owe and how much has already been paid. This would seem relatively logical. If you 
paid in the past then you will probably do so in the future. 

### Residual Error
Based on looking at the distribution of the errors I have a tendency to 
under-predict, which may simply be a result of the preponderance of 0s
in the dataset. It may be wise to predict "if any payment" in an initial
model to filter these out. 

Residual error is not static with the predictor, as we approach 100% of 
debt repaid our errors increase in spread and also tend to under-prediction
more. Basically this model does a horrible job of predicting good payers. Of
course, based on the exploration, these people are rarer. 

## Predicting the New Data
Running the prediction script on the new data suggests a total 12 month gain
of £1,456,450 but there is a high degree of skew in the predicted ratio. Analysis 
of the outliers is highly advised before we have any confidence in this, also see 
the TODOs section. 

## Thoughts for the future
### Data Enrichment
I reckon we can enrich this quite markedly. For example, we could grab
the company info from Companies House to get an idea of the size and 
finances (or even if they file properly). 

I would also be keen to get the interaction history between each account 
and the bank. People who have been sent legal letters may well be more 
cooperative!

### To-Dos
Yeah, this is long:  
[ ] Re-do the bandings, probably as dummies.  
[ ] Determine if all these accounts were new when the dataset 
was generated.  
[ ] Train 2 models. There's a lot of 0s in my predictor so I would actually 
prefer to train a model for "if 0" and then one for any that aren't predicted
 to be 0s. This could be expanded to other kinds of repayment behaviour too. 
[ ] Alternatively, perhaps some over-sampling?  
[ ] I have played with using a logistic function when my predictor is 
constrained between 0-1 in the past, may be worth a go.  
[ ] There's plenty of features here, perhaps a PCA?
[ ] Survival analysis on some of this might be fun.  
[ ] When predicting for the new data I would be inclined to check the 
features and errors have similar distributions, it's possible that they 
will not!  
[ ] I could probably try with some of the more esoteric hyperparameters too  
[ ] There's TODO comments throughout this. It's a work in progress.   