import wx
import json

password = {}
num = []
# LoginDialog is used to open a window where the user enters a username and password to access his stored passwords.
class LoginDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Login")
        self.logged_in = False
        self.password_shown= False

        self.username = wx.TextCtrl(self, -1)     
        self.hidden_password = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.visible_password = wx.TextCtrl(self)
        self.visible_password.Hide()
        
        self.login = wx.Button(self, -1, "Login")

        self.password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.password_sizer.Add(self.hidden_password, 0, wx.ALL, 5)
        self.password_sizer.Add(self.visible_password, 0, wx.ALL, 5)
        

        mainsizer= wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.username, 0, wx.ALL, 5)
        mainsizer.Add(self.password_sizer)
        mainsizer.Add(self.login, 0, wx.ALL, 5)

        
        self.login.Bind(wx.EVT_BUTTON, self.OnLogin)
       
        self.username.SetToolTip("Username")
        
        self.hidden_password.SetToolTip("Input password")
        self.visible_password.SetToolTip("Input password")
        

        self.SetSizer(mainsizer)

    def OnToggle(self, event):
        self.hidden_password.Show(self.password_shown)
        self.visible_password.Show(not self.password_shown)
        if not self.password_shown:
            self.visible_password.SetValue(self.hidden_password.GetValue())
            self.visible_password.SetFocus()
        else:
            self.hidden_password.SetValue(self.visible_password.GetValue())
            self.hidden_password.SetFocus()
        self.hidden_password.GetParent().Layout()
        self.password_shown = not self.password_shown

    def OnLogin(self, event):
        # Check if data entered by the user matches with the one stored in the json file.  
        user_password1 = self.hidden_password.GetValue()
        user_username1 = self.username.GetValue()
        # Open the file with the stored passwords and check if the data entered by the user is in the file.
        with open('data4.json') as master_data:
            all_users=json.load(master_data)
            entry_exists = False
            for acct in all_users["accounts"]:

                if acct["username"] == user_username1:
                    entry_exists = True
                    if acct["password"] == user_password1:
                        wx.MessageBox('Login Success', 'Error', wx.OK | wx.ICON_INFORMATION)
                        self.logged_in = True
                        self.Close()
                        self.userpw(self)
                        return
                    else:
                        wx.MessageBox('Login failed with wrong password', 'Error', wx.OK | wx.ICON_ERROR)
                        self.Close()
                        return
                else:
                    pass
            if not entry_exists:
                wx.MessageBox('Not exist user, creating new account and password', 'Error', wx.OK | wx.ICON_INFORMATION)
                temp = all_users["accounts"]
                temp.append({
                    "username": user_username1,
                    "password": user_password1
                })
                with open('data4.json', 'w') as outfile:
                    json.dump(all_users, outfile, indent=2)
                        
                self.logged_in = True
                self.Close()
                self.userpw(self)
                return
        
           
