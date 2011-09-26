#!/usr/bin/python2

import gtk
import pdb
import providers.mycantos as mycantos
import ConfigParser
import threading

#Initiating thread use
gtk.gdk.threads_init()

class SMSSender:
    def __init__(self):
        #Create the top-level window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Sms Sender")
        self.window.set_border_width(3)
        self.window.set_opacity(0.5)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("destroy", lambda w: gtk.main_quit())

        #The main VBox which will contain the widgets
        self.vbox = gtk.VBox()
        self.window.add(self.vbox)
                
        #Show a combo box to choose which service to use
        frame_choose_service = gtk.Frame()
        frame_choose_service.set_label_align(0.5,0.5)
        frame_choose_service.set_label("Choose the provider")
        self.combobox_sms_service = gtk.combo_box_new_text()
        self.combobox_sms_service.append_text("mycantos")
        frame_choose_service.add(self.combobox_sms_service)
        self.vbox.pack_start(frame_choose_service, True, True, 0)

        #This gtk.Entry will contain the phone number
        self.frame_phno = gtk.Frame()
        self.frame_phno.set_label("Enter your phone")
        self.entry_phno = gtk.Entry()
        self.frame_phno.add(self.entry_phno)
        self.vbox.pack_start(self.frame_phno, True, True, 0)

        
        #This gtk.TextView has the multi-line text which is to be sent
        self.frame_message = gtk.Frame()
        self.frame_message.set_label("Enter message")
        self.textview_message = gtk.TextView()
        self.textview_message.set_size_request(450,200)
        self.frame_message.add(self.textview_message)
        self.vbox.pack_start(self.frame_message, True, True, 0)
        
        #The gtk.HBox which will contain Send & Exit gtk.Buttons
        self.hbox_buttons = gtk.HBox()
        
        #The send gtk.Button
        self.button_send = gtk.Button("Send")
        self.button_send.connect("clicked", self.send_sms) 
        self.hbox_buttons.pack_start(self.button_send, True, True, 0)
        
        #The quit gtk.Button
        self.button_quit = gtk.Button("Quit")
        self.button_quit.connect("clicked", lambda q: gtk.main_quit())
        self.hbox_buttons.pack_start(self.button_quit, True, True, 0)
        
        #Pack the gtk.HBox with the main gtk.VBox
        self.vbox.pack_start(self.hbox_buttons, True, True, 0)

        #My statusbar which will show messages
        self.statusbar = gtk.Statusbar()
        self.statusbar.set_size_request(450,15)
        self.warning_contextid = self.statusbar.get_context_id("Warnings")
        self.vbox.pack_start(self.statusbar, False, False, 0)
        
        #Show all widgets
        self.window.show_all()
    
    def send_sms(self, widget, data=None):
        
        service_in_use = self.combobox_sms_service.get_active_text()
        
        if service_in_use is None:
            self.statusbar.push(self.warning_contextid, "Please choose the right service")
            print "No service selected, not sending any messages"
            return

        phone_no = self.entry_phno.get_text()
        message_buffer = self.textview_message.get_buffer()
        
        #Getting the credentials from config file
        c = ConfigParser.ConfigParser()
        c.read(".creds")
        username = c.get(service_in_use, "username")
        password = c.get(service_in_use, "password")

        #Get the start & end gtk.IterText
        start, end = message_buffer.get_bounds()
        
        #Check if its less than 300 characters
        message_text = message_buffer.get_text(start,end, True)
        if len(message_text) > 300:
            self.statusbar.push(self.warning_contextid, "Number of characters should be less than 300")
            return
        else:
            self.statusbar.pop(self.warning_contextid)
        
        #Choosing the right service
        if service_in_use == "mycantos":
            #self.send_sms_mycantos(phone_no, message_text, username, password)
            threading.Thread(target = self.send_sms_mycantos, args=(phone_no, message_text, username, password)).start()
        else:
            print "No matching services found"
                   
    def send_sms_mycantos(self, phone_no, message_text, username, password):
        mycantos_handle = mycantos.MyCantos()
        mycantos_handle.set_credentials(username,password)
        mycantos_handle.set_message(message_text)
        mycantos_handle.set_number(phone_no)
        print mycantos_handle.send_sms()

    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    my_app = SMSSender()
    my_app.main() 
