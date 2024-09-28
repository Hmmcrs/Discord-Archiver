# How to Get Your Discord Token

Follow these steps to retrieve your Discord token:

1. **Open Discord in your web browser** (e.g., Chrome or Firefox).

2. **Open Developer Tools**:  
   Press `Ctrl + Shift + I` (or `Cmd + Option + I` on Mac) to open the Developer Tools panel.

3. **Toggle Device Toolbar**:  
   In the Developer Tools panel, click the small icon that looks like a phone and tablet at the top (or press `Ctrl + Shift + M`) to toggle the device toolbar.

   ![image](https://github.com/user-attachments/assets/8f95d45b-4b58-439f-9101-cbcf9aa0586a)



4. **Navigate to Application Tab**:  
   In the Developer Tools panel, click on the **Application** tab at the top, if you cant see it then you should click the 2 arrows seen in the screenshot below. Then, in the left sidebar, go to **Local Storage** and click on the Discord URL.

   ![image](https://github.com/user-attachments/assets/4a121661-47a0-4889-9a43-b5648e6c3a9b)
   ![image](https://github.com/user-attachments/assets/a1402918-c457-4f68-b45e-6ecac0f390e7)



5. **Filter by Token**:  
   In the Local Storage panel, there’s a filter bar at the top. Type `token` in the filter to find the token entry.

   ![image](https://github.com/user-attachments/assets/f2fdc986-a38c-40e4-b24d-0c3d79a21ada)

6. **Copy Your Token**:  
   You’ll see a field labeled `token`. Right-click on the token string and select **Copy**. Paste this token into the `config.json` file in your project.
   

### Important:
- Do **not** share your token publicly.
- It is recommended to use a secondary account for this script, as using your main account could result in suspension.

