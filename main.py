import sys
from Fund import Fund
from TAA import TAA

fundListPath = input( "Enter path to fundlist: " )

with open( fundListPath, 'r' ) as handle:
    fundList = []
    print( "Fetching data", end='', flush=True )

    for line in handle:
        if line == '\n' or line.startswith( '#' ):
            continue
        parts = line.split()
        id = parts[ 0 ]
        name = " ".join( parts[ 1: ] )
        
        fundList.append( Fund( id, name ) )
        print('.', end='', flush=True)

fundList = sorted( fundList, key = lambda fund: fund.getAverageReturns(), reverse = True )

print( "\n\n" + Fund.getFormattedHeader() )

for fund in fundList:
    print( fund.getFormattedData() )

print()
topN = int( input( "Choose top n: " ) )

if topN < 1 or topN > len( fundList ):
    topN = len( fundList )

print( "\n" + Fund.getFormattedHeader() )

for fund in fundList[ :topN ]:
    print( fund.getFormattedData() )

unRateData = TAA.getUnRateData()

print( "\n\n=== US Unemployment rate ===" )
print( "Current: " + str( unRateData[ 0 ] ) )
print( "MA12: " + str( '{:.3f}'.format( unRateData[ 1 ] ) ) )