class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        global password
        wx.Frame.__init__(self, parent, id, "Password Manager", pos=(0, 0), size=(480, 300))
        # Define the basic information of the frame
        panel = wx.Panel(self, -1)
        self.proof = None
        # initialize
        self.input_password(self)
        # initialize
        self.read_txt(self)
        # initialize
        txt1 = wx.StaticText(panel, -1, 'Welcome！', pos=(50, 0))
        # define static text 'welcome' and its position
        txt1.SetForegroundColour("black")
        # set the forground colour as black
        txt1.SetBackgroundColour("")
        # set the backgound colour as default
        txt2 = wx.StaticText(panel, -1, 'Total', pos=(200, 0))
        # define static text "Total"
        self.total_pw = wx.TextCtrl(panel, -1, "", pos=(250, 0), size=(20, 20))
        # set the position and size of the static text
        txt3 = wx.StaticText(panel, -1, 'All records', pos=(0, 30))
        # define static text 'All records'
        self.PSList = wx.Choice(
            panel, -1, choices=list(password), pos=(80, 30), size=(80, -1))
        # define drop down list and its position
        button2 = wx.Button(panel, wx.ID_ANY, pos=(
            161, 26), size=(80, 27), label='Show')
        # set the position and size of the button
        button2.Bind(wx.EVT_BUTTON, self.show_strength)
        # bind button2 with the function of show_strength)
        self.findpw = wx.TextCtrl(panel, -1, "", pos=(250, 30), size=(100, -1))
        # define find frame
        button5 = wx.Button(panel, wx.ID_ANY, pos=(
            351, 28), size=(80, 27), label='Search')
        # set position and sizae of button 5
        button5.Bind(wx.EVT_BUTTON, self.find_password)
        txt4 = wx.StaticText(panel, -1, 'Password', pos=(0, 65))
        # define the 'Password' frame
        self.PSList_show = wx.TextCtrl(
            panel, -1, "", pos=(80, 60), size=(150, 35))
        txt5 = wx.StaticText(panel, -1, 'Strength', pos=(250, 65))
        self.strength = wx.TextCtrl(
            panel, -1, "", pos=(380, 60), size=(50, -1))
        button3 = wx.Button(panel, wx.ID_ANY, pos=(
            0, 100), size=(220, 30), label='Update Password')
        button3.Bind(wx.EVT_BUTTON, self.edit_password)
        button4 = wx.Button(panel, wx.ID_ANY, pos=(
            220, 100), size=(220, 30), label='Delete')
        button4.Bind(wx.EVT_BUTTON, self.delete)
        txt_ = wx.StaticText(
            panel, -1, '-----------------------------------------------------------------------------------------', pos=(0, 150))
        txt6 = wx.StaticText(panel, -1, 'Name', pos=(15, 180))
        # define static text 'Name'
        txt6 = wx.StaticText(panel, -1, 'Password', pos=(165, 180))
        self.temp_Name = wx.TextCtrl(
            panel, -1, "", pos=(60, 180), size=(100, -1))
        self.temp_key = wx.TextCtrl(
            panel, -1, "", pos=(225, 180), size=(100, -1))
        button = wx.Button(panel, wx.ID_ANY, pos=(330, 173),
                           size=(120, 35), label='Add Record')
        button.Bind(wx.EVT_BUTTON, self.take_password)
        self.get_total_pw(self)

    def input_password(self, event):
        dlg = wx.TextEntryDialog(None, "Enter User Key (Number between 1-256)", 'Authentication')
        # create user inputting page and text dialog
        while True:
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    self.proof = int(dlg.GetValue())
        # continue test until a valid user input value was entered
            except:
                pass
            dlg2 = wx.MessageDialog(
                self, 'Your user key will be used for encryption and decoding, if the password is wrong you will not be able to see the correct password', 'attention!', wx.OK | wx.ICON_INFORMATION)
        # Eject hint message
            dlg2.ShowModal()
            dlg2.Destroy()
            break
        dlg.Destroy()


    def read_txt(self, event):
        global password
        global num
        f = open("record1.txt", 'a+')
        f = open("record1.txt", 'r')
        for line in f.readlines():
            if ':' in line and line[:line.index(':')] not in num:
                password[line[:line.index(':')]] = line[line.index(':')+1:len(line)-1]
                num.append(line[:line.index(':')])
        f.close()

    def append(self, name, key):
        f = open("record1.txt", 'a+')
        if name != "" and key != "":
            f.write(name + ':' + key + '\n')
        f.close()
        self.PSList.Append(name)
        self.get_total_pw(self)


    def take_password(self, event):
        global num
        if self.temp_Name.GetValue() != None and self.temp_key.GetValue() != None:
            if self.temp_Name.GetValue() in num:
                dlg = wx.MessageDialog(
                    self, 'Record existed', '！', wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                raw = self.temp_key.GetValue()
                raw = my_encrypt(self.proof, raw)
                self.append(self.temp_Name.GetValue(), raw)
                self.read_txt(self)
                self.PSList.Refresh()
        self.temp_Name.Clear()
        self.temp_key.Clear()

    def get_total_pw(self, event):
        global num
        self.total_pw.Clear()
        self.total_pw.AppendText(str(len(num)))

    def show_strength(self, event):
        temp = self.PSList.GetSelection()
        self.PSList_show.Clear()
        self.PSList_show.AppendText(decrypt(self.proof, password[num[temp]]))
        self.strength.Clear()
        if self.judge_password_strength(decrypt(self.proof, password[num[temp]])):
            self.strength.AppendText('Strong')
        else:
            self.strength.AppendText('Weak')

    def edit_password(self, event):
        global num
        global password
        temp = self.PSList.GetSelection()
        temp2 = None
        dlg = wx.TextEntryDialog(
            None, "Please enter editted password：", 'edit password')
        while True:
            # obtain user revised input password
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    temp2 = dlg.GetValue()
                break
            except:
                pass
        dlg.Destroy()
        if temp2 != "":
            f = open("record1.txt", 'r+')
            new_key = num[temp] + ':' + my_encrypt(self.proof, temp2) + '\n'
            x = f.readlines()
            flag = x.index(num[temp] + ':' + password[num[temp]] + '\n')
            x[flag] = new_key
            password[num[temp]] = my_encrypt(self.proof, temp2)
            # revised origin password
            f = open("record1.txt", 'w+')
            f.writelines(x)
            # add new pasword to origin file
            f.close()
        self.strength.Clear()
        if self.judge_password_strength(decrypt(self.proof, temp2)):
            self.strength.AppendText('Strong！')
        else:
            self.strength.AppendText('Weak！')

    def delete(self, event):
        global num
        global password
        temp = self.PSList.GetSelection()
        f = open("record1.txt", 'r+')
        x = f.readlines()
        flag = x.index(num[temp] + ':' + password[num[temp]] + '\n')
        del password[num[temp]]
        del num[temp]
        x[flag] = ""
        f = open("record1.txt", 'w+')
        f.writelines(x)
        f.close()
        self.PSList.Delete(temp)
        self.take_password(self)
        self.PSList_show.Clear()
        self.strength.Clear()
        self.get_total_pw(self)

    def find_password(self, event):
        global password
        if self.findpw.GetValue() != "":
            temp = self.findpw.GetValue()
            self.PSList_show.Clear()
            try:
                self.PSList_show.AppendText(
                    decrypt(self.proof, password[temp]))
            except:
                self.PSList_show.AppendText("Not found！！")

    def judge_password_strength(self, pw):
        if len(pw) < 10:
            return False
        flag = [0, 0, 0, 0]
        symbol = ['_', '!', '@', '#', '%', '^', '*', '(', ')', '&']
        for i in pw:
            # construct the requirement of valid password
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
        if sum(flag) >= 3:
            # Once the password satisfied the three items of password requirment, judge result will be true
            return True
        else:
            return False


def my_encrypt(key, s):  
    # input key is the the all count of record, s the to-be encrpyted password
    b = bytearray(str(s).encode("gbk"))
    n = len(b)
    #Calculate the numbers of bytes of b
    c = bytearray(n * 2)
    j = 0
    for i in range(0, n): 
    # detail encrypt trick
        b1 = b[i]
        b2 = b1 ^ key
        c1 = b2 % 16
        c2 = b2 // 16
        c1 = c1 + 65
        c2 = c2 + 65
        #c1 and c2 are numbers between 0-15, Add 65 to become the A-P character encoding
        c[j] = c1
        c[j + 1] = c2
        j = j + 2
    return c.decode("gbk")


def decrypt(key, s):  
    # input key is the all count of record, s is the to-be decrypted password
    c = bytearray(str(s).encode("gbk"))
    n = len(c)
    if n % 2 != 0:
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):  
    # detail decrypt trick which is corresponding to the encrypt
        c1 = c[j]
        c2 = c[j + 1]
        j = j + 2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2 * 16 + c1
        b1 = b2 ^ key
        b[i] = b1
    return b.decode("gbk")

class MainApp(wx.App):
    def OnInit(self):
        dlg = LoginDialog()
        dlg.ShowModal()
        authenticated = dlg.logged_in
        dlg.Destroy()
        if not authenticated:
            wx.MessageBox('Login failed', 'Error', wx.OK | wx.ICON_ERROR)
            self.Destroy()
        self.frame1 = MyFrame(None, -1)
        self.frame1.Center()
        self.frame1.Show(True)
        self.SetTopWindow(self.frame1)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
