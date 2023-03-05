# Paddle Lite Builder For Android
用于将预构建 `Paddle Lite` 版本整合

## 使用要求
* Android SDK API >= 31
* NDK Ver >= 21
* Android Studio 4.1+

## 使用方式
* 添加源
```groovy
allprojects {
  repositories {
    // ...
    maven { url "https://raw.githubusercontent.com/LimeVista/android-paddle-lite/master/prebuilt" }
  }
}
```
* 引入
```groovy
dependencies {
    implementation 'me.limeice.paddle:lite:2.12.1'
}
```
* 启用 `prefab`
```groovy
android {
    buildFeatures {
        prefab true
    }
}
```
* 引入 `CMakeLists.txt`
```cmake
find_package (paddle REQUIRED CONFIG)

target_link_libraries(yourLib paddle::paddle android ${log-lib})
```

## 构建
* 需要 Python3
* 执行 `.\main.py`

## 版本记录
### 2.12.1
* 2023-03-05
* Paddle lite version: 2.12
