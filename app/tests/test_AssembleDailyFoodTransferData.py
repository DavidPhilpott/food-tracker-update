from app.Domain_Actions.AssembleDailyFoodTransferData import assemble_daily_food_transfer_data


class TestAssembleDailyFoodTransferData:
    def test_can_assemble_data_correctly(self, test_state):
        test_state.set({"date_value": "01-Jan-2000"})
        test_state.set({"daily_auto_worksheet_all_values":
                            [["Item", "No.", "Size", "C", "P", "V"],
                             ["Auto 1", "1", "Auto 1", "Auto 1", "Auto 1", "Auto 1"]]})
        test_state.set({"daily_manual_worksheet_all_values":
                            [["Item", "No.", "C", "P", "V", "C", "P", "V"],
                             ["Manual 1", "1", "1", "2", "3", "1", "2", "3"]]})
        assemble_daily_food_transfer_data(test_state)
        expected_values = [['Date', 'Item', 'Number', 'Cal', 'Prot', 'Veg'],
                           ["01-Jan-2000", "Auto 1", "1", "", "", ""],
                           ["01-Jan-2000", "Manual 1", "1", "1", "2", "3"]]
        assert test_state.get("food_daily_transfer_data") == expected_values
