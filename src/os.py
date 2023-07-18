import platform

def get_os():   
    system = platform.system()
    
    if system == "Windows":
        if platform.win32_ver()[0] != str(10 or 11):
            return f"Windows {platform.win32_ver()[0]} {platform.win32_edition()} {platform.win32_ver()[1]}", False
        
        if int(platform.win32_ver()[1].split(".")[-1]) >= 22000:
            return f"Windows 11 {platform.win32_edition()} {platform.win32_ver()[1]}", True
        else:
            return f"Windows 10 {platform.win32_edition()} {platform.win32_ver()[1]}", True
        

    else:
        return "Non-Windows operating system", False
