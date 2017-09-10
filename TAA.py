import http.client
import urllib.parse
import json

class TAA:

    def getNAV( id ):
        response = TAA.getAvanzaResponse( id, "month", 1 )
        
        parsedJSON = json.loads( response )
        return parsedJSON[ "lastPrice" ]

    def getMA( id, days ):
        response = TAA.getAvanzaResponse( id, "month", days )
        
        parsedJSON = json.loads( response )
        return parsedJSON[ "technicalAnalysis" ][ 0 ][ "dataPoints" ][ -1 ][ -1 ]

    def getChangePercent( id, timePeriod ):
        response = TAA.getAvanzaResponse( id, timePeriod, 1 )
        
        parsedJSON = json.loads( response )
        return parsedJSON[ "changePercent" ]

    def getUnRateData():
        headers = { "Content-type": "application/json", "Accept": "*/*" }
        conn = http.client.HTTPSConnection( "api.bls.gov", 443 )
        conn.request( "POST", "/publicAPI/v1/timeseries/data/LNS14000000", "", headers )

        response = conn.getresponse()
        data = response.read()
        conn.close()

        parsedJSON = json.loads( data.decode( "utf-8" ) )
        datapoints = parsedJSON[ "Results" ][ "series" ][ 0 ][ "data" ]

        ret = [ float( datapoints[ 0 ][ "value" ] ) ]
        sum = 0.0
        nrOfMonths = 12
        for i in range( nrOfMonths ):
            sum += float( datapoints[ i ][ "value" ] )

        ret.append( sum / nrOfMonths )

        return ret

    def getAvanzaResponse( id, timePeriod, days ):
        headers = { "Content-type": "application/json", "Accept": "*/*" }
        body = "{\"orderbookId\":" + str( id ) + ",\"chartType\":\"AREA\",\"widthOfPlotContainer\":558,\"chartResolution\":\"DAY\",\"percentage\":true,\"volume\":false,\"owners\":false,\"timePeriod\":\"" + str( timePeriod ) + "\",\"ta\":[{\"type\":\"sma\",\"timeFrame\":" + str( days ) + "}]}"
        conn = http.client.HTTPSConnection( "www.avanza.se", 443 )
        conn.request( "POST", "/ab/component/highstockchart/getchart/orderbook", body, headers )

        response = conn.getresponse()
        data = response.read()
        conn.close()

        return data.decode( "utf-8" )