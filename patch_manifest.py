p='android/app/src/main/AndroidManifest.xml'
s=open(p,encoding='utf-8').read()
if 'leanback' not in s:
    feats=('    <uses-feature android:name="android.hardware.touchscreen" android:required="false" />\n'
           '    <uses-feature android:name="android.software.leanback" android:required="false" />\n')
    s=s.replace('<application',feats+'    <application',1)
    s=s.replace('<category android:name="android.intent.category.LAUNCHER" />',
                '<category android:name="android.intent.category.LAUNCHER" />\n                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />',1)
    s=s.replace('<application','<application android:banner="@drawable/tv_banner"',1)
    open(p,'w',encoding='utf-8').write(s)
print('OK manifest TV')
