# AWS EC2
    docker-server
         ├── docker-compose.yml
         ├── nginx
         │   ├── Dockerfile
         │   ├── nginx-app.conf
         │   └── nginx.conf
         └── subbly-docker
# docker-compose.yml
    version: '3'
    services:

        nginx:
            container_name: nginx
            build: ./nginx
            image: docker-server/nginx
            restart: always
            ports:
              - "80:80"
            volumes:
              - ./subbly-docker:/srv/docker-server
              - ./log:/var/log/nginx
            depends_on:
              - django

        django:
            container_name: django
            build: ./subbly-docker
            image: docker-server/django
            restart: always
            command: uwsgi --ini uwsgi.ini
            volumes:
              - ./subbly-docker:/srv/docker-server
              - ./log:/var/log/uwsgi
# Dockerfile
        FROM nginx:latest

        COPY nginx.conf /etc/nginx/nginx.conf
        COPY nginx-app.conf /etc/nginx/sites-available/

        RUN mkdir -p /etc/nginx/sites-enabled/\
            && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

        # EXPOSE 80
        CMD ["nginx", "-g", "daemon off;"]

# ELK (Elasticsearch, Logstash, Kibana)
EKL은 Elasticsearch, Kibana, Logstash를 일컫는 말이다.\
ElasticSearch은 아파치 루씬기반의 오픈소스형 검색기반 엔진이다.\
간단하게 Elasticsearch는 분석 및 저장 기능, Logstash는 수집담당, Kibana는 시각화 하는 도구이다.\
나는 각각 ElasticSearch, Kibana, Logstash를 도커화 시켜 이미지를 만든 후 docker-compose를 이용하여 같은 네트워크 환경에서 run을 하게끔 만들었다.(설명이 이상하네요..)

## ElasticSearch
### DockerFile
    FROM elasticsearch:7.16.3
    RUN bin/elasticsearch-plugin install --batch analysis-nori ## 한글 형태소 분석기
    RUN bin/elasticsearch-plugin install --batch https://github.com/hongsub95/lib_2023/raw/main/docs/javacafe-analyzer-7.16.3.zip

## Kibana
### DockerFile
    FROM kibana:7.16.3
## Logstash
### Dockerfile
    FROM logstash:7.16.3
