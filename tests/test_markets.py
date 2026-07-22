import unittest

from scripts.update_markets import (
    build_butter,
    build_eggs,
    build_pigmeat,
    build_poultry,
    build_wheat,
    parse_eu_price,
    percentage_change,
    select_series,
    eu_date,
)


class MarketDataTests(unittest.TestCase):
    def test_parses_dot_and_comma_price_formats(self):
        self.assertEqual(parse_eu_price("€200,00"), 200.0)
        self.assertEqual(parse_eu_price("€1.265,40"), 1265.4)
        self.assertEqual(parse_eu_price("€1265.40"), 1265.4)

    def test_percentage_change_is_guarded_and_rounded(self):
        self.assertEqual(percentage_change(202.5, 200), 1.2)
        self.assertEqual(percentage_change(198, 200), -1.0)
        self.assertIsNone(percentage_change(10, 0))

    def test_series_is_sorted_filtered_and_deduplicated(self):
        records = [
            {"kind": "keep", "endDate": "14/01/2026", "price": "€110,00"},
            {"kind": "skip", "endDate": "21/01/2026", "price": "€999,00"},
            {"kind": "keep", "endDate": "07/01/2026", "price": "€100,00"},
            {"kind": "keep", "endDate": "14/01/2026", "price": "€111,00"},
        ]
        result = select_series(
            records,
            lambda row: row["kind"] == "keep",
            date_field="endDate",
            date_parser=eu_date,
        )
        self.assertEqual(result, [
            {"date": "2026-01-07", "value": 100.0},
            {"date": "2026-01-14", "value": 111.0},
        ])

    def test_wheat_uses_austria_national_average_only(self):
        rows = [
            {
                "memberStateCode": "AT", "productName": "Breadmaking common wheat",
                "marketName": "National Average", "endDate": "12/07/2026", "price": "€197,50",
            },
            {
                "memberStateCode": "AT", "productName": "Breadmaking common wheat",
                "marketName": "National Average", "endDate": "19/07/2026", "price": "€200,00",
            },
            {
                "memberStateCode": "AT", "productName": "Breadmaking common wheat",
                "marketName": "Wien", "endDate": "19/07/2026", "price": "€999,00",
            },
        ]
        result = build_wheat(rows)
        self.assertEqual(result["value"], 200.0)
        self.assertEqual(result["change_pct"], 1.3)
        self.assertEqual(result["scope"], "Austria")
        self.assertEqual(result["display_decimals"], 0)

    def test_hospitality_input_series_use_the_intended_product(self):
        dates = ("12/07/2026", "19/07/2026")
        eggs = build_eggs([
            {"memberStateCode": "AT", "farmingMethod": "Barn", "endDate": dates[0], "price": "€300,00"},
            {"memberStateCode": "AT", "farmingMethod": "Barn", "endDate": dates[1], "price": "€315,00"},
            {"memberStateCode": "AT", "farmingMethod": "Organic", "endDate": dates[1], "price": "€999,00"},
        ])
        poultry = build_poultry([
            {"memberStateCode": "AT", "productName": "Whole broiler (65%)", "priceType": "Selling price", "endDate": dates[0], "price": "€350,00"},
            {"memberStateCode": "AT", "productName": "Whole broiler (65%)", "priceType": "Selling price", "endDate": dates[1], "price": "€360,00"},
        ])
        pigmeat = build_pigmeat([
            {"memberStateCode": "AT", "pigClass": "E", "endDate": dates[0], "price": "€170,00"},
            {"memberStateCode": "AT", "pigClass": "E", "endDate": dates[1], "price": "€175,00"},
        ])
        butter = build_butter([
            {"memberStateCode": "EU", "product": "BUTTER", "endDate": dates[0], "price": "€380,00"},
            {"memberStateCode": "EU", "product": "BUTTER", "endDate": dates[1], "price": "€390,00"},
        ])

        self.assertEqual(eggs["value"], 315.0)
        self.assertEqual(poultry["value"], 360.0)
        self.assertEqual(pigmeat["value"], 175.0)
        self.assertEqual(butter["value"], 390.0)


if __name__ == "__main__":
    unittest.main()
