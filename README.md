---
description: API Introduction for mock-up project in Eins-Internship Program.
---

# Introduction

### Inputs API

{% swagger method="get" path="" baseUrl="http://localhost:5000/simulator/inputs" summary="일부 시나리오 파일의 내용 혹은 시나리오 파일 목록을 불러옵니다." %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-parameter in="body" name="name" type="String" %}
default : all
{% endswagger-parameter %}

{% swagger-parameter in="body" name="format" type="String" %}
default : json
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="파일/목록을 정상적으로 불러왔습니다." %}

{% endswagger-response %}

{% swagger-response status="404: Not Found" description="파일이 존재하지 않습니다." %}

{% endswagger-response %}

{% swagger-response status="500: Internal Server Error" description="서버 측에서 에러가 발생했습니다." %}

{% endswagger-response %}
{% endswagger %}

{% swagger method="post" path="" baseUrl="http://localhost:5000/simulator/inputs" summary="Simulator 시나리오 파일을 등록합니다." %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-parameter in="body" name="files[]" type="file" required="true" %}

{% endswagger-parameter %}

{% swagger-response status="200: OK" description="시나리오 파일을 정상적으로 등록했습니다." %}

{% endswagger-response %}

{% swagger-response status="400: Bad Request" description="서버 측에서 에러가 발생했습니다." %}

{% endswagger-response %}
{% endswagger %}

{% swagger method="delete" path="" baseUrl="http://localhost:5000/simulator/inputs" summary="일부 혹은 전체 시나리오 파일을 삭제합니다." %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-parameter in="body" name="name" type="String" %}
default : all
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="시나리오 파일을 정상적으로 삭제했습니다." %}

{% endswagger-response %}

{% swagger-response status="404: Not Found" description="해당 시나리오 파일이 존재하지 않습니다." %}

{% endswagger-response %}

{% swagger-response status="500: Internal Server Error" description="서버 측에서 에러가 발생했습니다." %}

{% endswagger-response %}
{% endswagger %}

### Outputs API

{% swagger method="get" path="" baseUrl="http://localhost:5000/simulator/outputs" summary="시뮬레이션 결과 파일 내용을 불러옵니다." %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-parameter in="body" name="format" type="String" %}
default : json
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="시뮬레이션 결과를 정상적으로 불러왔습니다." %}

{% endswagger-response %}

{% swagger-response status="500: Internal Server Error" description="서버 측에서 에러가 발생했습니다." %}

{% endswagger-response %}
{% endswagger %}
