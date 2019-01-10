# -*- coding: utf-8 -*-
import requests
import hashlib
import os

VT_APIKEY = ''

def getMalwareInfoFromVT(hash) : 
    result = {}
    result['Scan_date'] = "-"
    result['Permalink'] = "-"
    result['Sha256'] = "-"
    result['Md5'] = "-"
    result['Sha1'] = "-"
    result['Total'] = "-"
    result['Positives'] = "-" 
    result['AhnLab-V3'] = "-"
    result['Avast'] = "-"
    result['BitDefender'] = "-"
    result['Kaspersky'] = "-"
    result['McAfee'] = "-"
    result['Sophos'] = "-"
    result['Symantec'] = "-"
    result['FileName'] = "-"
    result['Ssdeep'] = "-"
    result['FileType'] = "-"
    result['MagicLiteral'] = "-"
    result['Size'] = "-"
    result['FirstSubmissionDate'] = "-"
    result['MS_SW'] = "-"
    result['Signed'] = "-"
    url = 'https://www.virustotal.com/vtapi/v2/file/report?' + 'resource='+ hash+'&apikey=' + VT_APIKEY
    headers = {"User-Agent" : "I love Twice"}
    response = requests.post(url, headers=headers)
    response_json = response.json()
    if response_json['response_code'] == 1 :
        result['Scan_date'] = response_json['scan_date']
        result['Permalink'] = response_json['permalink']
        result['Sha256'] = response_json['sha256']
        result['Md5'] = response_json['md5']
        result['Sha1'] = response_json['sha1']
        result['Total'] = response_json['total']
        result['Positives'] = response_json['positives']
        scans = response_json['scans']
        if 'AhnLab-V3' in scans.keys() : 
            result['AhnLab-V3'] = scans['AhnLab-V3']['result']
        
        if 'Avast' in scans.keys() : 
            result['Avast'] = scans['Avast']['result']
        
        if 'BitDefender' in scans.keys() : 
            result['BitDefender'] = scans['BitDefender']['result']
        
        if 'Kaspersky' in scans.keys() : 
            result['Kaspersky'] = scans['Kaspersky']['result']
        
        if 'McAfee' in scans.keys() : 
            result['McAfee'] = scans['McAfee']['result']
        
        if 'Sophos' in scans.keys() : 
            result['Sophos'] = scans['Sophos']['result']
        
        if 'Symantec' in scans.keys() : 
            result['Symantec'] = scans['Symantec']['result']
        
        url = result['Permalink']
        response = requests.post(url, headers=headers)
        if (response.status_code == requests.codes.ok):
            response_html = response.text
            nameIndex = response_html.find("<td class=\"field-key\">File names</td>");
            if(nameIndex > -1) :
                result['FileName'] = response_html[nameIndex+86:nameIndex+200].split('<')[0]
            
            ssdeepIndex = response_html.find("ssdeep</div>\n  <div class=\"floated-field-value\">");
            if(ssdeepIndex > -1) :
                result['Ssdeep'] = response_html[ssdeepIndex+48:ssdeepIndex+300].split('<')[0];
            
            typeIndex = response_html.find("\n  <span class=\"field-key\">File type</span>");
            if(typeIndex > -1) :
                result['FileType'] = response_html[typeIndex+44:typeIndex+200].split('<')[0].replace("\n","")
            
            magicIndex = response_html.find("Magic literal</div>");
            if(magicIndex > -1) :
                result['MagicLiteral'] = response_html[magicIndex+55:magicIndex+300].split('<')[0].replace("\n","")
            
            sizeIndex= response_html.find("File size</span>");
            if(sizeIndex > -1) :
                result['Size'] = (response_html[sizeIndex+18:sizeIndex+100].split('<')[0].replace(' ','').split('(')[1].split(')')[0]).replace("\n","").split("bytes")[0];
           
            fsIndex = response_html.find("First submission</span>");
            if(fsIndex > -1) :
                result['FirstSubmissionDate'] = response_html[fsIndex+26:fsIndex+45];
            
            microsoftIndex = response_html.find('Microsoft Corporation software catalogue');
            if(microsoftIndex > -1) :
                result['MS_SW'] = "O"
            
            signedIndex = response_html.find('<i class="icon-ok-sign"></i> Signed file, verified signature</span>');
            if(fsIndex > -1) :
                result['Signed'] = "O"
    return result

def getMD5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':
    filePath = ''
    if os.path.isfile(filePath) :
        md5 = getMD5(filePath)
        vt_result = getMalwareInfoFromVT(md5)
        print (vt_result)
