import json

with open("test_srp.json", "r", encoding="utf-8") as f:
    test_record = json.load(f)
goodscode = test_record[0]["case1"]["상품번호"]
click_time = test_record[0]["case1"]["click"]
print(goodscode,click_time)