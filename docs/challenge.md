# About the Datasets

We have provided two data sets in two PSVs: 
* “SIATestDataSalefile” – this is the accounts open as of the point 
  at which we are pricing. 
* “SIATestDataBuildSample” – This contains the history of all accounts 
  including accounts which paid down and settled. 

* 10,000 accounts/customers data over an 18-month period from February 
  2017 to August 2018.
* Each row in the dataset corresponds to an individual customer within 
  the current month, where the month is defined within variable [Month].
* The unique identifier within this data is therefore the combination 
  of [AccountID] and [Month].
* Please see the variable definitions document for details on all 
  variables within the data.
* Please note the variable [Age] refers to the age (years) of the 
  debt not the individual.

## RM: What to model? 
Well, we could take the initial data and then predict some things:
* Predict full payment. Watch the 0 frequency. 
* Predict settlement at < full payment. Watch the 0 frequency.
* Predict no payment (do initial filter for the transaction flag. No need 
troubling the model. That would make it horrifically 0 inflated however)
* what % of their balance they will likely repay in the next year. Could 
use the input of the above three as features if you fancied. 
