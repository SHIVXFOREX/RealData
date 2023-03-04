# CHANGE VERSON 2
# verson 8
# LINUX SERVER
# lINUX sWWERVRS 2
from datetime import datetime
import time
from iqoptionapi.stable_api import IQ_Option
import easygui
import time
import mysql.connector

mydb = mysql.connector.connect(
  host="sql178.main-hosting.eu",
  user="u733493607_pythondb",
  password="python@3NGINE",
  database="u733493607_pythondb"
)

mycursor = mydb.cursor()

now = datetime.now()
seconds = now.strftime("%H:%M")


#ACTIVES = easygui.enterbox("Actives ? ?")
ACTIVES = "EURGBP"

while True:
            time.sleep(1)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            seconds = now.strftime("%H:%M")
            day = now.strftime("%d/%m/%Y")
            
            print("HR and MIN =", seconds)
            if seconds == seconds:
                print("time is ", seconds)
                error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
                Iq = IQ_Option("shivxforex@gmail.com", "IDEAPAD300")
                check, reason = Iq.connect()

                if check:
                    print("Start your robot")
                    # if see this you can close network for test
                    balance_type = "REAL"
                    print(Iq.change_balance(balance_type))
                    Initial_Balance = float(Iq.get_balance())

                    
                    duration =  1 # minute 1 or 5
                    default_Amt = 1
                    amount = 2
                    action = "put"  # put
                    polling_time = 3
                    counter = 1
                    expirations_mode = 1
                    winCounter = 0
                    lossCounter = 0
                    Martingle_Arr = [8,15,33,72,160]
                    Reg_row = 0
                    Mar_row = 0
                    currentEarning = 0
                    compounding_Flag = False
                    martingle_Flag = True
                    compundingAmt = 0
                    
                    # check result
                    def check_result(id):
                        while True:
                            check, win = Iq.check_win_digital_v2(id)
                            if check == True:
                                break
                        if win < 0:

                            return win
                        else:

                            return win

                    # first time place trade
                    
                    amount = Martingle_Arr[Mar_row]

                    print("Placing First Trade!")
                    _, id = (Iq.buy_digital_spot(ACTIVES, amount, action, duration))

                    # Master Loop
                    while True:
                        file1 = open(ACTIVES + ".txt", "a")
                        if check_result(id) > 0:
                            result = "WIN"
                            print("win")
                            lossCounter = 0
                            winCounter = winCounter + 1
                        else:
                            result = "LOSS"
                            print("loss")
                            winCounter = 0
                            lossCounter = lossCounter + 1

                            

                        # AM
                        if martingle_Flag :
                            if check_result(id) > 0:
                                Mar_row = 0
                            else:
                                Mar_row = Mar_row + 1
                            amount = Martingle_Arr[Mar_row]


                        
                        print("Amount Counter 1 :" + str(amount))  

                        current_Bal = float(Iq.get_balance())  
                        
                        currentEarning = current_Bal - Initial_Balance


                        # Counter Controller

                        counter = counter + 1

                        

                        

                        #call indiacators
                        if currentEarning > 7 :
                             print("exiting")       
                             exit()

                        #Place Trade

                        _, id = (Iq.buy_digital_spot(
                            ACTIVES, amount, action, duration))


                         
                        
                        #SQL UPDAT
                        mydb.connect()
                        sql = (f"UPDATE active SET winAmt = '{currentEarning}' WHERE currency = '{ACTIVES}'" )
                        print(sql)
                        mycursor.execute(sql)
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected")
                        

                        #Write Logs...
                        print("-------------------------------------")
                        print("Active :- " + ACTIVES)
                        print("Counter :- " + str(counter))
                        print("WinCounter :- " + str(winCounter))
                        print("LossCounter :- " + str(lossCounter))
                        print("Balance :- ", Iq.get_balance())
                        print("Amount :- ", amount)
                        print("Current Earning :- ", current_Bal - Initial_Balance)
                        print("T&D :- " + dt_string + " | ")
                        print("-------------------------------------")
                        
                        #Write File..
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        file1.write("T&D :- " + dt_string + " | ")
                        file1.write(ACTIVES + " | ")
                        file1.write(" | " + result + " | ")
                        file1.write(action + " | ")
    
                        file1.write(str(amount))
                        file1.write(" | Counter :- " + str(counter) + " | ")
                        file1.write(str(Iq.get_balance()))
                        file1.write("\n")
                        file1.close()


