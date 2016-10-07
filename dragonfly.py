import speech_recognition
import pyttsx
import os

speech_engine = pyttsx.init('espeak')
speech_engine.setProperty('rate', 150)


def speak(text):
    speech_engine.say(text)
    speech_engine.runAndWait()
recognizer = speech_recognition.Recognizer()


def listen():
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # return recognizer.recognize_sphinx(audio)
        return recognizer.recognize_google(audio)
    except speech_recognition.UnknownValueError:
        return "Could not understand audio"
    except speech_recognition.RequestError as e:
        return("Recog Error; {0}".format(e))


def ask_again():
    listen_again = listen().lower().split()
    print(listen_again[0])
    return listen_again[0]


def make_directory(output_list):
    print(os.getcwd() + "/" + output_list[-1])
    os.mkdir(os.getcwd() + "/" + output_list[-1])
    print("path created")


def move_back():

    if(os.getcwd() != "/home/" + os.getenv('USERNAME')):
        print(os.getcwd())
        os.chdir("..")
        print(os.getcwd())
    else:
        print("Please enter before you proceed!")
        passwd = ask_again()
        if(passwd == "iphone"):
            os.chdir("..")
            print(os.getcwd())
        else:
            print("Sorry! you can't move back from this directory")
            speak("Sorry! you can't move back from this directory")


def change_directory(output_list):
    capital = output_list[-1].title()
    if os.path.exists(os.getcwd() + "/" + output_list[-1]):
        os.chdir(output_list[-1])
        print(os.getcwd())
    elif os.path.exists(os.getcwd() + "/" + capital):
        os.chdir(capital)
        print(os.getcwd())
    else:
        print("Do you want to create a directory(y/n)")
        speak("Do you want to create a directory(y/n)")
        cd_listen = ask_again()
        if(cd_listen == "y" or cd_listen == "yes"):
            os.mkdir(os.getcwd() + "/" + output_list[-1])
            os.chdir(output_list[-1])
            print("Directory is created and we have moved to that directory")
            speak("Directory is created and we have moved to that directory")
        else:

            print("Permission Denied! Directory not created.")


def list_directories(output_list):
    dirs = os.listdir(os.getcwd())
    for file in range(0, len(dirs)):
        print file, ":", dirs[file]


def create_file(output_list):
    if not os.path.exists(
            os.getcwd() +
            "/" +
            output_list[2] +
            "." +
            output_list[1]):
        if(output_list[1] == "html"):
            os.system("touch " + output_list[2] + ".html")
            print(output_list[2] + ".html is created.")
        elif(output_list[1] == "text"):
            os.system("touch " + output_list[2] + ".text")
            print(output_list[2] + ".txt is created.")
        else:
            print(
                "Do you really want to create this file: %s.%s" %
                (output_list[2], output_list[1]))
            file_listen = ask_again()
            if(file_listen == "y" or file_listen == "yes"):
                os.system("touch " + output_list[2] + "." + output_list[1])
                print(output_list[2] + "." + output_list[1] + " is created.")
                speak(output_list[2] + "." + output_list[1] + " is created.")
            else:

                print("Permission Denied! File not created.")
    else:
        print("File already present.")
if __name__ == "__main__":
    username = os.getenv('USERNAME')
    path = "/home/" + username + "/"
    while(1):
        listen_output = listen()
        print(listen_output)
        if(str(listen_output) != "Could not understand audio"):
            output_list = listen_output.lower().split()
            if((output_list[0] == "mkdir" or output_list[0] == "make")and len(output_list) >= 2):
                make_directory(output_list)
            elif((output_list[0] == "move" or output_list[0] == "go") and output_list[1] == "back"):
                move_back()
            elif((output_list[0] == "cd" and len(output_list) >= 2) or ((output_list[0] == "change" and output_list[1] == "directory") and len(output_list) >= 2)):
                change_directory(output_list)
            elif(output_list[0] == "pwd" or (output_list[0] == "present" and output_list[1] == "working" and output_list[2] == "directory") or output_list[0][0:2] == "pw"):
                print("Present Working Directory: " + os.getcwd())
                speak(os.getcwd())
            elif(output_list[0] == "ls" or (output_list[0] == "list" and output_list[1] == "directories")):
                list_directories(output_list)
            elif(output_list[0] == "file" and len(output_list) >= 3):
                create_file(output_list)
            else:
                print("Sorry! please speak again")
                speak("Sorry! please speak again")
        else:
            speak("Sorry! please speak again")
	
