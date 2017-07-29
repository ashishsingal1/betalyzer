Public Function betalyzer(params As String) As String
    Dim URL As String
    Dim objHTTP As Object
    URL = "http://035d8c98.ngrok.io/api/?" & params
    Set objHTTP = CreateObject("WinHttp.WinHttpRequest.5.1")
    objHTTP.Open "GET", URL, False
    objHTTP.send ("")
    betalyzer = objHTTP.ResponseText
End Function
