The idea of this topology is to simulate a typical flow, namely:

* get message from rabbitmq
* various stages of processing
* index results somewhere (and deal with original message)


There is a script to populate write messages to the rabbitmq queue.

```
$ python src/populate.py localhost sparse_average 10
Publishing {'values': [99, 73, 31, 45, 13]}
Publishing {'values': [28, 5, 13, 34, 15, 92, 35, 6, 27, 30]}
Publishing {'values': [91, 1, 37, 80, 87, 23]}
Publishing {'values': [29, 1, 100, 34, 10, 36, 43, 58, 2, 37]}
Publishing {'values': [96, 68, 90, 44, 56, 47, 75, 57, 77, 19]}
Publishing {'values': [25, 36, 13, 54, 47, 13, 29, 84, 58, 14]}
Publishing {'values': [78, 10, 10, 26, 39]}
Publishing {'values': [50, 42, 48, 96, 35, 87]}
Publishing {'values': [99, 68, 3, 65, 64, 37, 75, 83, 59, 95]}
Publishing {'values': [31, 44, 7, 50, 66, 89, 54, 66, 45, 85]}
```


And then the pipeline will
* total and count the values ([SummariseBolt](src/summarise.py))
* average the values ([CalcAverageBolt](src/calcaverage.py))
* write the values somewhere ([IndexBolt](src/index.py))
