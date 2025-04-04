DELETE FROM device;
DELETE FROM customer;

INSERT INTO customer (customer_name, phone_number, address)
VALUES ('김싸피', '010-1234-0001', '경기도 수원시 영통구 삼성로 129'),
       ('송싸피', '010-1234-0002', '경기도 수원시 영통구 삼성로 129'),
       ('윤싸피', '010-1234-0003', '경기도 수원시 영통구 삼성로 129'),
       ('홍싸피', '010-1234-0004', '경기도 수원시 영통구 삼성로 129'),
       ('조싸피', '010-1234-0005', '경기도 수원시 영통구 삼성로 129');

INSERT INTO device (serial_number, customer_id, product_type, model_suffix, model_name, launch_date)
VALUES ('REF_TEST_IncreaseRefrigeratorTemp_001', 1, 'REF', 'RM70F63R2A', 'BESPOKE 냉장고 4도어 키친핏 Max 640L', '2025-03-01'),
       ('REF_TEST_IncreaseRefrigeratorTemp_002', 1, 'REF', 'RM90F64E2W', 'BESPOKE AI 하이브리드 4도어 키친핏 Max 602L', '2025-02-01'),
       ('REF_TEST_IncreaseRefrigeratorTemp_003', 2, 'REF', 'RF85DB91D1AP', 'BESPOKE 냉장고 4도어 869L', '2024-03-01'),
       ('REF_TEST_IncreaseRefrigeratorTemp_004', 3, 'REF', 'RF90DG9111S9', 'BESPOKE 냉장고 4도어 902L', '2024-03-01'),
       ('REF_TEST_IncreaseRefrigeratorTemp_005', 4, 'REF', 'RF85DB95A2APW', 'BESPOKE AI 패밀리허브 4도어 861L', '2024-05-01'),
       ('ZMMB6CK2P7AIJF4', 5, 'REF', 'RF85DB9421AP', 'BESPOKE 냉장고 4도어 849L (빅아이스/큐브)', '2024-03-01'),
       ('SF5YT62MPO2G3DH', 5, 'REF', 'RF91DB98J1AP01', 'BESPOKE AI 하이브리드 4도어 868L (빅아이스/위스키볼)', '2024-03-01');


