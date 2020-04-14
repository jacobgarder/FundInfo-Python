import http.client
import json


class TAA:

    def getNAV(id):
        response = TAA.getAvanzaResponse(id, "month", 1)

        parsedJSON = json.loads(response)
        return parsedJSON["lastPrice"]

    def getMA(id, days):
        response = TAA.getAvanzaResponse(id, "month", days)

        parsedJSON = json.loads(response)
        try:
            return parsedJSON["technicalAnalysis"][0]["dataPoints"][-1][-1]
        except IndexError:
            return float('nan')

    def getChangePercent(id, timePeriod):
        response = TAA.getAvanzaResponse(id, timePeriod, 1)

        parsedJSON = json.loads(response)
        return parsedJSON["changePercent"]

#    def getUnRateData():
#        headers = { "Content-type": "application/json", "Accept": "*/*", "Cache-Control": "no-cache" }
#        conn = http.client.HTTPSConnection( "api.bls.gov", 443 )
#        conn.request( "POST", "/publicAPI/v1/timeseries/data/LNS14000000", "", headers )

    def getUnRateData():

        headers = {
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'dnt': "1",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'sec-fetch-site': "none",
            'cache-control': "no-cache",
        }

        conn = http.client.HTTPSConnection("api.bls.gov")
        conn.request(
            "GET", "/publicAPI/v1/timeseries/data/LNS14000000", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            print(response.status, response.reason)
        data = response.read()
        conn.close()

#         print( json.dumps(data.decode("utf-8" )) )

        parsedJSON = json.loads(data.decode("utf-8"))
        datapoints = parsedJSON["Results"]["series"][0]["data"]

        ret = [float(datapoints[0]["value"])]
        sum = 0.0
        nrOfMonths = 12
        for i in range(nrOfMonths):
            sum += float(datapoints[i]["value"])

        ret.append(sum / nrOfMonths)

        return ret

    def getAvanzaResponse(id, timePeriod, days):
        headers = {"Content-type": "application/json",
                   "Accept": "*/*", "Cache-Control": "no-cache"}
        body = "{\"orderbookId\":" + str(id) + ",\"chartType\":\"AREA\",\"widthOfPlotContainer\":558,\"chartResolution\":\"DAY\",\"percentage\":true,\"volume\":false,\"owners\":false,\"timePeriod\":\"" + str(
            timePeriod) + "\",\"ta\":[{\"type\":\"sma\",\"timeFrame\":" + str(days) + "}]}"
        conn = http.client.HTTPSConnection("www.avanza.se", 443)
        conn.request(
            "POST", "/ab/component/highstockchart/getchart/orderbook", body, headers)

        response = conn.getresponse()
        if response.status != 200:
            print(f"\nERR: {response.status}: {response.reason} when getting id: {id}\n")
        data = response.read()
        conn.close()

        return data.decode("utf-8")
