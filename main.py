## Needed Imports
from PCANBasic import *
from config import *
import sys
from time import sleep

import time
import datetime
import threading

import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import sys  
import io


class UDSClient():

    # Defines
    #region

    # Sets the PCANHandle (Hardware Channel)
    PcanHandle = PCAN_USBBUS1

    # Sets the desired connection mode (CAN = false / CAN-FD = true)
    # IsFD = True

    # Sets the bitrate for normal CAN devices
    Bitrate = PCAN_BAUD_500K

    # Sets the bitrate for CAN FD devices. 
    # Example - Bitrate Nom: 1Mbit/s Data: 2Mbit/s:
    #   "f_clock_mhz=20, nom_brp=5, nom_tseg1=2, nom_tseg2=1, nom_sjw=1, data_brp=2, data_tseg1=3, data_tseg2=1, data_sjw=1"
    # BitrateFD = b'f_clock_mhz=80,nom_brp=10,nom_tseg1=12,nom_tseg2=3,nom_sjw=3,data_brp=2,data_tseg1=31,data_tseg2=8,data_sjw=4'
    BitrateFD = b'f_clock=80000000,nom_brp=10,nom_tseg1=12,nom_tseg2=3,nom_sjw=3,data_brp=2,data_tseg1=31,data_tseg2=8,data_sjw=4'

    #endregion

    # Members
    #region
    

    # Shows if DLL was found
    m_DLLFound = False

    #endregion

    def __init__(self, IsFD, need_keep_alive, log_area = None):
        file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".log"
        self._file_record = open(file_name, "w+")
        self._IsFD = IsFD
        self._need_keep_alive = need_keep_alive
        """
        Create an object starts the programm
        """
        self.ShowConfigurationHelp() ## Shows information about this sample
        self.ShowCurrentConfiguration() ## Shows the current parameters configuration

        self.log_area = log_area

        ## Checks if PCANBasic.dll is available, if not, the program terminates
        try:
            self.m_objPCANBasic = PCANBasic()        
            self.m_DLLFound = self.CheckForLibrary()
        except:
            print("Unable to find the library: PCANBasic.dll !")
            self.getInput("Press <Enter> to quit...")
            self.m_DLLFound = False
            return

        
        ## Initialization of the selected channel
        if self._IsFD:
            stsResult = self.m_objPCANBasic.InitializeFD(self.PcanHandle,self.BitrateFD)
        else:
            stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle,self.Bitrate)

        if stsResult != PCAN_ERROR_OK:
            print("Can not initialize. Please check the defines in the code.")
            self.ShowStatus(stsResult)
            print("")
            print("Press enter to close")
            input()
            return

        # Init the can massge
        if self._IsFD == False:            
            self._can_msg_obj = TPCANMsg()
            # can msg len is default 8, it will changed by msg contend
            self._can_msg_obj.LEN = 8
            self._can_msg_obj.MSGTYPE = PCAN_MESSAGE_STANDARD.value
        else:            
            self._can_msg_obj = TPCANMsgFD()
            # canfd msg dlc is default 15, it will changed by msg contend
            self._can_msg_obj.DLC = 15
            self._can_msg_obj.MSGTYPE = PCAN_MESSAGE_FD.value | PCAN_MESSAGE_BRS.value

        
        print("Successfully initialized.")

    def __del__(self):
        if self.m_DLLFound:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)
        self._file_record.close()

    def getInput(self, msg="Press <Enter> to continue...", default=""):
        res = default
        if sys.version_info[0] >= 3:
            res = input(msg + " ")
        else:
            res = raw_input(msg + " ")
        if len(res) == 0:
            res = default
        return res


    def send_and_receive_messages(self, messages):
        for next_message in messages:
            self.send_and_receive_message(next_message)
            sleep(next_message[delay_for_send_next_msg_index])
            
            
    def send_and_receive_message(self, next_message):
        self._can_msg_obj.ID = next_message[tx_canid_index]
        if self._IsFD == True:
            self._can_msg_obj.DLC = self.GetDLCFromLength(len(next_message[msg_contend_index]))
            pass
        else:
            self._can_msg_obj.LEN = len(next_message[msg_contend_index])

        self.WriteMessages(next_message[msg_contend_index])
        self.ReadMessages(next_message[rx_canid_index])

    def ReadMessages(self, rx_canid):
        """
        Function for reading PCAN-Basic messages
        """
        stsResult = PCAN_ERROR_OK
        is_pending = False
        is_multi_msg = False

        ## We read at least one time the queue looking for messages. If a message is found, we look again trying to 
        ## find more. If the queue is empty or an error occurr, we get out from the dowhile statement.
        start_time = int(round(time.time() * 1000))
        timeout_stamp = start_time + rx_timeout
        # use timeout to control read can msg
        while (int(round(time.time() * 1000)) < timeout_stamp):
            if self._IsFD:
                stsResult, is_pending, is_multi_msg = self.ReadMessageFD(rx_canid)
            else:
                stsResult, is_pending, is_multi_msg = self.ReadMessage(rx_canid)
            if stsResult != PCAN_ERROR_OK and stsResult != PCAN_ERROR_QRCVEMPTY:
                self.ShowStatus(stsResult)
                return
            # got nrc pending or multi msg, so delay
            if is_pending == True:
                timeout_stamp += addition_time_for_pending
            elif is_multi_msg == True:
                timeout_stamp += rx_timeout


    def ReadMessage(self, rx_canid):
        """
        Function for reading CAN messages on normal CAN devices

        Returns:
            A TPCANStatus error code
        """
        ## We execute the "Read" function of the PCANBasic   
        stsResult = self.m_objPCANBasic.Read(self.PcanHandle)
        is_pending = False
        is_multi_msg = False

        if stsResult[0] == PCAN_ERROR_OK:
            ## We show the received message
            is_pending, is_multi_msg = self.ProcessMessageCan(stsResult[1], stsResult[2], rx_canid)

        return (stsResult[0], is_pending, is_multi_msg)

    def ReadMessageFD(self, rx_canid):
        """
        Function for reading messages on FD devices

        Returns:
            A TPCANStatus error code
        """
        ## We execute the "Read" function of the PCANBasic   
        
        stsResult = self.m_objPCANBasic.ReadFD(self.PcanHandle)
        is_pending = False
        is_multi_msg = False

        if stsResult[0] == PCAN_ERROR_OK:
            is_pending, is_multi_msg = self.ProcessMessageCanFd(stsResult[1],stsResult[2], rx_canid)
            
        return (stsResult[0], is_pending, is_multi_msg)

    def ProcessMessageCan(self, msg, itstimestamp, rx_canid):
         """
         Processes a received CAN message
         
         Parameters:
             msg = The received PCAN-Basic CAN message
             itstimestamp = Timestamp of the message as TPCANTimestamp structure
         """
         microsTimeStamp = itstimestamp.micros + (1000 * itstimestamp.millis) + (0x100000000 * 1000 * itstimestamp.millis_overflow)
         msg_can_id =  self.GetIdString(msg.ID, msg.MSGTYPE)
         is_pending = False
         is_multi_msg = False
         if msg_can_id == rx_canid:
            msg_length = self.GetLengthFromDLC(msg.DLC)
            print("\nReceive message:")
            print(self.GetDataString(msg.DATA,msg.MSGTYPE))
            self._file_record.write("Receive message:\n")
            self._file_record.write(self.GetDataString(msg.DATA[:msg_length],msg.MSGTYPE) + "\n")
            print("----------------------------------------------------------")
            if self.log_area:
                log_message = f"Receive message:\n" + self.GetDataString(msg.DATA[:msg_length],msg.MSGTYPE) + "\n"
                self.log_area.insert(tk.END, log_message)  # Insert log message into the text area  
                self.log_area.see(tk.END)  # Scroll to the end of the text area  
                self.log_area.update()
            if rx_canid in rx_uds_msg_id:
                if self.is_nrc_pending(self.GetDataString(msg.DATA,msg.MSGTYPE)):
                    is_pending = True
                if self.is_multi_msg(self.GetDataString(msg.DATA,msg.MSGTYPE)):
                    self.WriteMessages(msg_flow_control)
                    is_multi_msg = True

         return (is_pending, is_multi_msg)

    def ProcessMessageCanFd(self, msg, itstimestamp, rx_canid):
        """
        Processes a received CAN-FD message

        Parameters:
            msg = The received PCAN-Basic CAN-FD message
            itstimestamp = Timestamp of the message as microseconds (ulong)
        """
        msg_can_id =  self.GetIdString(msg.ID, msg.MSGTYPE)
        is_pending = False
        is_multi_msg = False
        if msg.ID == rx_canid:
            msg_length = self.GetLengthFromDLC(msg.DLC)
            print("\nReceive message:")
            print(self.GetDataString(msg.DATA[:msg_length],msg.MSGTYPE))
            self._file_record.write("Receive message:\n")
            self._file_record.write(self.GetDataString(msg.DATA[:msg_length],msg.MSGTYPE) + "\n")
            if self.log_area:
                log_message = f"Receive message:\n" + self.GetDataString(msg.DATA[:msg_length],msg.MSGTYPE) + "\n"
                self.log_area.insert(tk.END, log_message)  # Insert log message into the text area  
                self.log_area.see(tk.END)  # Scroll to the end of the text area  
                self.log_area.update()
            print("----------------------------------------------------------")
            if rx_canid in rx_uds_msg_id:
                if self.is_nrc_pending(self.GetDataString(msg.DATA,msg.MSGTYPE)):
                    is_pending = True
                if self.is_multi_msg(self.GetDataString(msg.DATA,msg.MSGTYPE)):
                    # send flow control asap
                    self.WriteMessages(msg_flow_control)
                    is_multi_msg = True

        return (is_pending, is_multi_msg)

    def is_nrc_pending(self, input_string):
        hex_values = input_string.split(' ')
        if len(hex_values) >= 4:
            second_value = hex_values[1]
            fourth_value = hex_values[3]
            if second_value == '7F' and fourth_value == '78':
                return True
        return False

    def is_multi_msg(self, input_string):
        hex_values = input_string.split(' ')
        if hex_values[0][0] == '1':
            return True
        return False

    def WriteMessages(self, message):
        '''
        Function for writing PCAN-Basic messages
        '''
        self._file_record.write("\nSend message:\n")
        self._file_record.write(self.GetDataString(message, 0) + "\n")
        # self._file_record.write(str([hex(num) for num in message]) + "\n")
        print("\n\nSend message:")
        print(self.GetDataString(message, 0) + "\n")
        if self.log_area:
            log_message = f"\n\nSend message:\n" + self.GetDataString(message, 0) + "\n"
            self.log_area.insert(tk.END, log_message)  # Insert log message into the text area  
            self.log_area.see(tk.END)  # Scroll to the end of the text area  

        if self._IsFD:
            stsResult = self.WriteMessageFD(message)
        else:
            stsResult = self.WriteMessage(message)

        ## Checks if the message was sent
        if (stsResult != PCAN_ERROR_OK):
            print("error, stsResult {}".format(stsResult))
            self.ShowStatus(stsResult)
            

    def WriteMessageFD(self, message):
        """
        Function for writing messages on CAN-FD devices

        Returns:
            A TPCANStatus error code
        """
        ## Sends a CAN-FD message
        self._can_msg_obj.DATA[:len(message)] = message
        return self.m_objPCANBasic.WriteFD(self.PcanHandle, self._can_msg_obj)

    def WriteMessage(self, message):
        """
        Function for writing messages on CAN devices

        Returns:
            A TPCANStatus error code
        """
        ## Sends a CAN message
        self._can_msg_obj.DATA[:self._can_msg_obj.LEN] = message
        return self.m_objPCANBasic.Write(self.PcanHandle, self._can_msg_obj)

    # Help-Functions
    #region
    def CheckForLibrary(self):
        """
        Checks for availability of the PCANBasic library
        """
        ## Check for dll file
        try:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)
            return True
        except :
            print("Unable to find the library: PCANBasic.dll !")
            self.getInput("Press <Enter> to quit...")
            return False 

    def ShowConfigurationHelp(self):
        """
        Shows/prints the configurable parameters for this sample and information about them
        """
        print("=========================================================================================")
        print("|                        PCAN-Basic TimerRead Example                                    |")
        print("=========================================================================================")
        print("Following parameters are to be adjusted before launching, according to the hardware used |")
        print("                                                                                         |")
        print("* PcanHandle: Numeric value that represents the handle of the PCAN-Basic channel to use. |")
        print("              See 'PCAN-Handle Definitions' within the documentation                     |")
        print("* IsFD: Boolean value that indicates the communication mode, CAN (false) or CAN-FD (true)|")
        print("* Bitrate: Numeric value that represents the BTR0/BR1 bitrate value to be used for CAN   |")
        print("           communication                                                                 |")
        print("* BitrateFD: String value that represents the nominal/data bitrate value to be used for  |")
        print("             CAN-FD communication                                                        |")
        print("  TimerInterval: The time, in milliseconds, to wait before trying to write a message     |")
        print("=========================================================================================")
        print("")

    def ShowCurrentConfiguration(self):
        """
        Shows/prints the configured paramters
        """
        print("Parameter values used")
        print("----------------------")
        print("* PCANHandle= " + self.FormatChannelName(self.PcanHandle,self._IsFD))
        print("* IsFD= " + str(self._IsFD))
        if (self._IsFD == True):
            print("* BitrateFD= " + self.ConvertBytesToString(self.BitrateFD))
        else:
            print("* Bitrate= " + self.ConvertBitrateToString(self.Bitrate))
        print("")

    def ShowStatus(self,status):
        """
        Shows formatted status

        Parameters:
            status = Will be formatted
        """
        print("=========================================================================================")
        print(self.GetFormattedError(status))
        print("=========================================================================================")
    
    def FormatChannelName(self, handle, isFD=False):
        """
        Gets the formated text for a PCAN-Basic channel handle

        Parameters:
            handle = PCAN-Basic Handle to format
            isFD = If the channel is FD capable

        Returns:
            The formatted text for a channel
        """
        handleValue = handle.value
        if handleValue < 0x100:
            devDevice = TPCANDevice(handleValue >> 4)
            byChannel = handleValue & 0xF
        else:
            devDevice = TPCANDevice(handleValue >> 8)
            byChannel = handleValue & 0xFF

        if isFD:
           return ('%s: FD %s (%.2Xh)' % (self.GetDeviceName(devDevice.value), byChannel, handleValue))
        else:
           return ('%s: %s (%.2Xh)' % (self.GetDeviceName(devDevice.value), byChannel, handleValue))

    def GetFormattedError(self, error):
        """
        Help Function used to get an error as text

        Parameters:
            error = Error code to be translated

        Returns:
            A text with the translated error
        """
        ## Gets the text using the GetErrorText API function. If the function success, the translated error is returned.
        ## If it fails, a text describing the current error is returned.
        stsReturn = self.m_objPCANBasic.GetErrorText(error,0x09)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            message = str(stsReturn[1])
            return message.replace("'","",2).replace("b","",1)

    def GetLengthFromDLC(self, dlc):
        """
        Gets the data length of a CAN message

        Parameters:
            dlc = Data length code of a CAN message

        Returns:
            Data length as integer represented by the given DLC code
        """
        if dlc == 9:
            return 12
        elif dlc == 10:
            return 16
        elif dlc == 11:
            return 20
        elif dlc == 12:
            return 24
        elif dlc == 13:
            return 32
        elif dlc == 14:
            return 48
        elif dlc == 15:
            return 64
        
        return dlc
    
    def GetDLCFromLength(self, length):
        """
        Gets the data DLC of a CAN message

        Parameters:
            length = Data length code of a CAN message

        Returns:
            Data DLC as integer represented by the given length
        """
        if length <= 8:
            return length
        elif length <= 12:
            return 9
        elif length <= 16:
            return 10
        elif length <= 20:
            return 11
        elif length <= 24:
            return 12
        elif length <= 32:
            return 13
        elif length <= 48:
            return 14
        elif length <= 64:
            return 15
        else:
            return 0

    def GetIdString(self, id, msgtype):
        """
        Gets the string representation of the ID of a CAN message

        Parameters:
            id = Id to be parsed
            msgtype = Type flags of the message the Id belong

        Returns:
            Hexadecimal representation of the ID of a CAN message
        """
        if (msgtype & PCAN_MESSAGE_EXTENDED.value) == PCAN_MESSAGE_EXTENDED.value:
            return '%.8Xh' %id
        else:
            return '%.3Xh' %id

    def GetTimeString(self, time):
        """
        Gets the string representation of the timestamp of a CAN message, in milliseconds

        Parameters:
            time = Timestamp in microseconds

        Returns:
            String representing the timestamp in milliseconds
        """
        # time = (time.split('(')[1]).split(')')[0]
        time = int(time.value)
        time_milliseconds = (time) / 1000
        return str(time_milliseconds)

    def GetTypeString(self, msgtype):  
        """
        Gets the string representation of the type of a CAN message

        Parameters:
            msgtype = Type of a CAN message

        Returns:
            The type of the CAN message as string
        """
        if (msgtype & PCAN_MESSAGE_STATUS.value) == PCAN_MESSAGE_STATUS.value:
            return 'STATUS'
        
        if (msgtype & PCAN_MESSAGE_ERRFRAME.value) == PCAN_MESSAGE_ERRFRAME.value:
            return 'ERROR'        
        
        if (msgtype & PCAN_MESSAGE_EXTENDED.value) == PCAN_MESSAGE_EXTENDED.value:
            strTemp = 'EXT'
        else:
            strTemp = 'STD'

        if (msgtype & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value:
            strTemp += '/RTR'
        else:
            if (msgtype > PCAN_MESSAGE_EXTENDED.value):
                strTemp += ' ['
                if (msgtype & PCAN_MESSAGE_FD.value) == PCAN_MESSAGE_FD.value:
                    strTemp += ' FD'
                if (msgtype & PCAN_MESSAGE_BRS.value) == PCAN_MESSAGE_BRS.value:                    
                    strTemp += ' BRS'
                if (msgtype & PCAN_MESSAGE_ESI.value) == PCAN_MESSAGE_ESI.value:
                    strTemp += ' ESI'
                strTemp += ' ]'
                
        return strTemp

    def GetDataString(self, data, msgtype):
        """
        Gets the data of a CAN message as a string

        Parameters:
            data = Array of bytes containing the data to parse
            msgtype = Type flags of the message the data belong

        Returns:
            A string with hexadecimal formatted data bytes of a CAN message
        """
        if (msgtype & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value:
            return "Remote Request"
        else:
            strTemp = b""
            for x in data:
                strTemp += b'%.2X ' % x
            return str(strTemp).replace("'","",2).replace("b","",1)

    def GetDeviceName(self, handle):
        """
        Gets the name of a PCAN device

        Parameters:
            handle = PCAN-Basic Handle for getting the name

        Returns:
            The name of the handle
        """
        switcher = {
            PCAN_NONEBUS.value: "PCAN_NONEBUS",
            PCAN_PEAKCAN.value: "PCAN_PEAKCAN",
            PCAN_ISA.value: "PCAN_ISA",
            PCAN_DNG.value: "PCAN_DNG",
            PCAN_PCI.value: "PCAN_PCI",
            PCAN_USB.value: "PCAN_USB",
            PCAN_PCC.value: "PCAN_PCC",
            PCAN_VIRTUAL.value: "PCAN_VIRTUAL",
            PCAN_LAN.value: "PCAN_LAN"
        }

        return switcher.get(handle,"UNKNOWN")   

    def ConvertBitrateToString(self, bitrate):
        """
        Convert bitrate c_short value to readable string

        Parameters:
            bitrate = Bitrate to be converted

        Returns:
            A text with the converted bitrate
        """
        m_BAUDRATES = {PCAN_BAUD_1M.value:'1 MBit/sec', PCAN_BAUD_800K.value:'800 kBit/sec', PCAN_BAUD_500K.value:'500 kBit/sec', PCAN_BAUD_250K.value:'250 kBit/sec',
                       PCAN_BAUD_125K.value:'125 kBit/sec', PCAN_BAUD_100K.value:'100 kBit/sec', PCAN_BAUD_95K.value:'95,238 kBit/sec', PCAN_BAUD_83K.value:'83,333 kBit/sec',
                       PCAN_BAUD_50K.value:'50 kBit/sec', PCAN_BAUD_47K.value:'47,619 kBit/sec', PCAN_BAUD_33K.value:'33,333 kBit/sec', PCAN_BAUD_20K.value:'20 kBit/sec',
                       PCAN_BAUD_10K.value:'10 kBit/sec', PCAN_BAUD_5K.value:'5 kBit/sec'}
        return m_BAUDRATES[bitrate.value]
    
    def ConvertBytesToString(self, bytes):
        """
        Convert bytes value to string

        Parameters:
            bytes = Bytes to be converted

        Returns:
            Converted bytes value as string
        """
        return str(bytes).replace("'","",2).replace("b","",1)


class App:  
    def __init__(self, master):  
        self.master = master  
        master.title("CAN Message Configuration")  
        master.geometry("800x600")  

        self.check_vars_external = []  
        self.check_vars_internal = []
        self.check_vars_function_did = []
        self.check_session_switch = []
        self.checkboxes_external = []  
        self.checkboxes_internal = []
        self.checkboxes_function_did = []
        self.checkboxes_session_switch = []


        # Frame for checkboxes with a scrollbar  
        self.checkbox_frame = tk.Frame(master)  
        self.checkbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))  

        self.canvas = tk.Canvas(self.checkbox_frame)  
        self.scrollbar = tk.Scrollbar(self.checkbox_frame, orient="vertical", command=self.canvas.yview)  
        self.scrollable_frame = tk.Frame(self.canvas)  

        self.scrollable_frame.bind(  
            "<Configure>",  
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))  
        )  

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")  
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  

        self.create_checkboxes()

        # Keep Alive Checkbox  
        self.keep_alive_var = tk.BooleanVar(value=False)  # Default value is False  
        self.keep_alive_checkbox = tk.Checkbutton(master, text="Circlely Send Keep Alive", variable=self.keep_alive_var, command=self.toggle_keep_alive)  
        self.keep_alive_checkbox.pack(pady=5)  

        # Submit button  
        self.submit_button = tk.Button(master, text="Send msg", command=self.submit, height=2, width=20)  
        self.submit_button.pack(pady=5)  

        # Clear log button  
        self.clear_log_button = tk.Button(master, text="Clean log", command=self.clear_log, height=2, width=20)  
        self.clear_log_button.pack(pady=5)  
    
        # Import can msg
        self.import_can_msg_button = tk.Button(master, text="Import can msg", command=self.import_can_msg, height=2, width=20)  
        self.import_can_msg_button.pack(pady=5)  

        # Input data area  
        self.input_area = scrolledtext.ScrolledText(master, width=40, height=5)  # Adjust width as needed  
        self.input_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))



        # Log Text Area  
        self.log_area = scrolledtext.ScrolledText(master, width=100, height=10)  
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))  


        # Redirect print output to the log area  
        self.log_stream = io.StringIO()  
        sys.stdout = self.log_stream  

        # Bind mouse wheel scrolling to specific widgets  
        self.log_area.bind("<MouseWheel>", self.on_mouse_wheel)  
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  

        self.is_can_fd = True  
        self.need_keep_alive = False  
        self.uds_client = UDSClient(self.is_can_fd, self.need_keep_alive, self.log_area)  

        self.keep_alive_thread = None  # Thread for keep_alive messages  

    def create_checkboxes(self):  
        # Frame for internal DID checkboxes with a label frame  
        internal_frame = tk.LabelFrame(self.scrollable_frame, text="Read Internal DID", padx=10, pady=10)  
        internal_frame.pack(side=tk.LEFT, padx=10, pady=10)  

        # Select all internal DID button  
        select_all_internal_button = tk.Button(internal_frame, text="Select all/Clean all", command=self.toggle_internal_dids)  
        select_all_internal_button.pack(pady=5)  

        for idx, config in enumerate(read_all_internal_did_sequence):  
            var = tk.BooleanVar()  
            checkbox = tk.Checkbutton(internal_frame, text=f"{config[-1]}", variable=var, font=("Arial", 12))  
            checkbox.pack(anchor='w', padx=5, pady=2)  
            self.check_vars_internal.append(var)  
            self.checkboxes_internal.append(config)  

        # Frame for external DID checkboxes with a label frame  
        external_frame = tk.LabelFrame(self.scrollable_frame, text="Read External DID", padx=10, pady=10)  
        external_frame.pack(side=tk.LEFT, padx=10, pady=10)  

        # Select all external DID button  
        select_all_external_button = tk.Button(external_frame, text="Select all/Clean all", command=self.toggle_external_dids)  
        select_all_external_button.pack(pady=5)  

        for idx, config in enumerate(read_all_external_did_sequence):  
            var = tk.BooleanVar()  
            checkbox = tk.Checkbutton(external_frame, text=f"{config[-1]}", variable=var, font=("Arial", 12))  
            checkbox.pack(anchor='w', padx=5, pady=2)  
            self.check_vars_external.append(var)  
            self.checkboxes_external.append(config)

        # Frame for function address DID checkboxes with a label frame  
        function_did_frame = tk.LabelFrame(self.scrollable_frame, text="Read DID With Function Address", padx=10, pady=10)  
        function_did_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Select all DID function button  
        select_all_function_did_button = tk.Button(function_did_frame, text="Select all/Clean all", command=self.toggle_function_dids)  
        select_all_function_did_button.pack(pady=5)  

        for idx, config in enumerate(read_all_function_did_sequence):  
            var = tk.BooleanVar()  
            checkbox = tk.Checkbutton(function_did_frame, text=f"{config[-1]}", variable=var, font=("Arial", 12))  
            checkbox.pack(anchor='w', padx=5, pady=2)  
            self.check_vars_function_did.append(var)  
            self.checkboxes_function_did.append(config)  

        # Frame for session switch checkboxes with a label frame  
        session_switch_frame = tk.LabelFrame(self.scrollable_frame, text="Session Switch", padx=10, pady=10)  
        session_switch_frame.pack(side=tk.TOP, padx=10, pady=10)

        for idx, config in enumerate(switch_session_sequence):
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(session_switch_frame, text=f"{config[-1]}", variable=var, font=("Arial", 12))  
            checkbox.pack(anchor='w', padx=5, pady=2)  
            self.check_session_switch.append(var)
            self.checkboxes_session_switch.append(config)

    def toggle_keep_alive(self):  
        if self.keep_alive_var.get():  
            self.need_keep_alive = True  
            self.keep_alive_thread = threading.Thread(target=self.keep_alive_messages)  
            self.keep_alive_thread.start()  
        else:  
            self.need_keep_alive = False

    def keep_alive_messages(self):
        while self.need_keep_alive:  
            self.uds_client.send_and_receive_messages([msg_keep_alive])  # Send keep_alive message  
            time.sleep(3)  # Wait for 1 second  

    def submit(self):  
        threading.Thread(target=self.send_messages).start()

    def send_messages(self):  
        selected_sequences = [self.checkboxes_external[idx] for idx, var in enumerate(self.check_vars_external) if var.get()]  
        selected_sequences += [self.checkboxes_internal[idx] for idx, var in enumerate(self.check_vars_internal) if var.get()]
        selected_sequences += [self.checkboxes_function_did[idx] for idx, var in enumerate(self.check_vars_function_did) if var.get()]
        selected_sequences += [self.checkboxes_session_switch[idx] for idx, var in enumerate(self.check_session_switch) if var.get()]

        # Parse input area data
        input_data = self.input_area.get("1.0", tk.END).strip().splitlines()  
        can_messages = []  
        for line in input_data:  
            try:  
                can_message = eval(line)  # Evaluate the line to convert it to a Python object  
                can_messages.append(can_message)  
            except Exception as e:  
                messagebox.showerror("Error", f"Invalid input format: {line}\n{str(e)}")  
                return  

        if not selected_sequences and not can_messages:  
            messagebox.showwarning("Warning", "Please select at least one item or enter CAN messages")  
            return  

        # Log the selected sequences and input messages  
        log_message = f"Selected sequences: {selected_sequences}\nCAN Messages: {can_messages}\n"   
        self.log_area.insert(tk.END, log_message)  
        self.log_area.see(tk.END)  
        self.log_area.update()  

        # Simulate sending messages and waiting  
        self.uds_client.send_and_receive_messages(selected_sequences + can_messages)  

    def toggle_internal_dids(self):  
        all_checked = all(var.get() for var in self.check_vars_internal)  
        new_state = not all_checked  
        for var in self.check_vars_internal:  
            var.set(new_state)  

    def toggle_external_dids(self):  
        all_checked = all(var.get() for var in self.check_vars_external)  
        new_state = not all_checked  
        for var in self.check_vars_external:  
            var.set(new_state)  

    def toggle_function_dids(self):  
        all_checked = all(var.get() for var in self.check_vars_function_did)  
        new_state = not all_checked  
        for var in self.check_vars_function_did:
            var.set(new_state)  

    def clear_log(self):  
        """Clear the log area."""  
        self.log_area.delete(1.0, tk.END)  # Delete all content from the log area 

    def import_can_msg(self):
        file_path = filedialog.askopenfilename(title="Select Config File",  
        filetypes=[("CAN_MSG File", "*.can_msg")]
)  
        if file_path:
            with open(file_path, 'r') as file:  
                content = file.read()  
                self.input_area.delete("1.0", tk.END)  # Clear existing content  
                self.input_area.insert(tk.END, content)  # Insert file content into input area 

    def on_mouse_wheel(self, event):  
        # Check which widget the mouse is over  
        widget = event.widget  
        if isinstance(widget, tk.Text) or isinstance(widget, scrolledtext.ScrolledText):  
            # Scroll the log area  
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")  
        elif widget == self.canvas:  
            # Scroll the canvas  
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")  

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


# if __name__ == "__main__":
#     uds_client = UDSClient(is_can_fd, need_keep_alive)
#     uds_client.send_and_receive_messages(channel_open)

# Starts the program
# if __name__ == "__main__":
    # choice = input("Select shell or gui (shall: 1, gui: 2)? ")
    # if choice == "1":  
    #     uds_client = UDSClient(is_can_fd, need_keep_alive)
    #     uds_client.send_and_receive_messages([read_did_0104_internal])
    # elif choice == "2":
    # root = tk.Tk()
    # app = App(root)
    # root.mainloop()
    # else:
        # print("Invalid input, please input '1" or '2')



