import csv 
import sys

# An instrument class that represents the data for a single symbol
class Instrument:
    def __init__(self, name):
        self.name = name
        self.maxPrice = 0
        self.minPrice = sys.maxsize
        self.totalPrice = 0
        self.tradeCount = 0
        self.totalVolume = 0

    def addTrade(self, volume, price):
        """Updates the attributes based on the new trade information

        Args:
            volume: Integer representing the volume of the trade.
            price: Integer representing the price of the trade.
        """
        self.totalVolume += volume
        self.totalPrice += volume * price
        self.tradeCount += 1

        if price > self.maxPrice:
            self.maxPrice = price

        # Set initial minPrice to the first trade's price or update if needed
        self.maxPrice = max(self.maxPrice, price)
        self.minPrice = min(self.minPrice, price)

    def getAveragePrice(self):
        """Instead of recalculating the average price from the total price and
        total volume every time a new trade is added, we can keep track of the
        cumulative sum of prices and volume and calculate the average price 
        only when it is needed in the printSummary function. This approach 
        reduces the number of divisions needed for calculating the average.
        """
        return self.totalPrice / self.totalVolume if self.totalVolume > 0 else 0

    def printSummary(self):
        """Print the summary for the instrument
        Changed it to return instead of print in order to make it easier to test the function
        """
        return ('Symbol: {} Max Price: {} Min Price: {} Average Price: {} Total Volume: {}'.format(
            self.name, self.maxPrice, self.minPrice, self.getAveragePrice(), self.totalVolume))

def loadData(symbols, inputFile):
    """Load trade data from the input CSV file and update the symbols dict.

    Args:
        symbols: Dictionary storing trade information for each symbol 
                    (symbol name : Instrument object)
        inputFile: Path to the input CSV file containing trade data.


    CSV Format: 
        <Timestamp>,<Symbol>,<Volume>,<Price>
        I used the csv library in order to optimise the execution time.
    """
    with open(inputFile) as f:
        reader = csv.reader(f)
        for lineData in reader:
            timestamp = int(lineData[0])
            symbol = lineData[1]
            volume = int(lineData[2])
            price = int(lineData[3])

            # Use setdefault to get or create the instrument object
            instrument = symbols.setdefault(symbol, Instrument(symbol))
            instrument.addTrade(volume, price)


def printSummary(symbols):
    """Returns a summary of trade information for each symbol.

    Args:
        symbols: Dictionary containing trade information for each symbol.

    Returns:
        summary: A string containing the summary information for all instruments.
    """

    # Sort symbols alphabetically
    sorted_symbols = sorted(symbols.items(), key=lambda item: item[0])

    # Create a list to store the summary for each instrument
    summary_list = []

    # Append the summary for each instrument to the list
    for symbol, instrument in sorted_symbols:
        summary_list.append(instrument.printSummary())

    # Join the summaries into a single string
    summary = '\n'.join(summary_list)

    return summary


# Main code
if __name__ == '__main__': 
    # A dictionary to store our instrument information
    symbols = {}
    inputFile = './input_data.csv'

    loadData(symbols, inputFile)
    print(printSummary(symbols))
