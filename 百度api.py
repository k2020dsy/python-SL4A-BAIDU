# encoding:utf-8
import requests,ssl,sys,json,androidhelper,os
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

access_token=''

def sprintf(s, fs, *args):
    s = fs % args

def Base64Encode(str1):
    with open(str1, 'rb') as f:
        encode_img = base64.b64encode(f.read())
        print('data:image/{};base64,{}'.format(file_ext[1:], encode_img.decode()))
        f.close()
    return encode_img

def Base64Decode(SaveName,encode_img):
    with open(SaveName, 'wb') as f:
        f.write(base64.b64decode(encode_img))
        f.close()


def GetAssess():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GbpRWpgeVWsKmjd6DVuDa84o&client_secret=fNAdCWPl8lVr9f4uDE6bEVnpZ3CaodXr'
    response = requests.get(host,verify=False)
    if response:
        jsonData = json.loads(json.dumps(response.json()))
        access_token = jsonData['access_token']
        print(response.json())




'''
人脸融合
'''
def FaceMerge(strBackground,strTarget,SaveName):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v1/merge"

    templateB64=Base64Encode(strBackground)
    targetB64=Base64Encode(strTarget)

    sprintf(params,"{\"image_template\":{\"image\":\"%s\",\"image_type\":\"BASE64\",\"quality_control\":\"NONE\"},\"image_target\":{\"image\":\"%s\",\"image_type\":\"BASE64\",\"quality_control\":\"NONE\"}}",templateB64,targetB64)


    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        jsonData = json.loads(json.dumps(response.json()))
        resultsB64 = jsonData['result']['merge_image']
        if resultsB64:
            Base64Decode(SaveName,resultsB64)
        print (response.json())
    else:
        print("Service didn't response")

base_dir = "/storage/emulated/0/1"
droid = androidhelper.Android()
def show_dir(printStr,path=base_dir):
    
    """Shows the contents of a directory in a list view."""
    #The files and directories under "path"
    nodes = os.listdir(path)
    
    #Make a way to go up a level.
    if path != base_dir: 
        nodes.insert(0, '..')
    droid.dialogCreateAlert(printStr+"    当前目录："+os.path.basename(path).title())
    droid.dialogSetItems(nodes)
    droid.dialogShow()
    #Get the selected file or directory .
    result = droid.dialogGetResponse().result
    droid.dialogDismiss()
    if 'item' not in result:
       print("")
    else:
        target = nodes[result['item']]
        target_path = os.path.join(path, target)
        if target == '..': target_path = os.path.dirname(path)
        #If a directory, show its contents .
        if os.path.isdir(target_path): 
            return show_dir(printStr,target_path)
        #If an file display it.
        else:
           droid.dialogCreateAlert('Selected File','{}'.format(target_path))
           droid.dialogSetPositiveButtonText('Ok')
           droid.dialogSetNegativeButtonText('Cancel')
           droid.dialogShow()           
           reslt = droid.dialogGetResponse().result
           if reslt.get('which') == 'positive':
               return format(target_path)
           else:
               target_path = os.path.dirname(target_path)
               if os.path.isdir(target_path): 
                   return  show_dir(printStr,target_path)
            
            
            
def create_dir(printStr,path=base_dir):
    
    """Shows the contents of a directory in a list view."""
    #The files and directories under "path"
    nodes = os.listdir(path)
    target_path = path
    #Make a way to go up a level.
    if path != base_dir: 
        nodes.insert(0, '..')
    droid.dialogCreateAlert(printStr+"    当前目录："+os.path.basename(path).title())
    droid.dialogSetItems(nodes)
    droid.dialogSetPositiveButtonText('Ok')
    droid.dialogSetNegativeButtonText('Cancel')
    droid.dialogShow()   
    
    #Get the selected file or directory .
    result = droid.dialogGetResponse().result
    #droid.dialogDismiss()
    if result.get('which') == 'positive':
        droid.dialogCreateInput("请输入：*.jpg中的*")
        droid.dialogSetNeutralButtonText('Ok')
        droid.dialogSetNegativeButtonText('Cancel')
        droid.dialogShow()   
        reslt = droid.dialogGetResponse().result
        if reslt.get('which') == 'neutral':
            str1=reslt.get('value')
            droid.dialogDismiss()
            return target_path+"/"+str1+".jpg"
        else:
            if reslt.get('which') == 'negative':  
                 droid.dialogDismiss()
        print(target_path)
        
    if result.get('which') == 'negative':
        target_path = os.path.dirname(target_path)
        if os.path.isdir(target_path): 
            return create_dir(printStr,target_path) 
                 
    if 'item' in result:
        target = nodes[result['item']]
        target_path = os.path.join(path, target)
        if target == '..': target_path = os.path.dirname(path)
        #If a directory, show its contents .
        if os.path.isdir(target_path):
            return create_dir(printStr,target_path)
        #If an file display it.
            #droid.dialogCreateAlert('Selected File','{}'.format(target_path))
               
            #reslt = droid.dialogGetResponse().result
    
                        
            
            
strTarget = ""
strBackground = ""
SaveName = ""

if __name__=="__main__":
    #show_dir()
  
    #while len(strTarget)==0 | len(strBackground)==0 | len(SaveName) == 0:
    strTarget=show_dir("选择目标头像:")
    #    print(strTarget)
    strBackground=show_dir("混合背景:")
    SaveName=create_dir("保存路径:")
    #nameImg = input（"保存为：*.jpg"）
    
    print(strTarget,strBackground,SaveName)
    if(len(strTarget)&strBackground&SaveName):
        GetAssess()
        FaceMerge(strBackground,strTarget,SaveName+nameImg)
    
    













