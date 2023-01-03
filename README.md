[![LinkedIn][linkedin-shield]][linkedin-url]
[![MIT License][license-shield]][license-url]

<br />
<div>

<h3 align="center">Alignment API</h3>

  <p align="center">
    Local and Global Alignment in python
    
    
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
The objective of this sequence alignment technique is to place a query sequence end-to-end with the known sequence so as to find out some relationship like structural, functional, or evolutionary between them.
<br>
I implemented in this project **local** and **global** in python then deliver as API using django rest freamework

### Built With

* [![Python][Python]][Python-url]
* [![Django][Django]][Django-url]
* [![Django Rest Framework][drf-shield]][drf-url]
* [![sqlite][sqlite]][sqlite-url]

<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

* Python <= 3.10.6
* Pip <= 22.0.2
* Python virtual environment

1. Clone the repo
   ```sh
   git clone https://github.com/mohmmedfathi/Alignment-Api && cd Alignment-Api
   ```
2. Create virtual environment
   ```sh
   python3 -m venv venv
   ```
3. Activate virtual environment
   ```sh
   source venv/bin/activate
   ```
4. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
5. Migrate models
   ```sh
   python manage.py migrate
   ```
6. Run server
   ```sh
   python manage.py runserver 
   ```
   
   <!-- USAGE EXAMPLES -->
## Usage
We have two endpoint : 
<br>
### Global endpoint
#### http://127.0.0.1:8000/api/alignment/global/

<br>

![Screenshot from 2023-01-04 00-27-25](https://user-images.githubusercontent.com/64088888/210451739-3dc13876-8251-402c-8472-4f104e807058.png)

**you have to enter 5 value :**
<br>
* first sequence **is** seq1 <br>
* second sequence **is** seq2 <br>

* gap **is** gap <br>
* match **is** match <br>
* mismatch **is** mismatch <br>

sample input : 

```json
{ 
"seq1":"aaac",
"seq2":"agc", 
"gap" : -2,
"match":1, 
"mismatch" : -1 
}
```

output for previous input : 
```json
HTTP 201 Created
Allow: OPTIONS, GET, POST

{
    "id": 1,
    "seq1": "aaac",
    "seq2": "agc",
    "aligned1": "aaac",
    "aligned2": "ag-c",
    "score_matrix": "[0, -2, -4, -6],[-2, 1, -1, -3],[-4, -1, 0, -2],[-6, -3, -2, -1],[-8, -5, -4, -1]",
    "traceback_matrix": "['done', 'left', 'left', 'left'],['up', 'diag', 'left', 'left'],['up', 'up', 'diag', 'left'],['up', 'up', 'up', 'diag'],['up', 'up', 'up', 'diag']"
}
```
<br> <br>
### Local endpoint
#### http://127.0.0.1:8000/api/alignment/local/

<br>

![Screenshot from 2023-01-04 00-41-14](https://user-images.githubusercontent.com/64088888/210453324-f01e37e0-7420-4058-ac0d-14ddde0a2645.png)


**you have to enter 5 value :**
<br>
* first sequence **is** seq1 <br>
* second sequence **is** seq2 <br>

* gap **is** gap <br>
* match **is** match <br>
* mismatch **is** mismatch <br>

sample input : 

```json
{
"seq1": "ATGCT",
"seq2": "AGCT",
"gap": -2,
"match": 1,
"mismatch":-1
}

```

output for previous input : 
```json
HTTP 201 Created
Allow: POST, GET, OPTIONS

{
    "id": 1,
    "seq1": "ATGCT",
    "seq2": "AGCT",
    "score_matrix": "[0, 0, 0, 0, 0, 0],[0, 1, 0, 0, 0, 0],[0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 2, 0],[0, 0, 1, 0, 0, 3]",
    "best_score": 3,
    "alignment1": "ATGCT",
    "alignment2": "A-GCT"
}
```
<br>

* you can see the models in [Admin Panel](http://127.0.0.1:8000/admin) 

  ![Screenshot from 2023-01-04 00-52-04](https://user-images.githubusercontent.com/64088888/210454526-abcf3108-0f16-4ee5-94a7-6ba1c72a3fe5.png)
  
 <br>
 
To create a superuser
```sh
python manage.py createsuperuser
```
<!-- CONTACT -->
## Contact

Mohammed Fathi - mohmmedfathi.123@gmail.com

Project Link: [https://github.com/mohmmedfathi/Alignment-Api/](https://github.com/mohmmedfathi/Alignment-Api/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/mohammed-fathi-4a08071a7/
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-url]: https://docs.djangoproject.com/en/3.2/
[drf-shield]: https://img.shields.io/badge/DRF-Django%20Rest%20Framework-red
[drf-url]: https://www.django-rest-framework.org/
[Python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[Python-url]: https://docs.python.org/3/
[sqlite]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[sqlite-url]: https://www.sqlite.org/index.html
