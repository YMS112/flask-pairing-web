import json
import uuid

# 기존 JSON 파일 경로
filename = 'people.json'

# 기존 데이터 불러오기
with open(filename, 'r', encoding='utf-8') as f:
    people = json.load(f)

# 각 사람에 대해 UUID 추가
for person in people:
    if 'id' not in person:
        person['id'] = str(uuid.uuid4())

# 덮어쓰기 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(people, f, ensure_ascii=False, indent=2)

print("모든 항목에 'id'가 추가되었습니다.")
