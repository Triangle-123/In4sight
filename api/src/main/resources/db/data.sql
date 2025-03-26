INSERT INTO customer (customer_name, phone_number, address)
VALUES ('박싸피', '010-1234-0001', '서울시 종로구 종로1가 1-1'),
       ('김싸피', '010-1234-0002', '서울시 강남구 삼성동 23-5'),
       ('이싸피', '010-1234-0003', '서울시 서초구 서초동 99-12'),
       ('최싸피', '010-1234-0004', '서울시 마포구 합정동 88-3'),
       ('정싸피', '010-1234-0005', '서울시 용산구 한남동 45-7');

-- INSERT INTO device (serial_number, customer_id, product_type, model_suffix, model_name, launch_date)
-- VALUES ('test_001', 1, 'REF', 'RM70F63R2A', 'BESPOKE 냉장고 4도어 키친핏 Max 640L', '2025-03-01'),
--        ('test_002', 1, 'REF', 'RM70F64Q1A', 'BESPOKE AI 하이브리드 4도어 키친핏 Max 623L', '2025-03-01'),
--        ('test_003', 2, 'REF', 'RM90F64E2W', 'BESPOKE AI 하이브리드 4도어 키친핏 Max 602L', '2025-02-01'),
--        ('test_004', 3, 'REF', 'RF85DB91D1AP', 'BESPOKE 냉장고 4도어 869L', '2024-03-01'),
--        ('test_005', 3, 'REF', 'RF90DG90124W', 'BESPOKE 냉장고 4도어 905L', '2024-03-01'),
--        ('test_006', 4, 'REF', 'RF90DG9111S9', 'BESPOKE 냉장고 4도어 902L', '2024-03-01'),
--        ('test_007', 4, 'REF', 'RF85DB90B1AP', 'BESPOKE 냉장고 4도어 875L', '2024-03-01'),
--        ('test_008', 5, 'REF', 'RF85DB95A2APW', 'BESPOKE AI 패밀리허브 4도어 861L', '2024-05-01');
INSERT INTO device (serial_number, customer_id, product_type, model_suffix, model_name, launch_date)
VALUES ('defrost', 1, 'REF', 'RM70F63R2A', 'BESPOKE 냉장고 4도어 키친핏 Max 640L', '2025-03-01'),
       ('door', 1, 'REF', 'RM70F64Q1A', 'BESPOKE AI 하이브리드 4도어 키친핏 Max 623L', '2025-03-01'),
       ('hot', 2, 'REF', 'RM90F64E2W', 'BESPOKE AI 하이브리드 4도어 키친핏 Max 602L', '2025-02-01'),
       ('door', 3, 'REF', 'RF85DB91D1AP', 'BESPOKE 냉장고 4도어 869L', '2024-03-01'),
       ('load', 3, 'REF', 'RF90DG90124W', 'BESPOKE 냉장고 4도어 905L', '2024-03-01'),
       ('load', 4, 'REF', 'RF90DG9111S9', 'BESPOKE 냉장고 4도어 902L', '2024-03-01'),
       ('refrigerant', 4, 'REF', 'RF85DB90B1AP', 'BESPOKE 냉장고 4도어 875L', '2024-03-01'),
       ('refrigerant', 5, 'REF', 'RF85DB95A2APW', 'BESPOKE AI 패밀리허브 4도어 861L', '2024-05-01');
