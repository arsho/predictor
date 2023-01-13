## Predictor of Antibody colors
Filters combinations from antibody conjugate pairs.

## Installation
- CLI app requirements:
```shell
pip install -r requirements.txt
```
- Web app requirements:
```shell
pip install -r web_requirements.txt
```

## Run CLI App
- Run the [inventory_predictor.py](inventory_predictor.py) file using Python3 and follow on screen instructions.
```text
python inventory_predictor.py
Antibody list: CD103, CD11c, CD138
------------------------
CD103 has 4 conjugates: APC, APC-R700, BV711, PE
CD11c has 3 conjugates: BUV805, eFluor450, PE-Cy7
CD138 has 5 conjugates: APC, BV421, BV605, BV750, PE
========================
Total panels found: 54

Suggested Panel #1
--------------------
CD103: APC
CD11c: BUV805
CD138: BV421

Suggested Panel #2
--------------------
CD103: APC
CD11c: BUV805
CD138: BV605

Suggested Panel #3
--------------------
CD103: APC
CD11c: BUV805
CD138: BV750

...
...
...

Suggested Panel #53
--------------------
CD103: PE
CD11c: PE-Cy7
CD138: BV605

Suggested Panel #54
--------------------
CD103: PE
CD11c: PE-Cy7
CD138: BV750
========================
Enter number of conditions (0 to exit): 2
Enter condition in "Antibody:Conjugate" pattern (e.g. CD103:APC)
Enter condition #1: CD103: APC
Enter condition #2: CD11c: PE-Cy7
========================
Total panels found: 4

Suggested Panel #1
--------------------
CD103: APC
CD11c: PE-Cy7
CD138: BV421

Suggested Panel #2
--------------------
CD103: APC
CD11c: PE-Cy7
CD138: BV605

Suggested Panel #3
--------------------
CD103: APC
CD11c: PE-Cy7
CD138: BV750

Suggested Panel #4
--------------------
CD103: APC
CD11c: PE-Cy7
CD138: PE
========================

Enter number of conditions (0 to exit): 1
Enter condition in "Antibody:Conjugate" pattern (e.g. CD103:APC)
Enter condition #1: CD138: PE
========================
Total panels found: 1

Suggested Panel #1
--------------------
CD103: APC
CD11c: PE-Cy7
CD138: PE
========================

Enter number of conditions (0 to exit): 0
Program terminated
```

## Run web app
- Install the web app requirements.
- Run the web application:
```shell
flask run
```

### References
- [Stackoverflow answer: All combinations from dictionary](https://stackoverflow.com/a/61335465/3129414)
- [Flask minimal example](https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application)