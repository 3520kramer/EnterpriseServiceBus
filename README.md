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

#### CSV object:
```csv
a,b,c
1,2,3
```

#### CSV array:
```csv
a,b,c
1,2,3
3,4,5
```


## JSON
JSON object —> 
- xml: yes
- csv: yes
- tsv: N/A

JSON array —>
- xml: N/A
- csv: yes
- tsv: N/A

## XML
XML object —>
- json: yes
- csv: yes
- tsv: N/A

XML array ->
- json: yes
- csv: yes
- tsv: N/A

## CSV
CSV object —> 
- json: yes
- xml: yes
- tsv: N/A

CSV array —> 
- json: yes
- xml: N/A
- tsv: N/A

## TSV
Tsv —> dict —> json / xml / csv
- json: N/A
- xml: N/A
- csv: N/A

