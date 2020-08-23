import webbot
import time
import json


def get_game(game_id):
    driver = webbot.Browser()
    driver.go_to('duckduckgo.com')
    time.sleep(4)
    congs_number= "congs4.c.bytro.com"
    execute_string = '''
    $.ajax({
        type: "POST",
        url: "https://'''+congs_number+ '''/",
        data: `{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'''+str(game_number)+ '''","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:`,
        success: function( response ) {
    try{
        document.open()
        document.write(JSON.stringify(JSON.parse(response).result.states["1"]))
    }catch{
        document.open()
        document.write(response)
    }
        }
    });
    '''
    driver.execute_script(execute_string)
    time.sleep(5)
    try:
        new_congs_number = json.loads(driver.get_page_source()[62:-14])["result"]["detailMessage"]
        new_execute_string = '''
        $.ajax({
            type: "POST",
            url: "https://'''+new_congs_number+ '''/",
            data: `{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'''+str(game_number)+ '''","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:`,
            success: function( response ) {
        try{
            document.open()
            document.write(JSON.stringify(JSON.parse(response).result.states["1"]))
        }catch{
            document.open()
            document.write(response)
        }
            }
        });
        '''
        driver.execute_script(new_execute_string)
        time.sleep(4)
        print(driver.get_page_source()[62:65])
        print(driver.get_page_source()[-30:-14])
        data = json.loads(driver.get_page_source()[62:-14])

    except:
        data = json.loads(driver.get_page_source()[62:-14])
    return data