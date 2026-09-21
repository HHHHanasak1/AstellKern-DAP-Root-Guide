# AstellKern-DAP-Root-Guide

**[The APK Whitelist Removal solution has been released. Click here to check it out!](https://github.com/PPPPatrick0/Disable-AstellKern-UI4-App-Whitelist)**  
**[APK白名单解除方案现已发布，点击查看](https://github.com/PPPPatrick0/Disable-AstellKern-UI4-App-Whitelist)**

**Rooting the Astell&Kern DAP with Apatch**  
**通过Apatch来获取艾利和数字播放器的Root权限**
<img width="1080" height="1920" alt="Screenshot-trinket 1234567 -20250804145857" src="https://github.com/user-attachments/assets/98c6a9e1-ac68-4b4c-ad84-e974af0d0f84" />

## [Chinese Version](https://github.com/PPPPatrick0/AstellKern-DAP-Root-Guide?tab=readme-ov-file#%E4%B8%AD%E6%96%87%E7%89%88chinese-version)
## [English Version](https://github.com/PPPPatrick0/AstellKern-DAP-Root-Guide?tab=readme-ov-file#english-version-1)

## 中文版（Chinese Version）

### 简短说明

* 本指南旨在尝试为艾利和 (Astell&Kern) 播放器提供一套Root方案。本方案最初基于 SP3000 （无印版）、系统版本 v1.51 创建。

* 现在，艾利和的机器（UI4以及UI4.5），如 SP3000系列（SP3000,SP3000T,SP3000M得到验证），SE300 ，SR35（得到验证），PD10（得到验证） ...（UI4），SP4000（UI4.5）（理论可以，暂未得到验证）等机型，可参照本指南进行Root。

* 从V0.2开始，将开始提供部分机型的已解密update.zip，以方便您的操作以及后续可能的救砖（希望你永远都不会因此用上）。  
(V0.2增加了SP3000 V1.51)  
(V0.3增加了SP3000T V1.21 ，SP3000M V1.21)

### 重要提示

***风险警告:***
* Root过程可能将伴随着失去保修、数据丢失甚至设备永久损坏（变砖）的风险。请您在充分理解所有步骤和潜在风险后再进行操作。所有操作均由您本人负责。

**APK包名确认:**
* 由于AK操作系统采用白名单制度来限制APK文件的安装，本指南中的所有APK文件均通过了修改Package Name的方式来绕过AK的限制。  
因此，每一个修改后的APK文件格式均为xxx(package_name).apk的格式上传，以方便你自行查找是否存在包名冲突的Application。  
（仅限UI4的机型）

### 操作流程概览
**本指南将引导您完成以下三个核心步骤：**
* 准备工作1: 在设备上启用USB调试权限。  
* 准备工作2：获取适用于设备的解密后的系统镜像文件。  
* 获取Root: 刷写Apatch patch后的镜像，并安装APatch管理器。

### 1 准备工作
在设备上启用USB调试权限。  
由于AK的设备没有在常规设置中提供开启ADB调试的入口，我们需要通过一个自制的APK来调用其隐藏的工厂调试菜单。
#### 1) 开启ADB调试
在Release(Tag:Files)的中，下载全部文件。
将此 EnableAKTestMode(com.now.moov).apk 传输到您的设备内部存储中，并进行安装。  
安装完成后，进入该应用，点击“打开DebugSettings”，并点击第一个按钮，确保第一个按钮显示为“ADB ENABLED”。

#### 2) 验证连接
现在，使用USB数据线将您的设备连接到主机。  
在主机的终端里，输入以下命令：
```
adb devices
```
如果您看到输出了您设备的序列号，并且状态为 device，则表示ADB连接已成功建立。

#### 3) （可选，但强烈推荐）永久开启ADB调试
默认情况下，每次重启设备后，ADB调试选项都会自动关闭。  
为了方便后续操作及日后使用，您可以将其设置为永久开启。  
在主机的终端里，输入以下命令：
```
adb shell am start --user 0 -n com.iriver.tester.factorytool/.UserDebugActivity
```
设备的屏幕上会再次出现一个工厂调试界面。  
点击此界面上的第一个选项（与ADB相关的选项）。  
（注：在PD10上可能不是第一个）  
完成此操作后，ADB调试模式将会被永久激活，即使设备重启也不会关闭。

### 2 获取镜像文件
#### 1) 获得解密后的update.zip
请下载自己机型的OTA文件，名称一般为  `版本号.hex` ，下载后放入机器的根目录。  
在机器上点击确认升级。  
在升级的同时在电脑端不断刷新机器的内部存储目录。  
一般在升级进度50%之后在根目录下能够看见update.zip。  
迅速将update.zip拷贝至主机。

> **更新：** 现在不必再和进度条赛跑了。`.hex` 可以直接在电脑上离线解密：`python tools/akhex.py decrypt 1.42.hex 1.42.zip --project sp3000`（`--project` 为机型的 `ro.boot.project_name`，原理和一点点吐槽见[附录](#附录--appendix)）。

#### 2) 解密文件
请将update.zip内的 payload.bin 解密。
（推荐使用 payload-dumper  
也可以使用Release里添付的payload-dumper.exe  
将payload.bin拖拽至exe即可解包）  

  
至此获得解密后的镜像文件。

### 3 通过APatch获取Root权限
由于目标设备上修改包名后的APatch管理器存在文件写入问题，我们需要借助一台普通的安卓设备来完成启动镜像的修补工作。
#### 1) 在“辅助设备”上制作APatch镜像
您需要一台普通的、无特殊限制的安卓设备（手机或平板均可）作为“辅助设备”。  
* 在下载的 Apatch.zip中，解压后得到 APatch_10763_original.apk。  
同时，找到你设备的官方原版 boot.img。  
* 安装并传输文件：  
在您的“辅助设备”上，安装 APatch_10763_original.apk。  
将官方原版的 boot.img 文件也一同拷贝到这台辅助设备的内部存储中（例如，“Download”文件夹）。  
* 使用APatch进行修补：  
在辅助设备上，打开APatch应用。  
点击主界面右上角的从左往右第一个图标（手机+向下的箭头）。  
选择 “Select a boot image to Patch” 选项。  
在文件选择器中，找到并选择您刚刚拷贝的那个boot.img文件。  
应用会提示您设置一个 SuperKey。这是一个用于在管理器中激活Root权限的“密码”，请务必设置一个并牢牢记住它。  
输入完SuperKey后，点击“开始”（Start Patching）。APatch将会开始修补boot.img。  
* 获取最终镜像：  
修补成功后，在辅助设备的“下载”文件夹中，会生成一个名为 apatch_patched_....img 的新文件。这就是我们最终需要的启动镜像。  
将这个修补完成的镜像，从辅助设备传回您的主机。

#### 2) 为设备刷入镜像并重启

* 在主机的终端里，输入以下命令让设备重启到fastboot模式：  
```
adb reboot bootloader
```
* 刷写vbmeta镜像以禁用AVB  
我们需要刷写vbmeta和vbmeta_system两个镜像，以彻底关闭安卓验证启动（AVB, Android Verified Boot）。  
执行刷写：  
在fastboot模式下，执行以下两条命令：  
```
# 关闭主验证链
fastboot --disable-verity flash vbmeta vbmeta.img

# 关闭针对system分区的验证链
fastboot --disable-verity flash vbmeta_system vbmeta_system.img
```
* 刷写最终镜像  
在主机的终端里，导航到包含最终APatch镜像的目录，执行刷写命令：  
```
# 将 "Your/File/Path" 替换为您实际的文件路径和名称
fastboot flash boot "Your/File/Path/apatch_patched_....img"

# 镜像刷写完成后，执行以下命令重启您的设备：
fastboot reboot
```

#### 3) 激活Root
等待设备进入操作系统。  
* 安装修改版APatch管理器：  
在 Apatch.zip 中，找到 APatch_10763_Modded(com.appgeneration.itunerfree).apk。  
将这个修改了包名的版本，安装到您的设备上。  
* 获取Root权限：  
在设备上打开刚刚安装的APatch管理器。  
在应用主界面的输入框中，输入您之前设定好的那个SuperKey。  
点击确认。如果一切顺利，应用将显示Root已激活。您可以通过 adb shell 并执行 su 命令来验证是否已获得#权限。


**至此，您的Astell&Kern DAP已成功获取Root权限。**  
  
请发挥你的想象力，没有什么是在拥有Root后做不到的！  
<del>
关于解除Iriver操作系统的APP白名单限制，敬请期待！[@7dollars](https://github.com/7dollars)  
</del>
  
**Enjoy It!**




## English Version

<del>
Oops: 404: English Translation Not Found  
My translator is currently compiling (or maybe I'm just procrastinating). An English version of this epic saga is on its way. In the meantime, I hope the code snippets and command lines speak for themselves. 
</del>

### Brief Introduction
* This guide aims to provide a comprehensive rooting solution for Astell&Kern DAPs. The method was originally developed and tested on an SP3000 (standard version) running firmware v1.51.

* Currently, this guide can be referenced for rooting Astell&Kern devices running UI4 and UI4.5, such as the SP3000series (SP3000 , SP3000T , SP3000M verified) and PD10 (verified) , SR35 (verified) and potentially the SE300 etc...(UI4), SP4000 (UI4.5) (theoretically possible, but not yet verified).

* Starting with v0.2, pre-decrypted update.zip files for select models will be provided. This is to simplify the process and to serve as a potential rescue package for "unbricking" your device (hopefully, you'll never need it for that reason).  
(V0.2 Add SP3000 V1.51)  
(V0.3 Add SP3000T V1.21 , SP3000M V1.21)

### Important Notes

***Risk Disclaimer***
* The rooting process may carry risks, including but not limited to voiding the warranty, data loss, or even permanently damaging ("bricking") your device. Please proceed only after you have fully understood all steps and potential risks. You are solely responsible for all your actions.

**APK Package Name Confirmation**
* Due to the Astell&Kern OS employing a whitelist system to restrict APK installations, all APK files provided in this guide have had their Package Names modified to bypass this limitation.
* Consequently, each modified APK is named in the format of xxx(package_name).apk. This is to help you check for any potential package name conflicts with applications already on your device.  
(This applies to UI4-based models).

### Process Overview
** This guide will walk you through three core stages: **
* Preparation 1: Enable USB Debugging on your device.
* Preparation 2: Obtain the decrypted system image files for your device.
* Achieving Root: Flash the APatch-patched boot image and install the APatch Manager.

### 1. Preparation: Enabling ADB
Since AK devices do not provide an option to enable ADB Debugging in the standard settings, we need to use a custom-made APK to invoke a hidden factory debug menu.
#### 1) Enable ADB Debugging
From the Releases (Tag:Files) section, download all.  
Transfer EnableAKTestMode(com.now.moov).apk to your device's internal storage and install it.  
Once installed, open the application. Tap on "打开DebugSettings", then tap the first button and ensure its text changes to "ADB ENABLED".

#### 2) Verify the Connection
Now, connect your device to your host machine using a USB cable.  
In your host's terminal, enter the following command:
```
adb devices
```
If you see your device's serial number listed with the status device, the ADB connection is successfully established.

#### 3) (Optional but Highly Recommended) Permanently Enable ADB
By default, the ADB Debugging option disables itself after every reboot. To make it persistent for future use:  
On your host's terminal, enter the following command:
```
adb shell am start --user 0 -n com.iriver.tester.factorytool/.UserDebugActivity
```
Another factory menu will appear on the device's screen.  
Tap the first option on this screen (the one related to ADB).  
(Note: On the PD10, it may not be the first option.)  
This will permanently activate ADB Debugging mode, and it will persist through reboots.  

### 2. Obtaining the Image Files
#### 1) Get the Decrypted update.zip
Download the official OTA file for your device model, usually named VERSION_NUMBER.hex.  
Place the downloaded .hex file in the root directory of your device's internal storage.  
On the device, confirm the update when prompted.  
While the update is in progress, continuously refresh the device's internal storage directory from your computer.  
Typically, after the update progress reaches about 50%, you will see an update.zip file appear in the root directory.  
Quickly copy this update.zip file to your host machine.

> **Update:** you no longer have to race the progress bar. A `.hex` can be decrypted offline on your PC: `python tools/akhex.py decrypt 1.42.hex 1.42.zip --project sp3000` (`--project` is your model's `ro.boot.project_name`; how it works, plus some light commentary, in the [Appendix](#附录--appendix)).

#### 2) Decrypt the Files
Extract the payload.bin file from the update.zip.  
You need to unpack this payload.bin. (Using payload-dumper is recommended).  
Alternatively, you can use the payload-dumper.exe provided in the Releases section of this repository. Simply drag and drop the payload.bin file onto the .exe to unpack it.  
  
You have now obtained the decrypted system image files.

### 3. Achieving Root with APatch
Due to a file-writing issue with the package-modified APatch manager on the target device, we need a standard Android device to help with the patching process.
#### 1) Create the APatched Image on a "Helper" Device  
You will need a standard, unrestricted Android device (a phone or tablet) to act as a "helper device".  
* From the downloaded Apatch.zip, get the APatch_10763_original.apk.  
Also, locate the stock, official boot.img for your target device.  
* Install and Transfer:  
Install APatch_10763_original.apk on your "helper device".  
Copy the stock boot.img file to the helper device's internal storage (e.g., the "Download" folder).  
* Patch with APatch:  
Open the APatch app on the helper device.  
Set SuperKey and select the boot.img you just copied.  
Tap "Start Patching."  
* Retrieve the Final Image:  
Upon success, a new file named apatch_patched_....img will be generated in the "Download" folder of your helper device. This is our final boot image.  
Transfer this patched image from the helper device back to your host machine.

#### 2) Flash Images and Reboot
* On your host's terminal, reboot your target device into fastboot mode:
```
adb reboot bootloader
```
* Flash vbmeta Images to Disable AVB:  
We need to flash both vbmeta and vbmeta_system to completely disable Android Verified Boot (AVB).  
Execute Flashing:  
While in fastboot mode, execute the following two commands:
```
# Disable the main verification chain
fastboot --disable-verity flash vbmeta vbmeta.img

# Disable the verification chain for the system partition
fastboot --disable-verity flash vbmeta_system vbmeta_system.img
```
* Flash the Final Boot Image:  
Navigate to the directory containing the final APatch image and execute the flash command:
```
# Replace "Your/File/Path" with the actual path and filename
fastboot flash boot "Your/File/Path/apatch_patched_....img"

# After flashing is complete, reboot your device:
fastboot reboot
```

#### 3) Activate Root
Wait for the device to boot into the OS.
* Install the Modified APatch Manager:  
From the Apatch.zip, find APatch_10763_Modded(com.appgeneration.itunerfree).apk.  
Install this package-modified version onto your target device.  
* Gain Root Access:  
Open the newly installed APatch manager on your device.  
In the input field on the main screen, enter the SuperKey you set previously.  
Tap confirm. If everything went smoothly, the app should indicate that root is active. You can verify this by running adb shell and executing the su command to see if you get the # prompt.

**At this point, your Astell&Kern DAP has been successfully rooted.**
  
Let your imagination run wild; there's nothing you can't do with root access!  
<del>
Stay tuned for a guide on how to disable the iRiver OS app whitelist! [@7dollars](https://github.com/7dollars)  
</del>
  
**Enjoy It!**


## 附录 / Appendix

### 中文：`.hex` 是怎么“加密”的（以及为什么这道防线没有用）

官方 OTA 的 `.hex` 本质上是一个普通的 A/B OTA zip，只是前面绝大部分内容被套了一层 AES。机器上负责解密的是 `TaskService.apk` 里的 `libjniDecHex.so`，细节如下（均已用真机产出的 `update.zip` 逐字节验证，SP3000 的 1.36 与 1.42 完全一致）：

| 项目 | 内容 |
| --- | --- |
| 算法 | AES-128，**ECB** 模式 |
| 分块 | 每 **16 KiB** 一块，块内按 16 字节独立处理 |
| 尾部 | 最后不足 16 KiB 的部分（`文件大小 % 16384` 字节）**原样保留，不加密** |
| 密钥 | `("%sKOR" % ro.boot.project_name.upper()).ljust(16, "_")`，例如 SP3000 为 `SP3000KOR_______` |
| 一个怪癖 | 所谓“解密”分支调用的是 AES **加密**函数；制作 `.hex` 时用的则是 AES **解密**。所以直接用标准 AES 解密只会得到垃圾 |

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def unhex(src, dst, project="sp3000"):
    key = ("%sKOR" % project.upper()).ljust(16, "_").encode()
    aes = Cipher(algorithms.AES(key), modes.ECB()).encryptor()   # 是的，encryptor。
    size = __import__("os").path.getsize(src); done = 0
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        while buf := fi.read(0x4000):
            fo.write(aes.update(buf) if done + len(buf) < size else buf)
            done += len(buf)
```

完整脚本见 [`tools/akhex.py`](tools/akhex.py)。它只用来**读取**你自己机型的固件包，不能伪造签名，也不能让机器接受被改过的固件。

**关于这道防线，几点观察：**

* 是 **ECB**。就是维基百科用来演示“为什么不要用它”的那个模式，配图是一只企鹅。
* “密钥”是**机型名 + `KOR` + 下划线**。它更像一张标签而不是密钥：机器解密时还会很体贴地把它打印到 logcat 里（`enc_key = SP3000KOR_______, aes_key = SP3000KOR_______`）。
* “解密”函数调用的是加密，“加密”工具调用的是解密。对称加密，被对称地写反了，负负得正，居然还能用。
* 文件末尾，连同 OTA 签名块，被体贴地留成了**明文**，以防有人担心可读性。
* 解完之后，机器把完整的 `update.zip` **明文**放进 `/sdcard` 根目录，任何有存储权限的应用都能读走。
* 系统还允许降级，所以你可以让它帮你解密**任何**版本。
* 1.35 的构建指纹末尾写着 `test-keys`。

一道工事修得很认真，最后所有人从它的侧面走了过去。这就是**马奇诺防线**：精心构筑，正对着错误的方向。

（这不是漏洞报告。固件包本来就是要装进你自己的机器的，这层“加密”从来没有保护过任何东西，只是把大家变成了要和进度条赛跑的人。）

### English: how the `.hex` "encryption" works (and why it protects nothing)

An official OTA `.hex` is an ordinary A/B OTA zip with most of its bytes run through AES. The decryptor lives in `libjniDecHex.so` inside `TaskService.apk`. Everything below was verified byte-for-byte against the `update.zip` the device itself produces (SP3000 1.36 and 1.42).

| Item | Value |
| --- | --- |
| Cipher | AES-128 in **ECB** mode |
| Chunking | **16 KiB** chunks, processed as independent 16-byte blocks |
| Tail | the last partial chunk (`filesize % 16384` bytes) is copied **unchanged** |
| Key | `("%sKOR" % ro.boot.project_name.upper()).ljust(16, "_")`, e.g. `SP3000KOR_______` |
| The quirk | the "decrypt" branch calls AES **encrypt**, and the packages are produced with AES **decrypt**, so a stock AES decrypt yields garbage |

See [`tools/akhex.py`](tools/akhex.py) for a complete script. It only *reads* firmware packages for your own device; it cannot forge signatures.

**Observations on the fortification:**

* It is **ECB**, the mode Wikipedia illustrates with a penguin, as a warning.
* The "key" is the **model name plus `KOR` plus underscores**. Less a key than a label, and the device helpfully prints it to logcat while decrypting.
* The decrypt function calls encrypt and the encrypt tool calls decrypt. Symmetric cryptography, symmetrically backwards, and it still works.
* The end of the file, including the OTA signature block, is left in **plaintext**, in case anyone worried about readability.
* Afterwards the device drops the fully decrypted `update.zip` in **plaintext** into `/sdcard` for any app with storage access to read.
* The OS also accepts downgrades, so you can have it decrypt *any* version for you.
* The build fingerprint of 1.35 ends in `test-keys`.

A carefully engineered wall that everyone simply walks around: the **Maginot Line**.

(This is not a vulnerability report. A firmware package is meant to be installed on your own device; this layer never protected anything, it just turned everyone into people racing a progress bar.)

## Shout-Outs!
This success wouldn't have been possible without these legends:  
* The APatch Team: Your kernel-patching approach was the skeleton key that bypassed this device's final defenses. Absolute genius!  
* The AKBox dev [@7dollars](https://github.com/7dollars) and community: Thanks for all the encouragement and support. You were the motivation that kept me going!
* [@rlw6534](https://github.com/rlw6534):	verified for SR35
* Google Gemini: My AI partner, who provided tireless technical support and brainstorming sessions. AI-assisted reverse engineering is incredibly cool.  
