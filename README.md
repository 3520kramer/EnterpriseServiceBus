# Currently supported transformations
Object and array definitions for each type can be found below.

| from / to   | JSON | XML | CSV | TSV |
|-------------|------|-----|-----|-----|
| JSON object |      |  ✅  |  ✅  |  🔜  |
| JSON array  |      |  🚫  |  ✅  |  🔜  |
| XML object  |   ✅  |     |  ✅  |  🔜  |
| XML array   |   ✅  |     |  ✅  |  🔜  |
| CSV object  |   ✅  |  ✅  |     |  🔜  |
| CSV array   |   ✅  |  🚫  |     |  🔜  |
| TSV object  |   🔜  |  🔜  |  🔜  |     |
| TSV array   |   🔜  |  🔜  |  🔜  |     |

## Object and array definitions
#### JSON object:
```json
{"person": 
  {"name": "john", "age": "20"}
}
```

#### JSON array:
```json
  [
    {"name": "john", "age": "20"},
    {"name": "john", "age": "20"}
  ]
```

#### XML object:
```xml
<?xml version="1.0" ?>
<person>
  <name>John Johnson</name>
  <age>20</age>
</person>
```
#### XML array:
```xml
<?xml version="1.0" ?>
<persons>
  <person>
    <name>Daryl Dixon</name>
    <age>33</age>
  </person>
  <person>
    <name>Rick Grimes</name>
    <age>35</age>
 </person>
</persons>
```
