import unittest
from llm import calendar_registration

class TestCalendarRegistration(unittest.TestCase):
    def test_calendar_registration(self):
        # テスト用の入力データを作成します
        input_event_data = "来週の金曜日に神田で夜８時にタカシとご飯"

        # calendar_registration関数を呼び出します
        result = calendar_registration(input_event_data)

        # 戻り値が期待通りであることを確認します
        # この例では、戻り値がGoogle CalendarのURL形式になっていることを確認します
        self.assertTrue(result.startswith("https://www.google.com/calendar/render?action=TEMPLATE"))

        # 他のアサーションを追加して、戻り値が期待通りであることを確認します
        # 例えば、特定のイベント詳細がURLに含まれていることを確認します
        # self.assertIn("テストイベントの詳細", result)

if __name__ == "__main__":
    unittest.main()