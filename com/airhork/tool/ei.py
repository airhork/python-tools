"""
"""

token = '''eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJEeDJ6TE03cEdmS1cwZ2QyYUNCVllGQjgxTXFWZnpNanMwQzVkUlM5NkE4In0.eyJqdGkiOiJiOWQzYjFkYS1iYzgxLTQ0YzktYjVlMC0xM2NlMDM5MmUxYTgiLCJleHAiOjE2Mzc1NjI1MzAsIm5iZiI6MCwiaWF0IjoxNjM3NTYwNzMwLCJpc3MiOiJodHRwczovL3NoZ3dmMjIxLmFzcGFjLmxvY2FsL2F1dGgvcmVhbG1zL0VJIiwiYXVkIjoiY2xpZW50LWFwcCIsInN1YiI6IjViYjE2MTg5LTYyODktNDRkMC1iOTMxLTUzNzg0OTE3NzU5MSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudC1hcHAiLCJub25jZSI6IjFmZjNiODAxLTFkN2QtNDgzYS05YjYzLTJhMDdhNDQzZjI0NiIsImF1dGhfdGltZSI6MTYzNzU1MTc5OCwic2Vzc2lvbl9zdGF0ZSI6IjRjNjFhNjFiLWUzOWEtNGNiOC1hZmJiLTc0M2VkNTRhOTRkYSIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8xMC4yMzUuNTkuMTA1IiwiaHR0cHM6Ly9TSEdXRjIyMS5hc3BhYy5sb2NhbCIsImh0dHBzOi8vc2hnd2YyMjEuYXNwYWMubG9jYWwiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIk1PTklUT1IiLCJFcnJvclJlcG9ydFVzZXIiLCJTRUNPRkZJQ0VSIiwiSW50ZXJvcFVzZXIiLCJJbnRlcm9wQWRtaW5Vc2VyIiwiSGVhbHRoY2hlY2tVc2VyIiwiUHJlc2VudGF0aW9uQ3JlYXRvciIsIkRpYWdub3N0aWNQcmVzZW50YXRpb25DcmVhdG9yIiwiQXVkaXRMb2dVc2VyIiwiSmF2YU1lbG9keVVzZXIiLCJYZXJvQ3JlYXRvciIsIlN5c3RlbUFkbWluVXNlciIsIldlYlVzZXIiLCJBRE1JTiIsIlhlcm9Vc2VyIiwiQWdmYSIsIk5ldGJvb3QiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJpc1JlbW90ZUlkUCI6ImZhbHNlIiwidGFyZ2V0SWRQIjoiSW50ZXJuYWwiLCJncm91cHMiOlsiU2VjdXJpdHkgb2ZmaWNlciIsIlN5c3RlbSBBZG1pbmlzdHJhdG9yIiwiTW9uaXRvciJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJncmFjZSIsImdpdmVuX25hbWUiOiJHcmFjZSIsImFnZmFfZGVza3RvcF9wcm9maWxlcyI6WyJ0cmFuc2NyaXB0aW9uaXN0LmRlc2t0b3AiLCJ0ZWNobm9sb2dpc3QuZGVza3RvcCIsImNvbmZpZ3VyYXRvci5kZXNrdG9wIiwiZGlhZ25vc3RpYy5kZXNrdG9wIiwidGVhY2hpbmcuZmlsZXMud2ViLmNsaWVudCIsImVudGVycHJpc2Uudmlld2VyLmRlc2t0b3AiXSwibG9jYWxlIjoiZW5fVVMiLCJ0YXJnZXRJZFBJZCI6IkQ1MjBGRDIxMUE4NTQzRjdBMUUxMjlBNDA3Mjc5M0REIiwiZmFtaWx5X25hbWUiOiJLZWxseSJ9.EyRD6HwfDKpY2TfRxOvVJDpSM1KBfPmpdzT3nYVqwLVWZgg-5bbIf-kzHRb_MAdCsZ4RGzOJYM-jC1bu4rb6gOENklPhW58WcnJH-EVeqlCwBeNL92H24sQRNkKCG1OQhwyte04ySIYCGbsIh5ePdw7rZNHqKQ57jufKR3EDcy9e2nWHa5Sq0FSD7E5z7wULdxnS8G0AiI_qlEaXn0-deqTshvNXu3lw_Tnffeb61u5I8c4J5rWcUoVJ7wYSnud8T_-xnXcsCpTBg0fUl4aswraumMhdb9q-IlHv5gY4agiBKgxc5UpErpg5TvCttlYMR4TV1D8fzhUWNEDAPDkCOQ'''





def batchCreatingUser(begin, end):
    import requests
    import json
    header = {'Authorization' : ('Bearer  %s' %(token)), 'Content-Type' : 'application/json'}
    print(header)

    f = open('/Users/axesr/Downloads/user.json')
    input = json.load(f)
    url = "https://shgwf221.aspac.local/ris/web/v1/contactusers/professional"

    for x in range(begin, end):
        input['contact']['personName']['firstName'] = 'test%d' %(x)
        input['contact']['personName']['lastName'] = 'test%d' %(x)
        input['contact']['identityCodes'][0]['code'] = 'CNTCT240%d' %(x)
        input['user']['userDomains'][0]['loginName'] = 'TEST%d' %(x)

        print(input)
        res = requests.post(url,headers = header, json=input,verify=False)
        print(res.status_code)
        print(res.text)



	


def analysisQL():
    import json

    result = {}
    nameresult = {}

    with open("e:\\project\\advent\\query_list_23.json") as fp:
        lines = fp.readlines()
        for line in lines:
            item = json.loads(line)
            if item['filterGroups'] is not None:
                print(item['id'])
                i = 0
                for filterGroup in item['filterGroups']:
                    filters = []
                    bindings = {}
                    itemresult = []
                    for filter in filterGroup['filterBindings'] :
                        filters.append(filter['filterParam'])
                        bindings[filter['filterParam']] = filter

                    filters.sort()
                    for fi in filters :
                        itemresult.append(fi)
                        itemresult.append(bindings[fi]['operator'])
                        itemresult.append(bindings[fi]['value'])
                    result['%s_%s' %(item['id'], i)] = ('_'.join(itemresult))
                    nameresult['%s_%s' %(item['id'], i)] = item['name']
                    i = i + 1

    tt = result.values()
    print('size of list %d' %(len(tt)))
    print('size of set %d' %(len(set(tt))))

    f = open('e:\\r_23.csv','w')
    for x in result:
        f.write('%s,%s,%s \n' %(x, nameresult[x], result[x].replace(',','.')))
    f.close()

            

	



if __name__ == "__main__":
    main()