### logstash config
로그 스태시 구성에는 입력(input)플러그인과 출력(output)플러그인이 있어야 한다.\
나는 jdbc driver를 이용하여 db에 접속 하겠다.

    # 아래와 같은 설정이 없다면 로그스태시는 매번 업데이트된 데이터만 elasticsearch에 보내는 것이 아닌 처음부터 끝까지 다 보낼 것이다. 즉 낭비다.
    input {
      jdbc {  
        jdbc_driver_library => "/usr/share/logstash/vendor/jar/jdbc/mysql-connector-j-8.0.31.jar"
        jdbc_driver_class => "com.mysql.jdbc.Driver"
        jdbc_connection_string => "jdbc:mysql://192.168.254.16:3306/subbly"   # jdbc:mysql://db host ip:db포트(default는 3306)/db이름
        jdbc_user => "root"                                                   # db 유저명
        jdbc_password => "ghdtjq123"                                          # db 패스워드
        jdbc_paging_enabled => true
        tracking_column => "unix_ts_in_secs_1"                                # 로그스태시가 db로부터 읽은 마지막 문서를 추적하는데 사용
        use_column_value => true
        tracking_column_type => "numeric"
        last_run_metadata_path => "/usr/share/logstash/.logstash_jdbc_last_run_1"
        schedule => "* * * * *"                                               # 로그스태시가 '*' 개수의 초(seconds)마다 db와 접촉하라는 의미 
        jdbc_validate_connection => true
        statement => "SELECT P.*, UNIX_TIMESTAMP(P.updated) AS unix_ts_in_secs_1 FROM clothes_clothes AS P WHERE P.updated > FROM_UNIXTIME(:sql_last_value) AND P.updated < NOW() ORDER BY P.updated ASC"
        type => "subbly___clothes_clothes_type_1___v1"                        # type은 db의 테이블로 생각하자
      }
      jdbc {
        jdbc_driver_library => "/usr/share/logstash/vendor/jar/jdbc/mysql-connector-j-8.0.31.jar"
        jdbc_driver_class => "com.mysql.jdbc.Driver"
        jdbc_connection_string => "jdbc:mysql://192.168.254.16:3306/subbly"
        jdbc_user => "root"
        jdbc_password => "ghdtjq123"
        jdbc_paging_enabled => true
        tracking_column => "unix_ts_in_secs_2"
        use_column_value => true
        tracking_column_type => "numeric"
        last_run_metadata_path => "/usr/share/logstash/.logstash_jdbc_last_run_2"
        schedule => "* * * * *"
        jdbc_validate_connection => true
        statement => "SELECT P.*, M.name AS market_name, PCI.name AS category_name, UNIX_TIMESTAMP(P.updated) AS unix_ts_in_secs_2 FROM clothes_clothes AS P INNER JOIN markets_market AS M ON P.market_id = M.id INNER JOIN clothes_categories AS PCI ON P.category_id = PCI.id WHERE P.updated > FROM_UNIXTIME(:sql_last_value) AND P.updated < NOW() ORDER BY P.updated ASC"
        type => "subbly___clothes_clothes_type_2___v1"
      }
    }
    output {
      if [type] == "subbly___clothes_clothes_type_1___v1" {
        elasticsearch {
          hosts => "elasticsearch:9200"
          user => "elastic"
          password => "elasticpassword"
          index => "subbly___clothes_clothes_type_1___v1"
          document_id => "%{id}"
        }
      }
      if [type] == "subbly___clothes_clothes_type_2___v1" {
        elasticsearch {
          hosts => "elasticsearch:9200"
          user => "elastic"
          password => "elasticpassword"
          index => "subbly___clothes_clothes_type_2___v1"
          document_id => "%{id}"
        }
      }
    }
## docker-compose
    version: '3'

    services:
      elasticsearch:
        restart: unless-stopped
        build: ./elasticsearch
        container_name: elasticsearch 
        volumes:
          - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro,z
          - ./elasticsearch/config/dict.txt:/usr/share/elasticsearch/config/dict.txt
          - ./elasticsearch/data:/usr/share/elasticsearch/data
        environment:
          - TZ=Asia/Seoul
          - ELASTIC_PASSWORD=elasticpassword
          - node.name=elasticsearch 
          - bootstrap.memory_lock=true
          - discovery.type=single-node 
          - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
        ulimits:
          memlock:
            soft: -1
            hard: -1
        ports:
          - 9200:9200 

      kibana:
        restart: unless-stopped
        build: ./kibana
        container_name: kibana
        environment:
          - TZ=Asia/Seoul
        volumes:
          - ./kibana/config/kibana.yml:/usr/share/kibana/config/kibana.yml:ro,z
        ports:
          - "5601:5601" 
        depends_on:
          - elasticsearch

      logstash:
        restart: unless-stopped
        build: ./logstash
        container_name: logstash
        volumes:
          - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro,z
          - ./logstash/pipeline:/usr/share/logstash/pipeline:ro,z
          - ./logstash/drivers/:/usr/share/logstash/vendor/jar/jdbc/
        environment:
          - TZ=Asia/Seoul
          - "LS_JAVA_OPTS=-Xmx256m -Xms256m"
        depends_on:
          - elasticsearch

