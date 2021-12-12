import wx

password = {}
num = []

class InfoPanel(wx.Frame):
    def __init__(self, parent, id):
        global password
        wx.Frame.__init__(self, parent, id, "password assistance", pos=(0, 0), size=(480, 300)) #define the basic info of the frame
        panel = wx.Panel(self, -1)
        self.proof = None #initialize
        self.user_input_pw(self) #initialize
        self.read_pw_file(self) #initialize

        txt1 = wx.StaticText(panel, -1, "Welcome          " , pos=(50, 0)) #define static text "Welcome" including position
        txt1.SetForegroundColour("black") #set the forground colour as black
        txt1.SetBackgroundColour("") #set the background colour as default

        txt2 = wx.StaticText(panel, -1, '                            Total recorded', pos=(200, 0)) #define static text "Total recorded"
        self.total_pw = wx.TextCtrl(panel, -1, "", pos=(250, 0),  size=(20, 20)) #set the position and size of the static text

        txt3 = wx.StaticText(panel, -1, 'All records', pos=(0, 30))  #define static text "All records"
        self.PSList = wx.Choice(panel, -1, choices=list(password),  pos=(80, 30), size=(80, -1)) #define the drop-down list
        button2 = wx.Button(panel, wx.ID_ANY, pos=(161, 26), size=(80, 27), label='Show') #set the position and size of the button
        button2.Bind(wx.EVT_BUTTON, self.show_password_strength)

        self.findpw = wx.TextCtrl(panel, -1, "", pos=(250, 30), size=(100, -1)) #define "Find" frame
        button5 = wx.Button(panel, wx.ID_ANY, pos=(351, 28), size=(80, 27), label='Find') #set the position and size of the button
        button5.Bind(wx.EVT_BUTTON, self.my_find_password)

        txt4 = wx.StaticText(panel, -1, 'Password     ', pos=(0, 65)) #define the "Password" frame
        self.PSList_show = wx.TextCtrl(panel, -1, "", pos=(80, 60), size=(150, 35)) #set the position and size of the static text

        txt5 = wx.StaticText(panel, -1, 'Password strength', pos=(250, 65)) #define the "Password strength" frame
        self.strength = wx.TextCtrl(panel, -1, "", pos=(380, 60), size=(50, -1)) #set the position and size of the static text
        button3 = wx.Button(panel, wx.ID_ANY, pos=(0, 100), size=(220, 30), label='edit')  #set the position and size of the button
        button3.Bind(wx.EVT_BUTTON, self.my_revise_password)
        button4 = wx.Button(panel, wx.ID_ANY, pos=(220, 100), size=(220, 30), label='delet') #set the position and size of the button
        button4.Bind(wx.EVT_BUTTON, self.my_del_password)
        rev_ = wx.StaticText(panel, -1, '-----------------------------------------------------------------------------------------', pos=(0, 150))

        txt6 = wx.StaticText(panel, -1, 'Name', pos=(15, 180)) #define static text "Name"
        txt6 = wx.StaticText(panel, -1, 'Password', pos=(165, 180)) ##define static text "Password"
        self.temp_Name = wx.TextCtrl(panel, -1, "", pos=(60, 180), size=(100, -1))
        self.temp_key = wx.TextCtrl(panel, -1, "", pos=(225, 180), size=(100, -1))
        button = wx.Button(panel, wx.ID_ANY, pos=(330, 173), size=(120, 35), label='Append record')
        button.Bind(wx.EVT_BUTTON, self.get_password_from_record)
        self.my_get_total_pw(self)

    def user_input_pw(self, event): #create the user inputting password frame
        pw_dlg = wx.TextEntryDialog(None, "Please enter user key", 'Authentication') #create the text dialog
        while True: #continue test until valid user input
            try:
                if pw_dlg.ShowModal() == wx.ID_OK:
                    self.proof = int(pw_dlg.GetValue()) #get the value of userinput text
            except:
                pass
            pw_msg_dlg = wx.MessageDialog(self,'Your user key will be used for encryption and decoding, if the password is wrong you will not be able to see the correct password', 'attention!',
                                        wx.OK | wx.ICON_INFORMATION) #eject hint message
            pw_msg_dlg.ShowModal()
            pw_msg_dlg.Destroy()
            break
        pw_msg_dlg.Destroy()

    def read_pw_file(self, event): #read file to obtain password
        global password
        global num
        file = open("record.txt", 'r') #read file
        for line in file.readlines():
            if ':' in line and line[line.index(':')] not in num:
                password[line[:line.index(':')]] = line[line.index(':')+1:len(line)-1] #save password in text value to password dict
                num.append(line[line.index(':')]) ##save password in text value to num list
        file.close() #close file

    def my_add_password(self, name, key): #add new password to origin password text file
        f = open("record.txt", 'a+')
        if name != "" and key != "":
            f.write(name + ':' + key + 'n')
        f.close()
        self.PSList.Append(name)
        self.my_get_total_pw(self)

    def get_password_from_record(self, event):
        global num
        if self.temp_Name.GetValue() != None and self.temp_key.GetValue() != None:
            if self.temp_Name.GetValue() in num:
                dlg = wx.MessageDialog(self, 'Record exist', '! ',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                raw = self.temp_key.GetValue()
                raw = my_encrypt(self.proof, raw)
                self.my_add_password(self.temp_Name.GetValue(), raw)
                self.read_pw_file(self)
                self.PSList.Refresh()
        self.temp_Name.Clear()
        self.temp_key.Clear()


    def my_get_total_pw(self, event):
        global num
        self.total_pw.Clear()
        self.total_pw.AppendText(str(len(num)))

    def show_password_strength(self):
        temp = self.PSList.GetSelection()
        self.PSList_show.Clear()
        self.PSList_show.AppendText(my_decrypt(self.proof,
                                            password[num[temp]]))
        self.strength.Clear()
        if self.judge_if_valid_pssword(my_decrypt(self.proof, password[num[temp]])):
            self.strength.AppendText('Strong')
        else:
            self.strength.AppendText('Weak')

    def my_revise_password(self, event):
        global num
        global password
        temp = self.PSList.GetSelection()
        temp2 = None
        dlg = wx.TextEntryDialog(None, "Please enter editted password", ' Edit password')
        while True: #obtain user revised input password
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    temp2 = dlg.GetValue()
                break
            except:
                pass
        dlg.Destroy()
        if len(temp2) == 0:
            pass
        else:   #when the new password satisfied the requirement,
            f = open("record.txt", 'r+')
            new_key = num[temp] + ':' + my_encrypt(self.proof, temp2) + '\n'
            x = f.readlines()
            flag = x.index(num[temp] + ':' + password[num[temp]] + '\n')
            x[flag] = new_key
            password[num[temp]] = my_encrypt(self.proof, temp2) #revised origin password
            f = open("record.txt", 'w+')
            f.writelines(x) #add new pasword to origin file
            f.close()
        self.strength.Clear()
        if self.judge_if_valid_pssword(my_decrypt(self.proof, temp2)):
            self.strength.AppendText('Strong')
        else:
            self.strength.AppendText('Weak')

    def my_del_password(self, event):
        global num
        global password
        temp = self.PSList.GetSelection() #find all key of password in the drop-down list
        f = open("record.txt", 'r+')
        x = f.readlines()
        flag = x.index(num[temp] + ':' + password[num[temp]] + '\n')
        del password[num[temp]]
        del num[temp]
        x[flag] = ""
        f = open("record.txt", 'w+')
        f.writelines(x)
        f.close()
        self.PSList.Delete(temp)
        self.get_password_from_record(self)
        self.PSList_show.Clear()
        self.strength.Clear()
        self.my_get_total_pw(self)

    def my_find_password(self, event):
        global password
        if len(self.findpw.GetValue()) == 0:
            pass
        else:
            temp = self.findpw.GetValue()
            self.PSList_show.Clear()
            try:
                self.PSList_show.AppendText(my_decrypt(self.proof,
                             password[temp]))
            except:
                self.PSList_show.AppendText("Not found！")

    def judge_if_valid_pssword(self, pw):
        if len(pw) < 10: #the length of password must be longer than 10
            return False
        flag = [0, 0, 0, 0]
        symbol = ['_', '!', '@', '#', '%', '^', '', '(', ')', '&']
        for i in pw: #construct the requirement of valid password
            if i.isupper():
                flag[0] = 1
            elif i.islower():
                flag[1] = 1
            elif i.isdigit():
                flag[2] = 1
            elif i in symbol:
                flag[3] = 1
            else:
                return False
        if sum(flag) >= 3: #Once the password satisfied the three items of password requirment, judge result will be true
            return True
        else:
            return False


def my_encrypt(key, s): #input key is the the all count of record, s the to-be encrpyted password
    b = bytearray(str(s).encode("gbk"))
    n = len(b) 
    c = bytearray("n2") #
    j = 0
    for i in range(0, n): #detail encrypt trick
        b1 = b[i]
        b2 = b1 ^ key 
        c1 = b2 % 16
        c2 = b2 * 16 
        c1 = c1 + 65
        c2 = c2 + 65 
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")


def my_decrypt(key, s): #input key is the all count of record, s is the to-be decrypted password
    c = bytearray(str(s).encode("gbk"))
    n = len(c)  
    if n % 2 != 0:
        return 
    n = n * 2
    b = bytearray("n")
    j = 0
    for i in range(0, n): #detail decrypt trick which is corresponding to the encrypt
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2 + c1
        b1 = b2 ^ key
        b[i] = b1
    return b.decode("gbk")


class MainApp(wx.App):
    def OnInit(self):
        self.frame1 = InfoPanel(None, -1)
        self.frame1.Center()
        self.frame1.Show(True)
        self.SetTopWindow(self.frame1)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop() #obtain all event on app
