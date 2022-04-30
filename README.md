## Fixing the structured log files

I made a mistake.  I was asked to go to a bunch of servers and download the log files to a central location so that they would be easy to review.  The log files were all in a JSON format, so I figured I could just concatenate them together to have fewer files in the directory.  Later I was told that they are actually 3 different formats that are similar, but have significant
differences.  

### Required Transformations

Here are the differences that need resolved between the formats:

* some dates are numeric in seconds since epoch
* some dates are numeric in milliseconds since epoch
* some dates are in an ISO string format
* a log record may have 1 or more `events` records that produces a separate log record per event
* in some records,`indicator-level` maps to `severity` by mapping:
          1 - TRACE, 2 - DEBUG, 3..5 INFO, 6..8 WARN, 9..10 ERROR
* in some records, `indicator-type` and `indicator-value` are concatenated to form the `message` field
* ... but when `indicator-type` contains the text "message", then only the `indicator-value` is used to form the `message` field
* the `source` field is mapped into the `process` field for output

Please help by writing a function that takes as input the mixed up concatenated log records I created, and converts them into the normalized correct format.  The JSON parsing is handled for you, and so is the serialization back into JSON.  

See example log files below.

## Getting Started

`transmogrify/transmogrify.py` is where you may start writing your code.  Add any other classes, helper functions, utility functions, and tests that you think are appropriate.  But be careful not to change the `transmogrify` function signature or tests would break.  Tests are in `tests` directory and there is a sample input `test/transmogrify-input.json` and a sample result `test/transmogrify-output.json`.  Even though you are not dealing with the JSON directly, these are helpful to view.

### Installing and running tests:

```
pip3 install --user -e . && python3 setup.py pytest
```

## Log formats

The source format (LEFT side), and the target normalized format (RIGHT side)

```javascript
[                                                 [
  {                                                 {
    "server": "10.10.0.123",                          "server": "10.10.0.123",
    "date": 1561994754,                               "date": "2019-07-01T15:25:54.000000",
    "severity": "INFO",                               "severity": "INFO",
    "process": "webapp",                              "process": "webapp",
    "message": "server started."                      "message": "server started."
  },                                                },
  {                                                 {
    "server": "10.10.0.123",                          "server": "10.10.0.123",
    "date": 1561994756,                               "date":  "2019-07-01T15:25:56.000000",
    "severity": "WARN",                               "severity": "WARN",
    "process": "webapp",                              "process": "webapp",
    "message": "one registered cluster node ..."      "message": "one registered cluster node ..."
  },                                                },
  {                                                 {
    "server": "10.10.0.202",                          "server": "10.10.0.202",
    "date": 1561994757000,                            "date": "2019-07-01T15:25:57.000000",
    "source": "jvm-x994a",                            "severity": "WARN",
    "events": [{                                      "process": "jvm-x994a",
        "indicator-level": 7,                         "message": "memory-low 200mb"
        "indicator-type": "memory-low",             },
        "indicator-value": "200mb"                  {
      }]                                              "server": "10.10.0.123",
  },                                                  "date": "2019-07-01T15:25:58.000000",
  {                                                   "severity": "ERROR",
    "server": "10.10.0.123",                          "process": "webapp",
    "date": 1561994758,                               "message": "invalid cluster node removed ..."
    "severity": "ERROR",                            },
    "process": "webapp",                            {
    "message": "invalid cluster node removed ..."     "server": "10.10.0.202",
  },                                                  "date": "2019-07-01T15:26:13.000000",
  {                                                   "severity": "WARN",
    "server": "10.10.0.202",                          "process": "jvm-x994a",
    "date": 1561994773000,                            "message": "memory-low 190mb"
    "source": "jvm-x994a",                          },
    "events": [{                                    {
        "indicator-level": 7,                         "server": "10.10.0.202",
        "indicator-type": "memory-low",               "date": "2019-07-01T15:27:23.000000",
        "indicator-value": "190mb"                    "severity": "WARN",
      }]                                              "process": "jvm-x994a",
  },                                                  "message": "memory-low 180mb"
  {                                                 },
    "server": "10.10.0.202",                        {
    "date": 1561994843000,                            "server": "10.10.0.202",
    "source": "jvm-x994a",                            "date": "2019-07-01T15:27:23.000000",
    "events": [{                                      "severity": "INFO",
        "indicator-level": 7,                         "process": "jvm-x994a",
        "indicator-type": "memory-low",               "message": "full GC"
        "indicator-value": "180mb"                  },
      },                                            {
      {                                               "server": "10.10.0.177",
        "indicator-level": 3,                         "date": "2019-07-01T15:27:25.000000",
        "indicator-type": "message",                  "severity": "WARN",
        "indicator-value": "full GC"                  "process": "microsrvc",
      }]                                              "message": "retry failed to downstream ..."
  },                                                }
  {                                               ]
    "server": "10.10.0.177",
    "date": "2019-07-01T15:27:25.000000",
    "severity": "WARN",
    "process": "microsrvc",
    "message": "retry failed to downstream ..."
  }
]
```
