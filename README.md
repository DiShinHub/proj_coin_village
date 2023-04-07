<h1>IDNA RESTful API </h1>

<h2>인스톨</h2>
<pre><code>
pip install -r requirements.txt
</pre></code>

<h2>실행</h2>
<pre><code>
python manage.py run
</pre></code>


<h2>폴더 구조</h2>
<h5>Application Factory Pattern</h5>

.<br>
├── app<br>
│   ├── __init__.py<br>
│   ├── main<br>
│   │   ├── controller<br>
│   │   │   └── __init__.py<br>
│   │   ├── __init__.py<br>
│   │   ├── model<br>
│   │   │   └── __init__.py<br>
│   │   └── service<br>
│   │       └── __init__.py<br>
│   └── test<br>
│       └── __init__.py<br>
└── requirements.txt<br>


* app - flask 앱 base dir
* controller - API 엔드포인트
* model - DB 테이블 정의 
* service - 비즈니스로직
* test - python unittest
* config.py - 프레임웍 설정 

<h3>파이썬 버전</h3>
Python 3.6.7

<h3>참고자료</h3>
https://medium.com/free-code-camp/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563
