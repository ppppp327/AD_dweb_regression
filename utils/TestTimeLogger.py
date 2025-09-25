import json
from datetime import datetime
from pathlib import Path


class TestTimeLogger:
    def __init__(self, json_path: str = "test_times.json"):
        """
        :param json_path: 기록할 JSON 파일 경로
        """
        self.json_path = Path(json_path)

        # 파일이 없으면 기본 구조 생성
        if not self.json_path.exists():
            self._init_file()

    def _init_file(self):
        """기본 JSON 구조 초기화"""
        data = [
            {
                "case1": {"exposure": "", "click": ""},
                "case2": {"exposure": "", "click": ""},
                "case3": {"exposure": "", "click": ""},
            }
        ]
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def record_time(self, case_name: str, action: str):
        """
        특정 케이스와 액션(exposure/click)에 현재 시간을 기록
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # JSON 읽기
        with open(self.json_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        # 값 업데이트
        if case_name in records[0]:
            records[0][case_name][action] = now
        else:
            # case_name이 없으면 새로 추가
            records[0][case_name] = {action: now}

        # 다시 저장
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        print(f"[{case_name}] {action} 기록 완료: {now}")

    def record_goodscode(self, case_name: str, goodscode: str):
        """
        특정 케이스와 액션(exposure/click)에 현재 시간을 기록
        """
        # JSON 읽기
        with open(self.json_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        # 값 업데이트
        if case_name in records[0]:
            records[0][case_name]["상품번호"] = goodscode
        else:
            # case_name이 없으면 새로 추가
            records[0][case_name] = {"상품번호": goodscode}

        # 다시 저장
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        print(f"[{case_name}] 상품번호 기록 완료: {goodscode}")