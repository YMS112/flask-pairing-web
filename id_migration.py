import json
import os
import uuid

data_file = 'people.json'

if os.path.exists(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        people = json.load(f)

    updated = False
    for person in people:
        if 'id' not in person:
            person['id'] = str(uuid.uuid4())  # 고유 ID 생성
            updated = True

    if updated:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(people, f, ensure_ascii=False, indent=2)
        print("✅ ID 필드가 추가된 데이터를 저장했습니다.")
    else:
        print("ℹ️ 모든 사람에게 이미 ID가 있습니다.")
else:
    print("❌ people.json 파일이 없습니다.")