## DB세팅
    CREATE DATABASE subbly;

    USE subbly;

    DROP TABLE IF EXISTS clothes_clothes;

    CREATE TABLE clothes_clothes (
      id BIGINT(20) NOT NULL AUTO_INCREMENT,
      created DATETIME(6) NOT NULL,
      updated DATETIME(6) NOT NULL,
      name VARCHAR(100) NOT NULL,
      description TEXT NOT NULL,
      price INT(10) UNSIGNED NOT NULL CHECK (`price` >= 0),
      category_id BIGINT(20) NOT NULL,
      market_id BIGINT(20) NOT NULL,
      PRIMARY KEY (id)
    );

    ALTER TABLE subbly.clothes_clothes ADD INDEX (updated); 

    INSERT INTO clothes_clothes(id,created,updated,name,description,price,category_id,market_id) VALUES 
    (1,2023-01-12 08:55:51.328853,2023-01-12 08:55:51.328863,맨투맨1,요새 핫한 맨투맨,25000,1,2),
    (2,2023-01-12 08:55:51.334206,2023-01-12 08:55:51.334217,맨투맨2,누구나 소화 가능한 맨투맨,32000,1,2),
    (3,2023-01-12 08:55:51.337782,2023-01-12 08:55:51.337794,반팔1,여름에 입으면 시원한 반팔,18000,1,1),
    (4,2023-01-12 08:55:51.341518,2023-01-12 08:55:51.341529,반팔2,인스타에서 핫한 반팔,13000,1,3),
    (5,2023-01-12 08:55:51.346587,2023-01-12 08:55:51.346598,셔츠1,핏이 좋은 셔츠,40000 ,1,1),
    (6,2023-01-12 08:55:51.348277,2023-01-12 08:55:51.348288 ,셔츠2 ,오피스룩에 잘 어울리는 셔츠,45000,1,2),
    (7,2023-01-12 08:55:51.350812,2023-01-12 08:55:51.350823 ,슬랙스1,기능성 좋은 슬랙스,28000 ,2,1),
    (8,2023-01-12 08:55:51.354807,2023-01-12 08:55:51.354819 ,슬랙스2,연예인들이 많이 입는 슬랙스,25000,2,1),
    (9,2023-01-12 08:55:51.358756,2023-01-12 08:55:51.358768 ,블랙진, 무슨 옷을 입든 잘 어울리는 블랙진,30000,2,2),
    (10,2023-01-12 08:55:51.362453,2023-01-12 08:55:51.362465,청바지,여름에 입어도 시원한 청바지,23000,2,3),
    (11,2023-01-12 08:55:51.366308,2023-01-12 08:55:51.366320,아우터1,겨울에 따뜻하게 입을 수 있는 롱코트,105000,5,2),
    (12,2023-01-12 08:55:51.375494,2023-01-12 08:55:51.375505,아우터2,가을에 너무 잘 어울리는 코트,77000,5,2),
    (12,2023-01-12 08:55:51.375494,2023-01-12 08:55:51.375505,아우터2,가을에 너무 잘 어울리는 코트,77000,5,2),
    (14,2023-01-12 08:55:51.382075,2023-01-12 08:55:51.382086,아우터4,깔끔하게 입을 수 있는 블레이져,43000,5,2),
    (15,2023-01-12 08:55:51.384738,2023-01-12 08:55:51.384749,신발1, XX사에서 나온 깔끔한 디자인의 신발,89000,3,1),
    (16,2023-01-12 08:55:51.393252,2023-01-12 08:55:51.393264,신발2,봄에 신으면 이쁜 신발,53000,3,3),
    (17,2023-01-12 08:55:51.399009,2023-01-12 08:55:51.399021,신발3, 모든 바지에 잘 어울리는 단화,63000,3,2),
    (18,2023-01-12 08:55:51.404779 , 2023-01-12 08:55:51.404791,치마1,인스타에서 핫한 치마,43000,4,2),
    (19,2023-01-25 17:18:20.404791 , 2023-01-25 17:18:20.404791 , 치마2, 걸그룹이 잘 입는 치마,30000,4,2);


    DROP TABLE IF EXISTS `markets_market`;

    CREATE TABLE markets_market (
      id bigint(20) NOT NULL AUTO_INCREMENT,
      created datetime(6) NOT NULL,
      updated datetime(6) NOT NULL,
      name varchar(100) NOT NULL,
      phone_number INT(11) DEFAULT NULL,
      market_url varchar(100) NOT NULL,
      description longtext NOT NULL,
      master_id bigint(20) NOT NULL,
      PRIMARY KEY (id),
      UNIQUE KEY master_id (master_id)
    );`

    insert into markets_market(id,created,updated,name,phone_number,maket_url,description,master_id) values 
    (1,2023-01-12 08:55:51.312052,2023-01-12 08:55:51.312064,형아네옷가게,NULL,https://www.abc1.co.kr,형아네와 함께 멋진 스타일을 완성해보세요. #간편한 룩 #2030 #판교,2),
    (2,2023-01-12 08:55:51.312790,2023-01-12 08:55:51.312811,누나네옷가게,NULL,https://www.abc2.co.kr,편한 스타일링을 추구합니다. #일상 #미니멀 #VLOG,3),
    (3,2023-01-12 08:55:51.313540,2023-01-12 08:55:51.313724,이모네옷가게,NULL,https://www.abc3.co.kr,화려한 스타일을 추구합니다. #인스타여신 #트위터여신 #판교,4);

    DROP TABLE IF EXISTS clothes_categories;

    CREATE TABLE `products_productcategoryitem` (
      id bigint(20) NOT NULL AUTO_INCREMENT,
      created datetime(6) NOT NULL,
      updated datetime(6) NOT NULL,
      name varchar(50) NOT NULL,
      PRIMARY KEY (id)
    );

    /*Data for the table `products_productcategoryitem` */

    insert  into clothes_categories(id,created,updated,name) values 
    (1,2023-01-12 08:55:51.326675,2023-01-12 08:55:51.326688,상의),
    (2,2023-01-12 08:55:51.327102,2023-01-12 08:55:51.327113,하의),
    (3,2023-01-12 08:55:51.327292,2023-01-12 08:55:51.327300,신발),
    (4,2023-01-12 08:55:51.327437,2023-01-12 08:55:51.327444,원피스),
    (5,2023-01-12 08:55:51.327673,2023-01-12 08:55:51.327685,아우터);

## 인덱스 실행 
host ip:5601로 들어가 키바나 실행 후 ID, 비번 입력 후 실행
tokenizer: 해당 단어들을 분리 
token filter: 분리된 token들을 가공
analyzer: tokenizer + token filter 
예를들면, 밑에 나오겠지만 tokenizer는 nori, filter는 chosung을 했을 경우, text:["나는 개발자"]를 넣을 경우, nori tokenizer로 인해\
["나","는","개발자","개발","자"]로 나뉘어 지고 filter를 거치면 ["ㄴ","ㄱㅂㅈ","ㄱㅂ","ㅈ"]가 나온다

    GET /_cat/indices  #인덱스 목록

    # 인덱스 삭제
    DELETE /subbly___clothes_clothes_type_1___v1

    # 인덱스 생성 및 설정
    PUT /subbly___clothes_clothes_type_1___v1
    {
      "settings": {
        "index": {
          "number_of_shards": 5,
          "number_of_replicas": 1
        },
        "analysis": {
          "analyzer": {
            "nori_analyzer": {
              "type": "custom",
              "tokenizer": "nori_tokenizer",
              "filter": "nori_filter"
            }
          },
          "tokenizer": {
            "nori_tokenizer": {
              "type": "nori_tokenizer",
              "decompound_mode": "mixed",
              "user_dictionary": "dict.txt"
            }
          },
          "filter": {
            "nori_filter": {
              "type": "nori_part_of_speech",
              "stoptags": [
                "E", "IC", "J", "MAG", "MAJ", "MM", "SP", "SSC", "SSO", "SC", "SE", "XPN", "XSA", "XSN", "XSV", "UNA", "NA", "VSV"
              ]
            }
          }
        }
      }
    }

    # 타입 설정(엘라스틱 서치 7.0 부터 인덱스에 타입 1개만 설정 가능)
    PUT /subbly___clothes_clothes_type_1___v1/_mappings
    {
      "properties": {
        "id": {
          "type": "long"
        },
        "name": {
          "type": "keyword",
          "copy_to": ["name_nori"]
        },
        "name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "description": {
          "type": "keyword",
          "copy_to": ["description_nori"]
        },
        "description_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "category_id": {
          "type": "integer"
        },
        "market_id": {
          "type": "integer"
        },
        "price": {
          "type": "integer"
        }
      }
    }

    # 인덱스 확인
    GET /subbly___clothes_clothes_type_1___v1

    # 인덱스 안의 데이터 개수 확인
    GET _sql?format=json
    {
      "query": """
      SELECT count(*) FROM subbly___clothes_clothes_type_1___v1 
      """
    } 
## 인덱스 실행2
    DELETE /subbly___clothes_clothes_type_2___v1

    # 인덱스 설정
    PUT /subbly___clothes_clothes_type_2___v1
    {
      "settings": {
        "index": {
          "number_of_shards": 5,
          "number_of_replicas": 1
        },
        "analysis": {
          "analyzer": {
            "nori_analyzer": {
              "type": "custom",
              "tokenizer": "nori_tokenizer",
              "filter": "nori_filter"
            }
          },
          "tokenizer": {
            "nori_tokenizer": {
              "type": "nori_tokenizer",
              "decompound_mode": "mixed",
              "user_dictionary": "dict.txt"
            }
          },
          "filter": {
            "nori_filter": {
              "type": "nori_part_of_speech",
              "stoptags": [
                "E", "IC", "J", "MAG", "MAJ", "MM", "SP", "SSC", "SSO", "SC", "SE", "XPN", "XSA", "XSN", "XSV", "UNA", "NA", "VSV"
              ]
            }
          }
        }
      }
    }

    # 타입설정
    PUT /subbly___clothes_clothes_type_2___v1/_mappings
    {
      "properties": {
        "id": {
          "type": "long"
        },
        "name": {
          "type": "keyword",
          "copy_to": ["name_nori"]
        },
        "name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "description": {
          "type": "keyword",
          "copy_to": ["description_nori"]
        },
        "description_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "market_name": {
          "type": "keyword",
          "copy_to": ["market_name_nori"]
        },
        "market_name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "category_name": {
          "type": "keyword",
          "copy_to": ["catetegory_name_nori"]
        },
        "category_name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "price": {
          "type": "integer"
        }
      }
    }

    # 인덱스 확인
    GET /subbly___clothes_clothes_type_2___v1

    # 데이터 개수
    GET _sql?format=json
    {
      "query": """
      SELECT COUNT(*) FROM subbly___clothes_clothes_type_2___v1
      """
    }
## 엘라스틱에서 SQL 실행
    # subbly___clothes_clothes_type_1___v1 에서 `인스타`로 키워드, 카테고리, 가격까지 검색
    GET _sql?format=json
    {
      "query": """
      SELECT score() AS score, * FROM subbly___clothes_clothes_type_1___v1
      WHERE
      (
        MATCH(name_nori, '인스타')
        OR
        MATCH(description_nori, '인스타')
      )
      AND category_id = 1
  
      ORDER BY score() DESC
      """
    }

    # subbly___clothes_clothes_type_2___v1 에서 `연예인`로 키워드 검색(마켓명과 카테고리 명까지 검색대상에 포함)
    GET _sql?format=json
    {
      "query": """
      SELECT score() AS score, * FROM subbly___clothes_clothes_type_2___v1
      WHERE
      (
        MATCH(name_nori, '연예인')
        OR
        MATCH(description_nori, '연예인')
        OR
        MATCH(market_name_nori, '연예인')
        OR
        MATCH(category_name_nori, '연예인')
      )
      ORDER BY score() DESC
      """
    }
## 인덱스에 자모검색, 초성검색 적용하기
만약 테이블이 수정되었거나, 사전데이터(dict.txt)가 추가 된다면, 새로운 인덱스를 만든 후 모든 데이터가 잘 들어 오도록 세팅 완료 후 교체\
하지만 테이블은 그대로인데 신조어만 추가된 상태라면? => reindex라는 명령어를 통해 기존 인덱스의 데이터를 새 인덱스로 가져 올 수 있다.\
주의 해야 할 점은 데이터만 옮길 뿐 인덱스는 새로 만들어야함.(type포함) 밑에서 적용해 보자\
인덱스 이름이 바뀔때, 알리아싱(alias)을 통해 소스코드에 하드코딩되어 있는 인덱스 이름을 수정하는 작업을 안할수 있다.

    #인덱스 설정
    PUT /subbly___clothes_clothes_type_2___v2
    {
      "settings":{
        "index":{
          "number_of_shards":5,
          "number_of_replicas":1
        },
        "analysis": {
          "analyzer": {
            "nori_analyzer": {
              "type":"custom",
              "tokenizer": "nori_tokenizer",
              "filter": "nori_filter"
            },
            "jamo_analyzer": {
              "type": "custom",
              "tokenizer": "nori_tokenizer",
              "filter": ["nori_filter", "jamo_filter", "lowercase"]
            },
            "chosung_analyzer": {
              "type": "custom",
              "tokenizer": "nori_tokenizer",
              "filter": ["nori_filter", "chosung_filter", "lowercase"]
            }
          },
          "tokenizer": {
            "nori_tokenizer": {
              "type": "nori_tokenizer",
              "decompound_mode": "mixed",
              "user_dictionary": "dict.txt"
            }
          },
          "filter": {
            "nori_filter": {
              "type": "nori_part_of_speech",
              "stoptags": [
                "E", "IC", "J", "MAG", "MAJ", "MM", "SP", "SSC", "SSO", "SC", "SE", "XPN", "XSA", "XSN", "XSV", "UNA", "NA", "VSV"
              ]
            },
            "jamo_filter": {
              "type": "javacafe_jamo"
            },
            "chosung_filter": {
              "type": "javacafe_chosung"
            }
          }
        }
      }
    }

    # 타입설정
    PUT /subbly___clothes_clothes_type_2___v2/_mappings
    {
      "properties": {
        "id": {
          "type": "long"
        },
        "name": {
          "type": "keyword",
          "copy_to": ["name_nori", "name_jamo", "name_chosung"]
        },
        "name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "name_jamo": {
          "type": "text",
          "analyzer": "jamo_analyzer",
          "search_analyzer": "standard"
        },
        "name_chosung": {
          "type": "text",
          "analyzer": "chosung_analyzer",
          "search_analyzer": "standard"
        },
        "description": {
          "type": "keyword",
          "copy_to": ["description_nori", "description_jamo", "description_chosung"]
        },
        "description_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "description_jamo": {
          "type": "text",
          "analyzer": "jamo_analyzer",
          "search_analyzer": "standard"
        },
        "description_chosung": {
          "type": "text",
          "analyzer": "chosung_analyzer",
          "search_analyzer": "standard"
        },
        "market_name": {
          "type": "keyword",
          "copy_to": ["market_name_nori", "market_name_jamo", "market_name_chosung"]
        },
        "market_name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "market_name_jamo": {
          "type": "text",
          "analyzer": "jamo_analyzer",
          "search_analyzer": "standard"
        },
        "market_name_chosung": {
          "type": "text",
          "analyzer": "chosung_analyzer",
          "search_analyzer": "standard"
        },
        "category_name": {
          "type": "keyword",
          "copy_to": ["category_name_nori", "category_jamo", "category_chosung"]
        },
        "category_name_nori": {
          "type": "text",
          "analyzer": "nori_analyzer"
        },
        "category_name_jamo": {
          "type": "text",
          "analyzer": "jamo_analyzer",
          "search_analyzer": "standard"
        },
        "category_name_chosung": {
          "type": "text",
          "analyzer": "chosung_analyzer",
          "search_analyzer": "standard"
        },
        "price": {
          "type": "integer"
        }
      }
    }

## 상품명 검색에 일반검색, 자모검색, 초성검색 동시적용
### 입력
    GET _sql?format=json
    {
      "query": """
      SELECT score() AS score, *
      FROM subbly___clothes_clothes_type_2___v2
      WHERE
      (
        MATCH(name_nori, 'ㅁㅐㄴㅌㅜㅁㅐㄴ')
        OR
        MATCH(name_jamo, 'ㅁㅐㄴㅌㅜㅁㅐㄴ')
        OR
        MATCH(name_chosung, 'ㅁㅐㄴㅌㅜㅁㅐㄴ')
      )
      ORDER BY score() DESC
      """
    }
    
### 출력
      "rows" : [
    [
      1.2039728,
      "2023-01-30T09:18:00.896Z",
      "1",
      "상의",
      1,
      "상의",
      "상의",
      null,
      null,
      "상의",
      "2023-01-11T23:55:51.328Z",
      "요새 핫한 맨투맨",
      "요새 핫한 맨투맨",
      "요새 핫한 맨투맨",
      "요새 핫한 맨투맨",
      1,
      2,
      "누나네옷가게",
      "누나네옷가게",
      "누나네옷가게",
      "누나네옷가게",
      "맨투맨1",
      "맨투맨1",
      "맨투맨1",
      "맨투맨1",
      25000,
      "subbly___clothes_clothes_type_2___v1",
      1.67348134E9,
      "2023-01-11T23:55:51.328Z"
    ],
    [
      0.6931471,
      "2023-01-30T09:18:00.899Z",
      "1",
      "상의",
      1,
      "상의",
      "상의",
      null,
      null,
      "상의",
      "2023-01-11T23:55:51.334Z",
      "누구나 소화 가능한 맨투맨",
      "누구나 소화 가능한 맨투맨",
      "누구나 소화 가능한 맨투맨",
      "누구나 소화 가능한 맨투맨",
      2,
      2,
      "누나네옷가게",
      "누나네옷가게",
      "누나네옷가게",
      "누나네옷가게",
      "맨투맨2",
      "맨투맨2",
      "맨투맨2",
      "맨투맨2",
      32000,
      "subbly___clothes_clothes_type_2___v1",
      1.67348134E9,
      "2023-01-11T23:55:51.334Z"
    ]
  ]

## reindex, aliase 적용해 보기
alias 후 logstash config output index 수정해야함

    # 기존 인덱스에서 값 받아오기
    POST _reindex
    {
      "source": {
        "index": "subbly___clothes_clothes_type_2___v1"
      },
      "dest": {
        "index": "subbly___clothes_clothes_type_2___v2"
      }
    }

    #별칭 추가
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "subbly___clothes_clothes_type_2___v1",
            "alias": "subbly___clothes_clothes_type_2"
          }
        }
      ]
    }


    # 별칭에 존재하던 연결을 삭제하고 새 인덱스 연결
    POST _aliases
    {
      "actions": [
        {
          "remove": {
            "index": "subbly___clothes_clothes_type_2___v1",
            "alias": "subbly___clothes_clothes_type_2"
          }
        },
        {
          "add": {
            "index": "subbly___clothes_clothes_type_2___v2",
            "alias": "subbly___clothes_clothes_type_2"
          }
        }
      ]
    }

    #별칭으로 인덱스 확인
    GET subbly___clothes_clothes_type_2


    # 인덱스 안의 데이터 개수 확인 => 19개로 잘나옴
    GET _sql?format=json
    {
      "query": """
      SELECT COUNT(*) FROM subbly___clothes_clothes_type_2
      """
    }


        
        
