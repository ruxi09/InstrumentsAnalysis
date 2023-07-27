import unittest
import csv
from io import StringIO
from Skeleton import Instrument, loadData, printSummary

# Create a sample CSV data for testing
sample_csv_data = """
1627283888,ABC,100,50
1627283889,XYZ,200,75
1627283890,ABC,150,60
1627283891,XYZ,250,80
1627283892,ABC,200,70
"""

class TestInstrumentClass(unittest.TestCase):

    def test_addTrade(self):
        instrument = Instrument('TEST')
        self.assertEqual(instrument.totalVolume, 0)
        self.assertEqual(instrument.totalPrice, 0)
        self.assertEqual(instrument.tradeCount, 0)

        # Add some trades and verify the attributes are updated correctly
        instrument.addTrade(100, 50)
        self.assertEqual(instrument.totalVolume, 100)
        self.assertEqual(instrument.totalPrice, 5000)
        self.assertEqual(instrument.tradeCount, 1)

        instrument.addTrade(150, 60)
        self.assertEqual(instrument.totalVolume, 250)
        self.assertEqual(instrument.totalPrice, 14000)
        self.assertEqual(instrument.tradeCount, 2)

        instrument.addTrade(200, 70)
        self.assertEqual(instrument.totalVolume, 450)
        self.assertEqual(instrument.totalPrice, 28000)
        self.assertEqual(instrument.tradeCount, 3)

    def test_getAveragePrice(self):
        instrument = Instrument('TEST')

        # Initially, average price should be 0 as no trades have been added
        self.assertEqual(instrument.getAveragePrice(), 0)

        # Add some trades
        instrument.addTrade(100, 50)
        instrument.addTrade(150, 60)
        instrument.addTrade(200, 70)

        # Calculate the average price manually and compare with the method result
        expected_average = (100 * 50 + 150 * 60 + 200 * 70) / 450
        self.assertEqual(instrument.getAveragePrice(), expected_average)

    def test_printSummary(self):
        instrument = Instrument('TEST')
        instrument.addTrade(100, 50)
        instrument.addTrade(150, 60)
        instrument.addTrade(200, 70)

        # Mock the print function to capture its calls
        print_summary = instrument.printSummary()

        # Join the captured lines to create the expected output
        expected_output = 'Symbol: TEST Max Price: 70 Min Price: 50 Average Price: 62 Total Volume: 450'
        
        # Compare the output with the expected result
        self.assertEqual(print_summary, expected_output)

class TestLoadDataAndPrintSummary(unittest.TestCase):

    def test_printSummary(self):
        # Create some instrument objects and add trades to them
        instrument1 = Instrument('ABC')
        instrument1.addTrade(100, 50)
        instrument1.addTrade(150, 60)

        instrument2 = Instrument('XYZ')
        instrument2.addTrade(200, 70)

        # Create the symbols dictionary with the instruments
        symbols = {
            'ABC': instrument1,
            'XYZ': instrument2,
        }

        # Call the printSummary function to get the summary
        summary = printSummary(symbols)

        # Define the expected output based on the added trades
        expected_output = (
            'Symbol: ABC Max Price: 60 Min Price: 50 Average Price: 56 Total Volume: 250\n'
            'Symbol: XYZ Max Price: 70 Min Price: 70 Average Price: 70 Total Volume: 200'
        )

        # Compare the output with the expected result
        self.assertEqual(summary, expected_output)

if __name__ == '__main__':
    unittest.main()
