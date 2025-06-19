# **Minecraft WorldEdit Transfer Assistant**

A command-line tool designed to simplify the complex process of moving large or multi-part structures between different Minecraft1 worlds using WorldEdit and Multiverse-Core commands. It intelligently breaks down large selections into smaller, manageable sub-regions, generating a sequential list of commands for smooth transfer.

## **✨ Features**

* **Automated Command Generation:** Generates //copy, //paste, /mvtp (Multiverse-Core teleport), and /tp commands.  
* **Sub-Region Splitting:** Breaks down large source bounding boxes into smaller, user-defined sub-regions to prevent server lag or crashes during large operations.  
* **Multiple Source Regions:** Supports defining multiple distinct source bounding boxes to be moved.  
* **Interactive CLI:** User-friendly command-line interface guides you through input collection.  
* **Input Review & Correction:** Allows you to review all entered parameters before generation and easily go back to modify any field.  
* **Smart Defaults:** Remembers your previous input for re-prompts and provides intelligent defaults (e.g., Creative Mode).  
* **Robust Input Validation:** Ensures valid responses for prompts (e.g., y/n for confirmations, correct coordinate formats).  
* **Negative Coordinate Support:** Fully supports structures located anywhere in the Minecraft world, including negative X and Z coordinates.  
* **Optional Creative Mode:** Includes /gamemode creative commands if you need to ensure you're in creative mode before operations.

## **🚀 Getting Started**

### **Prerequisites**

* **Python 3.x:** Installed on your system.  
* **Minecraft Server:** Running a Spigot/Paper/Fabric server (or similar) with the following plugins:  
  * **WorldEdit:** For selection, copying, and pasting.  
  * **Multiverse-Core:** For teleporting between worlds (/mvtp).  
* **Operator Permissions:** You must have sufficient operator (op) permissions or be in a group with access to all WorldEdit and Multiverse commands.

### **Installation**

1. **Download:** Simply download the main.py file from this repository.  
2. **Place:** Save the file to a convenient location on your computer.

### **Usage**

1. **Open your Terminal/Command Prompt:** Navigate to the directory where you saved main.py.  
2. **Run the script:**  
   Bash  
   python main.py

3. **Follow the Prompts:**  
   * The script will ask for your **Source World Name**, **Target World Name**, **Creative Mode** preference, **Source Bounding Boxes**, **Target Paste Origin**, and **Sub-Region Size**.  
   * **Default Values:** For prompts showing \[DefaultValue\], you can just hit Enter to accept the default or type a new value.  
   * **Bounding Boxes:** Enter each bounding box (X1,Y1,Z1,X2,Y2,Z2) on a new line. Type DONE when you've entered all boxes. If re-prompting, you can type KEEP to retain the previously entered list.  
   * **Coordinates:** Enter coordinates as comma-separated values (e.g., 100,64,-200).  
4. **Review Inputs:** After entering all information, the script will display a summary for your review.  
5. **Confirm or Correct:**  
   * Type y or yes and press Enter to confirm and generate the commands.  
   * Type n or no and press Enter to go back and correct any of the inputs.  
   * If you type an invalid response or just hit Enter on the confirmation, it will re-prompt you.  
6. **Execute Commands:**  
   * Once generated, the script will print a long list of WorldEdit and Multiverse commands to your console.  
   * **Crucially:** Copy these commands in the exact order they are generated.  
   * Paste and execute them **one block at a time** (e.g., copy the commands for "SUB-REGION 1", paste into Minecraft chat, wait for it to complete, then move to "SUB-REGION 2", etc.). This sequential execution is vital for large structures to prevent server overload.

## **💡 Example Workflow (Simplified)**

\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\#          Minecraft WorldEdit Transfer Assistant          \#  
\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\# ... (Welcome Header) ...  
Source World Name: MyOldCity  
Target World Name: MyNewServer  
Creative Mode needed? (Y/n) \[Y\]:  
Enter Source Bounding Box \#1 (or 'DONE' or 'KEEP'): \-100,60,-100,100,150,100  
Enter Source Bounding Box \#2 (or 'DONE' or 'KEEP'): DONE  
Target Paste Origin (X,Y,Z) \[0,0,0\]: 500,65,500  
Sub-Region Size \[64\]: 32

\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\#                   REVIEW YOUR INPUTS                     \#  
\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\# ... (Summary of inputs) ...  
Proceed with command generation? (y/n): n  \# User decides to correct  
\# ... (Restarting Input Process Header) ...  
Source World Name \[MyOldCity\]:  
Target World Name \[MyNewServer\]: ProdServer  
Creative Mode needed? (Y/n) \[Y\]: n \# User changes mind  
Current Source Bounding Boxes:  
  1: (-100, 60, \-100) to (100, 150, 100\)  
Enter NEW Source Bounding Box \#1 (X1,Y1,Z1,X2,Y2,Z2, 'DONE', or 'KEEP' to retain current list): KEEP  
Target Paste Origin (X,Y,Z) \[500,65,500\]:  
Sub-Region Size \[32\]:

\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\#                   REVIEW YOUR INPUTS                     \#  
\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\# ... (Updated summary, now with 'ProdServer', No Creative, etc.) ...  
Proceed with command generation? (y/n): y \# User confirms

\------------------------------------------------------------  
Generating your WorldEdit commands...  
\------------------------------------------------------------

\# \--- SUB-REGION 1 of X (Source: \-100,60,-100 to \-69,150,-69 \-\> Target: 500,65,500) \---  
/mvtp MyOldCity  
/tp \-100 60 \-100  
//sel box \-100,60,-100 \-69,150,-69  
//copy  
/mvtp ProdServer  
/tp 500 65 500  
//paste

\# \--- SUB-REGION 2 of X (Source: \-100,60,-68 to \-69,150,-37 \-\> Target: 500,65,532) \---  
\# ... (Many more commands) ...

\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#  
\# ... (Command Generation Complete Header) ...

## **⚠️ Important Notes**

* **BACKUP YOUR WORLDS\!** Before performing any large WorldEdit operations, always create a full backup of both your source and target Minecraft worlds.  
* **Server Performance:** Copying and pasting large regions, even in chunks, can be resource-intensive and may cause temporary server lag or freezes. It's recommended to perform these operations during off-peak hours or on a dedicated test server.  
* **Player Permissions & Position:** The generated commands rely on you having operator permissions. The /tp commands are essential as WorldEdit's //copy and //paste operations are relative to your current player position.  
* **WorldEdit & Multiverse:** Ensure both plugins are installed and functioning correctly on your Minecraft server.

## **🤝 Contributing**

Feel free to open issues or submit pull requests if you have suggestions for improvements, bug fixes, or new features\!

## **📄 License**

This project is licensed under the MIT License \- see the LICENSE file (if applicable) for details.

---

**Sources**  
1\. [https://github.com/iDarkshotOP/simple-todo-list](https://github.com/iDarkshotOP/simple-todo-list)