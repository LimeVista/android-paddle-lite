import hashlib
import io
import os
import shutil
import tarfile

import requests

# 定义全局变量
OriginVersion: str = '2.12'
Version: str = f'{OriginVersion}.1'
VersionCode: str = '21200'
Name: str = 'inference_lite_lib.android.armv8.clang.c++_static.with_extra.with_cv'
FileName: str = f'{Name}.tar.gz'
SrcStaticLibFileName: str = 'libpaddle_api_light_bundled.a'
DstStaticLibFileName: str = 'libpaddle.a'
BuildFolder: str = './build'
OutputFolder: str = f'{BuildFolder}/prepare/paddle-lite-{Version}'
TargetFolder: str = f'{BuildFolder}/target/paddle-lite-{Version}'
DownloadUrl: str = f'https://github.com/PaddlePaddle/Paddle-Lite/releases/download/v{OriginVersion}/{FileName}'


def prepare():
    print('正在清理缓存...')

    # 清理缓存
    if os.path.exists(BuildFolder):
        shutil.rmtree(BuildFolder)
    os.makedirs(BuildFolder)
    os.makedirs(TargetFolder)

    print('正在下载库文件...')

    # 下载库文件
    r = requests.get(DownloadUrl)

    print('正在解压目录...')

    # 解压目录
    file_object = io.BytesIO(r.content)
    tar = tarfile.open(fileobj=file_object)
    tar.extractall(BuildFolder)

    print('正在复制资源...')

    # 复制资源
    shutil.copytree('./prefab/paddle-VERSION', OutputFolder)
    shutil.copytree(f'{BuildFolder}/{Name}/cxx/include', f'{OutputFolder}/prefab/modules/paddle/include')
    shutil.copy(
        f'{BuildFolder}/{Name}/cxx/lib/{SrcStaticLibFileName}',
        f'{OutputFolder}/prefab/modules/paddle/libs/android.arm64-v8a/{DstStaticLibFileName}'
    )

    print('正在替换资源...')

    # 替换资源
    replace_content(f'{OutputFolder}/prefab/prefab.json', 'VERSION', Version)
    replace_content(f'{OutputFolder}/AndroidManifest.xml', 'VER_NAME', Version)
    replace_content(f'{OutputFolder}/AndroidManifest.xml', 'VER_CODE', VersionCode)


def build():
    print('开始构建...')
    zip_file = f'{TargetFolder}/paddle-{Version}'
    aar_file = f'{TargetFolder}/paddle-{Version}.aar'
    pom_file = f'{TargetFolder}/paddle-{Version}.pom'

    shutil.make_archive(zip_file, 'zip', OutputFolder)
    shutil.move(f'{zip_file}.zip', aar_file)

    shutil.copy('./prefab/paddle-VERSION.pom', pom_file)
    replace_content(pom_file, 'VER_NAME', VersionCode)

    create_hash_file(aar_file)
    create_hash_file(pom_file)
    print('完成构建')


def replace_content(file_name: str, old: str, new: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace(old, new)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(text)


def create_hash_file(file_name: str):
    data = open(file_name, 'rb').read()
    with open(f'{file_name}.md5', 'w') as f:
        f.write(hashlib.md5(data).hexdigest())
    with open(f'{file_name}.sha1', 'w') as f:
        f.write(hashlib.sha1(data).hexdigest())


if __name__ == '__main__':
    prepare()
    build()
