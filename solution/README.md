# DWH Coding Challenge

## Docker Command to Run This Application

```
# build image docker
docker build -t dwh-coding-challenge .

# run docker container
docker run dwh-coding-challenge
```


## Design Thinking

First thing to do is to understand the problem statement.
Our objective is to create a data lake that will be able to store and analyze the data from the three tables.
The table is saved in 3 different folder, thus I create a function called `def get_json(folder_name)` to get the data more efficiently.
The function will return all the json data from the folder, we just need to specify where the folder is.

After all The Data is loaded, we have an issue to read them because the timestamp is in the unix format and it is not well merged.
Then I reformat the timestamp and merge them into single column called `all_ts`.
In order to see historical data we need to sort it by our new timestamp `all_ts`.

All Data is set, now we need to narrow the data that we need to see.
To do this, I filter the data by non null values in `set.credit_used` and `set.savings_balance`.
The data need to include timestamp in readable format, credit used value and saving balance value.
Now the data is ready to be analyzed.
