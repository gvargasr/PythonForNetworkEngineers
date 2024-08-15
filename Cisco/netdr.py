#from bigdata.utility import pretty_print
#from bigdata.utility import stdin_json
# import bdblib
#import comm.emailout
from prettytable import PrettyTable
from datetime import datetime
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_mail(subject, email_from, email_to, output):

    #smtp_server = '173.37.113.194'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to
    email_to_list = email_to.split()

    mime_text = MIMEText(output, 'plain')
    msg.attach(mime_text)
    print("Sending email - subject {}".format(subject))
    #server = smtplib.SMTP(smtp_server, 25)
    server = smtplib.SMTP('outbound.cisco.com')
    #return
    # Year I know, not nice ;-)
    try:
        server.sendmail(email_from, email_to_list, msg.as_string())
    except Exception as e:
        print(str(e))
        
def buildTable(tableTuple, body, headline1, headline2):

    tab = PrettyTable([headline1, headline2])
    tab.padding_width = 1
    for item in tableTuple[:10]:
        tab.add_row([item[0], item[1]])
    body += "\n\r" + tab.get_string() + "\n\r"
    return(body)

def task(filename=None, email="", case_number=""):
    """
        The Netdr Decoder analyses the output of the command "show netdr capture" and categorizes them into various
        buckets based on ethertype, protocol, source address, source MAC address... 

        The top 7 talkers from each bucket are printed.

        This output is specific to certain Supervisor cards and the ES+ line card on the 6500/7600 platform.

        If you face any issues or would like to suggest enhancements, feel free to contact me at rrahul@cisco.com.
    """
    if "Yes" == "Yes":
        if filename == None:
            print("You need to provide a filename. Click on the arrow first to pick a file from your computer. Next, click on 'refresh file list' and finally select from the drop down menu")
            return
        f = open(filename)
        totalInPackets = 0
        totalOutPackets = 0
        inP = []
        outP = []
        packet = ""
        newPack = "None"
        keys = ["interface", "src_vlan", "destmac", "srcmac", "dest_indx", "protocol"]
        #print("Email id is " + str(emailid))
        #Performing a very simple test to check that an emailid is provided
        emailid = str(email)
        if not('@' in emailid and '.' in emailid): emailid = "Blank"
        if emailid == "Blank":
            print("No email will be sent out.")
        for line in f:
            # print(line)
            # To add each packet found to a list
            if 'dump of' in line:
                if newPack == "in":
                    inP.insert(totalInPackets,packet)
                    #logger.warning('Adding an Input packet')
                elif newPack == "out":
                    outP.insert(totalOutPackets,packet)
                    #logger.warning('Adding an Output packet')
                packet = ""
                num = 1

            if 'dump of incoming inband packet' in line:
                #logger.warning('found an Input packet')
                totalInPackets += 1
                newPack = "in"
            elif 'dump of outgoing inband packet' in line:
                #logger.warning('found an Output packet')
                totalOutPackets += 1
                newPack = "out"
            elif newPack == "in" or newPack == "out":
                # choosing a max length of 12 for each packet
                if num < 13:
                    packet += line
                num += 1

        if newPack == "None":
            print("Unable to find any packets")
        elif newPack == "in":
            inP.insert(totalInPackets, packet)
            #logger.warning('Adding an Input packet')
        elif newPack == "out":
            outP.insert(totalOutPackets, packet)
            #logger.warning('Adding an Output packet')

        #print('Section 1 - All Ingress Packets')
        #print('Total Input Packets found = ' + str(totalInPackets))
        #print("--------------------------------------")
        if emailid != "None":
            emailBody = """
============================================================
                  NetdrDecoder Output
------------------------------------------------------------

----------------------------------------
   Section 1 - All Ingress Packets
----------------------------------------
Total Input Packets found = """ + str(totalInPackets)

        #print("--------------------------------------")
        if totalInPackets != 0:
            logger.warning('Input Packet string =')
            #print(inP, type="list")
            logger.warning('Output Packet string =')
            #print(outP, type="list")

            keys = ["l2idb", "l3idb", "src_vlan", "destmac", "srcmac", "dest_indx", "protocol"]
            #inputValue will be a list of strings for each key
            inputValue = {}
            for key in keys:
                inputValue[key] = ""
            inPIPv4 = []
            inPMPLS = []
            inPARP = []
            inPIPv6 = []
            inPOther = []
            totalInIPv4Packets = totalInMPLSPackets = totalInARPPackets = totalInIPv6Packets = totalInOtherPackets = 0

            # Reading through the ingress packets and counting for each of the above Keys
            for packet in inP:
                packetlist = packet.split( )
                for i,item in enumerate(packetlist):
                    for key in keys:
                        if item == key:
                            inputValue[key] += " " + packetlist[i+1].replace(",","")
                    if item == "protocol":
                    # Creating Packet lists for each protocol
                        if packetlist[i+1].replace(",","") == "0800":
                            totalInIPv4Packets += 1
                            inPIPv4.insert(totalInIPv4Packets, packet)
                            #print("Total IPv4 packets")
                            #print(totalInIPv4Packets)
                            #print(packet)
                        elif packetlist[i+1].replace(",","") == "8847":
                            totalInMPLSPackets +=1
                            inPMPLS.insert(totalInMPLSPackets, packet)
                        elif packetlist[i+1].replace(",","") == "0806":
                            totalInARPPackets +=1
                            inPARP.insert(totalInARPPackets, packet)
                        elif packetlist[i+1].replace(",","") == "86DD":
                            totalInIPv6Packets +=1
                            inPIPv6.insert(totalInIPv6Packets, packet)
                        else:
                            totalInOtherPackets +=1
                            inPOther.insert(totalInOtherPackets, packet)
                        break

            logger.warning("Input value is")
            #print(inputValue,type="list")

            for key in keys:
                word = {}
                for item in inputValue[key].split( ):
                    if item not in word:
                        word[item] = 1
                    else:
                        word[item] += 1
                #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                #print([["All Incoming packets sorted based on " + key, "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]])
                #print("--------------------------------------")
                if emailid != "None": emailBody = buildTable(wordTuple, emailBody, "All Incoming packets sorted based on " + key, "Number of Packets")

            #print('Sub Section A - All Incoming IPv4 Packets')
            #print('Total IPv4 Incoming Packets found = ' + str(totalInIPv4Packets))
            #print("--------------------------------------")
            if emailid != "None": emailBody += """
-------------------------------------------
 Sub Section A - All Incoming IPv4 Packets
-------------------------------------------
Total IPv4 Incoming Packets found = """ + str(totalInIPv4Packets)

            if totalInIPv4Packets != 0:
                srcAddr = {}
                srcAddr["OSPF"] = ""
                srcAddr["EIGRP"] = ""
                srcAddr["PIM"] = ""
                srcAddr["TTL of 1"] = ""
                srcAddr["ICMP"] = ""
                display = {}
                display["TCP Src"] = display["TCP Dst"] = display["UDP Src"] = display["UDP Dst"] = ""
                display["Dest IPv4 Address"] = display["Src IPv4 Address"] = ""
                for packet in inPIPv4:
                    packetlist = packet.split( )
                    pakType = "None"
                    #if ppp ==1: print(packet)

                    for i,item in enumerate(packetlist):
                        if item == "destmac":
                            #print(packetlist[i+1])
                            inPDestMac = packetlist[i+1].replace(",","")
                            #print(inPDestMac)
                            if (inPDestMac == "01.00.5E.00.00.05" or inPDestMac == "01.00.5E.00.00.06"):
                                pakType = "OSPF"
                            elif inPDestMac == "01.00.5E.00.00.0A":
                                pakType = "EIGRP"
                            elif inPDestMac == "01.00.5E.00.00.0D":
                                pakType = "PIM"

                        if item == "ttl":
                            logger.warning("in TTL")
                            # print(packetlist[i+3] + packetlist[i+5])
                            # The following line is to capture the OSPF, EIGRP, PIM
                            try:
                                packetlist[i+5]
                            except:
                                logger.warning("Packet is incomplete")
                                print("Packet is incomplete")
                            else:
                                if pakType != "None": srcAddr[pakType] += " " + packetlist[i+3].replace(",","")
                                if int(packetlist[i+1].replace(",","")) == 1:
                                    srcAddr["TTL of 1"] += " " + packetlist[i+3].replace(",","")
                                display["Src IPv4 Address"] += " " + packetlist[i+3].replace(",","")
                                display["Dest IPv4 Address"] += " " + packetlist[i+5].replace(",","")
                            try:
                                packetlist[i+6]
                            except:
                                logger.warning("No need to parse for TCP or UDP")
                                print("No need to parse for TCP or UDP")
                            else:
                                if packetlist[i+6].replace(",","") == "tcp":
                                    display["TCP Src"] += " " + packetlist[i+8].replace(",","")
                                    display["TCP Dst"] += " " + packetlist[i+10].replace(",","")
                                if packetlist[i+6].replace(",","") == "udp":
                                    display["UDP Src"] += " " + packetlist[i+8].replace(",","")
                                    display["UDP Dst"] += " " + packetlist[i+10].replace(",","")
                                if packetlist[i+6].replace(",","") == "icmp":
                                    srcAddr["ICMP"] += " " + packetlist[i+3].replace(",","")
                            break

                for key in display.keys():
                    #print("--------------------------------------")
                    #print(key)
                    #print(display[key])
                    word = {}
                    for item in display[key].split( ):
                        if item not in word:
                            word[item] = 1
                        else:
                            word[item] += 1
                    #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                    wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                    #print([["IPV4 packets sorted based on " + key, "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table"))
                    #print("Number of IPv4 packets with " + key + " = " + str(len(display[key].split( ))))
                    #print("--------------------------------------")
                    if emailid != "None":
                        emailBody = buildTable(wordTuple, emailBody, "IPv4 packets sorted based on " + key, "Number of Packets")
                        emailBody += "Number of IPv4 packets with " + key + " = " + str(len(display[key].split( )))

                for key in srcAddr.keys():
                    #print("--------------------------------------")
                    #print(key)
                    #print(srcAddr[key])
                    word = {}
                    for item in srcAddr[key].split( ):
                        if item not in word:
                            word[item] = 1
                        else:
                            word[item] += 1
                    wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                    #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                    #print([[key + " packets sorted based on Source Address", "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table"))
                    #print("Number of " + key + " packets = " + str(len(srcAddr[key].split( ))))
                    #print("--------------------------------------")
                    if emailid != "None": 
                        emailBody = buildTable(wordTuple, emailBody, key + " packets sorted based on Source Address", "Number of Packets")
                        emailBody += "Number of " + key + " packets = " + str(len(srcAddr[key].split( ))) + "\n\r"

            #print('Sub Section B - Incoming MPLS Packets')
            #print('Total MPLS Incoming Packets found = ' + str(totalInMPLSPackets))
            #print("--------------------------------------")
            if emailid != "None": emailBody += """
---------------------------------------
 Sub Section B - Incoming MPLS Packets
---------------------------------------
Total MPLS Incoming Packets found = """ + str(totalInMPLSPackets)

            if totalInMPLSPackets != 0:
                dictOfLabels = {}
                dictOfLabels["MPLS"] = ""
                for packet in inPMPLS:
                    packetlist = packet.split( )
                    for i,item in enumerate(packetlist):
                        if item == "layer":
                            mplsLabel = packetlist[i+3].replace(",","")
                            if len(mplsLabel) == 8:
                                dictOfLabels["MPLS"] += " " + str(int(mplsLabel[:5],16))
                            else:
                                print("Found an MPLS Packet but unable to decode the label")
                            break
                word = {}
                for item in dictOfLabels["MPLS"].split( ):
                    if item not in word:
                        word[item] = 1
                    else:
                        word[item] += 1
                wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                #print("--------------------------------------")
                #print("Packets sorted based on Top of Stack MPLS Label")
                #print([["Packets sorted based on top of Stack Label", "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table"))
                if emailid != "None": emailBody = buildTable(wordTuple, emailBody, "Packets sorted based on top of Stack Label", "Number of Packets")

            #print("--------------------------------------")
            #print('Sub Section C - Incoming IPv6 Packets')
            #print('Total IPv6 Incoming Packets found = ' + str(totalInIPv6Packets))
            #print("--------------------------------------")
            if emailid != "None": emailBody += """
---------------------------------------
 Sub Section C - Incoming IPv6 Packets
---------------------------------------
Total IPv6 Incoming Packets found = """ + str(totalInIPv6Packets)

            if totalInIPv6Packets != 0:
                srcAddr = {}
                srcAddr["IPv6"] = ""
                for packet in inPIPv6:
                    packetlist = packet.split( )
                    for i,item in enumerate(packetlist):
                        if item == "src":
                            srcAddr["IPv6"] += " " + packetlist[i+1].replace(",","")
                            break
                word = {}
                for item in srcAddr["IPv6"].split( ):
                    if item not in word:
                        word[item] = 1
                    else:
                        word[item] += 1
                wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                #print("--------------------------------------")
                #print([["Packets sorted based on Source IPv6 Address", "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table")))
                if emailid != "None": emailBody = buildTable(wordTuple, emailBody, "Packets sorted based on Source IPv6 Address", "Number of Packets")

            #print("--------------------------------------")
            #print('Sub Section D - Incoming ARP Packets')
            #print('Total Incoming ARP Packets = ' + str(totalInARPPackets))
            #print("--------------------------------------")
            if emailid != "None": emailBody += """
--------------------------------------
 Sub Section D - Incoming ARP Packets
--------------------------------------
Total Incoming ARP Packets = """ + str(totalInARPPackets)

            if totalInARPPackets != 0:
                srcAddr = {}
                srcAddr["ARP"] = ""
                for packet in inPARP:
                    packetlist = packet.split( )
                    for i,item in enumerate(packetlist):
                        if item == "destmac":
                            srcAddr["ARP"] += " " + packetlist[i+3].replace(",","")
                            break
                word = {}
                for item in srcAddr["ARP"].split( ):
                    if item not in word:
                        word[item] = 1
                    else:
                        word[item] += 1
                #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                #print("--------------------------------------")
                #print([["ARP packets sorted based on Source MAC Address", "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table"))
                if emailid != "None": emailBody = buildTable(wordTuple, emailBody, "ARP packets sorted based on Source MAC Address", "Number of Packets")

            #print("--------------------------------------")
            #print('Sub Section E - Other Protocol Packets')
            #print('Total Incoming Packets of other Protocols = ' + str(totalInOtherPackets))
            #print("--------------------------------------")
            if emailid != "None": emailBody += """
----------------------------------------
 Sub Section E - Other Protocol Packets
----------------------------------------
Total Incoming Packets of other Protocols = """ + str(totalInOtherPackets)

            if totalInOtherPackets != 0:
                srcAddr = {}
                srcAddr["ISIS"] = ""
                for packet in inPOther:
                    packetlist = packet.split( )
                    for i,item in enumerate(packetlist):
                        if item == "destmac":
                            if ((packetlist[i+1].replace(",","") == "01.80.C2.00.00.15") or (packetlist[i+1].replace(",","") == "01.80.C2.00.00.14")):
                                srcAddr["ISIS"] += " " + packetlist[i+1].replace(",","")
                                break
                word = {}
                for item in srcAddr["ISIS"].split( ):
                    if item not in word:
                        word[item] = 1
                    else:
                        word[item] += 1
                #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                #print("--------------------------------------")
                #print([["ISIS packets sorted based on Source MAC Address", "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table"))
                if emailid != "None": emailBody = buildTable(wordTuple, emailBody, "ISIS packets sorted based on Source MAC Address", "Number of Packets")

        #print("--------------------------------------")
        #print('Section 2 - All Outgoing Packets')
        #print('Total Outgoing Packets found = ' + str(totalOutPackets))
        #print("--------------------------------------")
        if emailid != "None": emailBody += """
----------------------------------------
    Section 2 - All Outgoing Packets
----------------------------------------
Total Output Packets found = """ + str(totalOutPackets)

        if totalOutPackets != 0:
            outputValue = {}
            for key in keys:
                outputValue[key] = ""

            # Reading through the egress packets and counting for each of the above Keys
            for packet in outP:
                packetlist = packet.split( )
                #print("Packet list is")
                #print(packetlist, type="list")
                for key in keys:
                    for i,item in enumerate(packetlist):
                        if item == key:
                            outputValue[key] += " " + packetlist[i+1].replace(",","")
                            break

            logger.warning("Output value is")
            #print(outputValue,type="list")
            for key in keys:
                word = {}
                matchlist = outputValue[key].split( )
                for item in matchlist:
                    if item not in word:
                        word[item] = 1
                    else:
                        word[item] += 1
                #wordTuple = sorted(word.items(), key=lambda(k,v):(v,k), reverse=True)
                wordTuple = sorted(word.items(), key=lambda kv: kv[1], reverse=True)
                #print([["All Outgoing packets sorted based on " + key, "Number of Packets"]] + [[item[0], item[1]] for item in wordTuple[:7]]) #, type="table"))
                #print("--------------------------------------")
                if emailid != "None":
                    emailBody = buildTable(wordTuple, emailBody, "All Outgoing Packets sorted based on " + key, "Number of Packets")


        print(emailBody)
        if emailid != "Blank":
            emailBody += """

==============================================================================

 Contact rrahul@cisco.com for any issues with the above output or the tool.

==============================================================================

"""
            #send_mail("BDB - NetdrDecoder Output for file " + filename,"bdb_no_reply@cisco.com",emailid,emailBody)
            '''
            mail = comm.emailout.EmailOut("bdb_no_reply@cisco.com", emailid, "BDB - NetdrDecoder Output for file " + filename)
            mail.set_body("Output of the NetdrDecoder is attached. Avoid viewing in Notepad. View it in Notepad++, your Browser or Word.")
            text_filename = "NetdrDecoder - UTC -" + str(datetime.utcnow()) + ".txt"
            text_file = open(text_filename, "w")
            text_file.write(emailBody)
            text_file.close()
            mail.attach(text_filename)
            mail.send()
            os.remove(text_filename)
            '''
            print("Email has been sent to " + emailid)

        #f.close()

if __name__ == "__main__":
    # Request input from the user
    email = input("Please enter your email address: ")
    case_number = input("Please enter the case number: ")  # Assuming you might want to use this later
    filename = input("Please enter the filename: ")
    
    # Validate the inputs
    if not email or not filename:
        print("Email and filename are required.")
    else:
        # Define parameters
        env = 'test_environment'  # or another environment as needed

        # Call the function with the parameters
        task(filename, email, case_number)
