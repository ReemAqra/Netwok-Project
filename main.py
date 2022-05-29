from socket import *
import pandas as pd
def getData(fileName):
    df = pd.read_csv("smartPhones.csv")    # getting smart phones data from .csv file
    if (fileName == "SortByPrice"):
        sorted_df = df.sort_values(by=["Price"], ascending=True) # sorting a csv file is done easily using data frames.
    elif (fileName == "SortByName"):
        sorted_df = df.sort_values(by=["Name"], ascending=True)
    return sorted_df
# mapping function to mapping content type of request
def mapping(subURL):
    contentType = ""            # define content type empty firstly
    ext = subURL.split(".")    # split (by .) request to get extension of it
    if(len(ext) > 1):          # check if request have extension (more than one character)
        if(ext[1] == "png"):   #if extencion is png then contentType is image/png
            contentType = "image/png"
        elif (ext[1] == "jpg"):   #if extencion is jpg then contentType is image/jpg
            contentType = "image/jpg"
        elif (ext[1] == "css"):    #if extencion is css then contentType is text/html
            contentType = "text/html"
        else:
            contentType = "text/html"
    else:
        contentType = "text/html"     # if the extention of request less than one character , it will be error or sorting request in both cases contant type is text/html
    if(subURL == ""):
        subURL = "index.html"
    return [contentType, subURL.strip()]   # we return the deduced content type and the required file name.

def main():
    Port = 5000                               # port is 5000
    Socket = socket(AF_INET, SOCK_STREAM)
    Socket.bind(('', Port))             # get socket
    Socket.listen(1)                          # server is listening
    print('server is ready to receive')
    while True:
        connectionSocket, addr = Socket.accept() # accept request
        sentence = connectionSocket.recv(1024).decode() # the request
        tok = sentence.split("/")                 # split request to get subURL
        if len(tok)>=2:
            subURL = tok[1].split(" ")                # delete subURL from spaces
        contentType, fileName = mapping(subURL[0])
        print(sentence)
        print("----------------------------------------------------------------")
        ip = addr[0] # ip of the client
        port = addr[1] # port of the client
        try:
            if (fileName == "SortByName" or fileName == "SortByPrice"):#check if request sort by name or sort by price
                fileContent = getData(fileName)
                # print(fileContent)
                fileContent = bytes(fileContent.to_string(), "UTF-8")
                contentType = "text/plain"  # we would be printing the sorted csv file in a text/plain type
            else:
                # if no errors, and the file name exists, it will be read and saved in fileContent and the response will start based on the deduced content type above.
                with open(fileName, "rb") as f:
                    fileContent = f.read()
            connectionSocket.send(bytes("HTTP/1.1 200 OK\r\n", "UTF-8"))
            connectionSocket.send(bytes("Content-Type:" + contentType + "\r\n", "UTF-8"))
            connectionSocket.send(bytes("\r\n", "UTF-8"))
            connectionSocket.send(fileContent)
            connectionSocket.close()
        except IOError:
             # if server have false request , server will response with  htmlfile that contain file not found
                fileContent = '<!DOCTYPE html><html><head><title>Error</title> </head><body><h1><p style="color:red;">The file is not found</h1><p id=par> Diana Allan  1180665 &emsp;Baraa Fatony  1180566 &emsp;Reem Aqra  1181818 <style >p#par{font-weight: bold;}</style></p>   <p>The IP is  '+ str(ip)+'</p> <p>The Port number is  '+str(port)+'</p></body></html>'
                print(fileContent)
                connectionSocket.send(bytes("HTTP/1.1 404 Not Found \r\n", "UTF-8"))
                connectionSocket.send(bytes("Content-Type: text/html\r\n", "UTF-8"))
                connectionSocket.send(bytes("\r\n", "UTF-8"))
                connectionSocket.send(bytes(fileContent, "UTF-8"))
                connectionSocket.close()
# calling main
main()