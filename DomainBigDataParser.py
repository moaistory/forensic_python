import urllib2
import json

domainBigDataUrl = "http://198.50.154.167"
def getDomainInfo(domain) :
    request=urllib2.Request(domainBigDataUrl + "/" + domain)
    request.add_header("Host", "domainbigdata.com")
    response = urllib2.urlopen(request)
    htmlText = response.read()
       
    domainInfo  = {}
    domainInfo['domain_domain'] = ''
    domainInfo['domain_world_domain'] = ''
    domainInfo['domain_title'] = ''
    domainInfo['domain_date_creation'] = ''
    domainInfo['domain_web_age'] = ''
    domainInfo['domain_ip_address'] = ''
    domainInfo['domain_ip_geolocation'] = ''
    domainInfo['registrant_name'] = ''
    domainInfo['registrant_organization'] = ''
    domainInfo['registrant_email'] = ''
    domainInfo['registrant_country'] ='' 
    domainInfo['registrant_private'] = ''
    
    if htmlText.find("this domain does not exist") >= 0 :
        return domainInfo
    
    domain_index = htmlText.find("Domain</td>\r\n\t<td>")
    if domain_index > 0 : 
        domainInfo['domain_domain'] = htmlText[domain_index+18:domain_index+200].split('<')[0].strip()
    
    world_domain_index = htmlText.find("Words in</td>\r\n\t<td>")
    if world_domain_index > 0 :
        domainInfo['domain_world_domain'] = htmlText[world_domain_index+31:world_domain_index+200].split('<')[0].strip()
    
    title_index = htmlText.find("Title</td>\r\n\t<td>")
    if title_index > 0 :
        domainInfo['domain_title'] = htmlText[title_index+17:title_index+200].split('<')[0].strip()
    
    date_creation_index = htmlText.find("Date creation</td>\r\n\t<td>")
    if date_creation_index > 0 :
        domainInfo['domain_date_creation'] = htmlText[date_creation_index+25:date_creation_index+200].split('<')[0].strip()
    
    web_age_index = htmlText.find("Web age</td>\r\n\t<td colspan=\"2\">")
    if web_age_index > 0 :
        domainInfo['domain_web_age'] = htmlText[web_age_index+31:web_age_index+200].split('<')[0].strip()
    
    ip_address_index = htmlText.find("IP Address</td>\r\n\t<td style=\"min-width: 200px;\">")
    if ip_address_index > 0 :
        for startIndex in range(ip_address_index+48, ip_address_index+250) :
            if htmlText[startIndex] == '>' and htmlText[startIndex+1] != '<' : 
                domainInfo['domain_ip_address'] = htmlText[startIndex+1:startIndex+30].split('<')[0].strip()
                break
    
    ip_geolocation_index = htmlText.find("IP Geolocation</td>\r\n\t<td>")
    if ip_geolocation_index > 0 :
        for startIndex in range(ip_geolocation_index+26, ip_geolocation_index+300) :
            if htmlText[startIndex] == '>' and htmlText[startIndex+1] != '<' : 
                domainInfo['domain_ip_geolocation'] = htmlText[startIndex+1:startIndex+100].split('<')[0].strip()
                break
    
    registrant_name_index = htmlText.find("trRegistrantName\">\r\n\t<td>Name</td>")
    if registrant_name_index > 0 :
        for startIndex in range(registrant_name_index+34, registrant_name_index+300) :
            if htmlText[startIndex] == '>' and htmlText[startIndex+1] != '<' : 
                domainInfo['registrant_name'] = htmlText[startIndex+1:startIndex+100].split('<')[0].strip()
                break
            
    registrant_name_index = htmlText.find("MainMaster_trRegistrantOrganization\">\r\n\t<td>Organization</td>")
    if registrant_name_index > 0 :
        for startIndex in range(registrant_name_index+61, registrant_name_index+300) :
            if htmlText[startIndex] == '>' and htmlText[startIndex+1] != '<' : 
                domainInfo['registrant_organization'] = htmlText[startIndex+1:startIndex+100].split('<')[0].strip()
                break
            
    registrant_name_index = htmlText.find("trRegistrantEmail\">\r\n\t<td>Email</td>")
    if registrant_name_index > 0 :
        for startIndex in range(registrant_name_index+36, registrant_name_index+300) :
            if htmlText[startIndex] == '>' and htmlText[startIndex+1] != '<' : 
                domainInfo['registrant_email'] = htmlText[startIndex+1:startIndex+100].split('<')[0].strip()
                break
            
    registrant_name_index = htmlText.find("trRegistrantCountry\">\r\n\t<td>Country</td>")
    if registrant_name_index > 0 :
        for startIndex in range(registrant_name_index+41, registrant_name_index+300) :
            if htmlText[startIndex] == '>' and htmlText[startIndex+1] != '<' : 
                domainInfo['registrant_country'] = htmlText[startIndex+1:startIndex+100].split('<')[0].strip()
                break
            
    registrant_name_index = htmlText.find("<td>Private</td>\r\n                                        <td colspan=\"2\">")
    if registrant_name_index > 0 :
        domainInfo['registrant_private'] = htmlText[registrant_name_index+74:registrant_name_index+200].split('<')[0].strip()
                
    return domainInfo
   
file_r = open("domains.txt", "r")

for text in file_r.readlines():
    url = text.rstrip()
    print (url)
    domainInfo = getDomainInfo(url)
    print (domainInfo)

file_r.close()

