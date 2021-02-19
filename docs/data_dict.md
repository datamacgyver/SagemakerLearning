# Data Dictionary

### Account ID
ID for each account/customer

### Month
Transaction Month

### Number
Numeric value corresponding to Month (Ranges from 0-18)  
*It's 1-18 as it's an 18 month window*

### CurrentBalance
Balance on the account at current month

### DefaultDate
Date that the contract of the loan was terminated due to breach
*Looking at the data, this is info from the seller*

### DefaultAmt
Balance remaining (£) at point of default
*Also from seller?* 

### ConsistancyL3m, ConsistancyL6m, ConsistancyL12m, ConsistancyL24m
Number of payments made within the past 3,6,12,24 months from the current month

### ConsistancyHist
Number of total previous payments

### ColsL3m, ColsL6m, ColsL12m, ColsL24m
Amount paid within the past 3,6,12,24 months from the current month

### ColsHist
Total amount previously paid

### pay
Indicator variable with value 1 when the account makes a payment within the current month

### payl3m, payl6m, payl12m, payl24m
Indicator variable with value 1 when the account has made at least 1 payment in the last 3,6,12,24 months from the current month

### PayHist
Indicator variable with value 1 when the account makes at least 1 payment prior to the current month

### AvgL3m, AvgL6m, AvgL12m, AvgL24m
Average payment made in the previous 3,6,12,24 months

### AvgHist
Average payment made prior to current month

### SDL3m, SDL6m, SDL12m, SDL24m
Standard deviation of payments made in the previous 3,6,12,24 months

### SDHist
Standard deviation of payments made prior to the current month

### VarL3m, VarL6m, VarL12m, VarL24m
Variance of payments made in the previous 3,6,12,24 months

### VarHist
Variance of payments made prior to the current month

### MonthlyTransaction
Amount paid (£) in given month, 0 when the account has not paid

### monthssincenopay
Number of months from current month since the account last missed a payment

### collectionstodate
Total amount (£) collected up to current month

### monthssincelastpayment
Number of months from current month since the account last made a payment

### percentageofbalance
Monthly transaction amount divide by current balance in given month

### lastpaymentamount
Amount last paid (£). £0 if the account has never made a payment to date

### cumpctofbalance
To date the percentage of starting balance paid

### monthstodefault
Number of months from account origination to default date

### transflag
Indicator variable with value 1 when the account has made at least one payment in the 
past

### settlementdate
Date that the account settled
*Note to me: Debt settlement means accepting less than the balance, not clearing it. I 
did not know that!*
*This appears to be knowledge of the future, do not use it! Also, it's set to 2019 when 
they haven't settled yet.*

### settle
Indicator variable with value 1 when the account has settled
*Not always wgeb ut was repaid though*

### remainingbalance
Balance at end of current month (= CurrentBalance - MonthlyTransaction)

### CollectionsBand
Value of MonthlyTransaction split into bands

### remainingbalband
Value of remaining balance split into bands

### balanceband
Value of current balance split into bands

### CollectionsBandN
Numeric version of collections band

### remainingbalbandN
Numeric version of remainingbalance band

### balancebandN
Numeric version of balance band

### insample
Value 0,1 where the data has been split 30%/70% respectively
*Based on account ID by the look of it*

### lastpayband
Value of last payment amount split into bands

### MonthsSincePayBand
Value of months since payment split into bands

### Payment_Pct_Band
Value of cumulative pct of balance split into bands


# Also
### PrevCols 
Total paid before this month
*Possible duplciate of collectionstodate*

### PreviousPayments
Number of payments before this month

### age
Not sure, it's NA in some and static over an account so probably linked to age of account. Not 
investigated at this time. 