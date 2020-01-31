# Arknights Planner

명일방주 최적 파밍 모델

## Backgrounds

  - 알고리즘 원리는 [문서](https://www.notion.so/djshin/24637514c15f4244bd59d2d6513ce12c) 참고
  - 드랍률 정보는 [Penguin Statistics](https://penguin-stats.io/)에서 긁어와서 사용

## Resources

  - `data`
    - `items.json` : 재화 목록
    - `summary.json`: 지역별 재화 드랍률
    - `transform.json`: 가공소 조합식
    - `translation.json`: 재화 영문 - 국문 변환표
  - `inputs`
    - `requirement_items.json`: 파밍 목표 재화 목록
    - `respawn_items.json`: 단위시간당 자연재생 재화 목록

## Prerequisite

  - `pip install -r requirements.txt`
  - 파밍 지역 목록
    - 기본으로 스토리 1-4지역 + '기병과 사냥꾼' 이벤트 지역만 사용
    - 바꾸고 싶다면 `crawler.py`에서 `stage_ids`를 [penguin-stats API](https://github.com/penguin-statistics/backend/blob/master/penguin-stats%20API%20v1.2.2.md)를 참고하여 원하는 대로 수정하고 `python crawler.py` 실행

## Execute

  - `python main.py`
