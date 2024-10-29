#!/usr/bin/python3

import traceback, uuid, os
from flask import Flask, request, send_from_directory
from pywpsrpc.rpcwpsapi import (createWpsRpcInstance, wpsapi)
from pywpsrpc.common import (S_OK, QtApp)


app = Flask(__name__)
# 设置文件上传保存路径
app.config['UPLOAD_FOLDER'] = '/tmp'
# MAX_CONTENT_LENGTH设置上传文件的大小，单位字节
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024


formats = {
    "doc": wpsapi.wdFormatDocument,
    "docx": wpsapi.wdFormatXMLDocument,
    "rtf": wpsapi.wdFormatRTF,
    "html": wpsapi.wdFormatHTML,
    "pdf": wpsapi.wdFormatPDF,
    "xml": wpsapi.wdFormatXML,
}


class ConvertException(Exception):

    def __init__(self, text, hr):
        self.text = text
        self.hr = hr

    def __str__(self):
        return """Convert failed:
Details: {}
ErrCode: {}
""".format(self.text, hex(self.hr & 0xFFFFFFFF))


def convert_to(path, format, abort_on_fails=False):
    hr, rpc = createWpsRpcInstance()
    if hr != S_OK:
        raise ConvertException("Can't create the rpc instance", hr)

    hr, app = rpc.getWpsApplication()
    if hr != S_OK:
        raise ConvertException("Can't get the application", hr)

    try:
        # we don't need the gui
        app.Visible = False

        docs = app.Documents

        def _handle_result(hr):
            if abort_on_fails and hr != S_OK:
                raise ConvertException("convert_file failed", hr)

        hr = convert_file(path, docs, format)
        _handle_result(hr)
    except Exception as e:
        print(traceback.format_exc())

    app.Quit(wpsapi.wdDoNotSaveChanges)
    # 解决转换完成后wps进程卡住问题
    os.system('pkill -f "office"')


def convert_file(file, docs, format):
    hr, doc = docs.Open(file, ReadOnly=True)
    if hr != S_OK:
        return hr

    out_dir = os.path.dirname(os.path.realpath(file)) + "/out"
    os.makedirs(out_dir, exist_ok=True)

    # you have to handle if the new_file already exists
    new_file = out_dir + "/" + os.path.splitext(os.path.basename(file))[0] + "." + format
    ret = doc.SaveAs2(new_file, FileFormat=formats[format])

    # always close the doc
    doc.Close(wpsapi.wdDoNotSaveChanges)

    return ret


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


@app.route("/convert", methods=["POST"])
def do_convert():
    input_file_path = None
    out_file_path = None

    try:
        # 转换格式参数
        convert_format = request.form['format']

        # 获取文件参数
        file = request.files['file']
        # 文件后缀
        file_ext = file.filename.rsplit('.')[-1]
        file_name_uuid = str(uuid.uuid4())
        # UUID文件名
        file_name = file_name_uuid + "." + file_ext
        input_file_path = app.config['UPLOAD_FOLDER'] + '/' + file_name
        print('输入文档路径[%s]' % input_file_path)
        # 保存文件
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

        # 文件转换
        print("开始转换文档[%s]" % file_name)
        convert_to(os.path.join(app.config['UPLOAD_FOLDER'], file_name), convert_format, True)
        print("文档转换完成[%s]" % file_name)

        # 返回转换后的文件
        convert_file_name = file_name_uuid + "." + convert_format
        out_file_path = app.config['UPLOAD_FOLDER'] + '/out/' + convert_file_name
        print('输出文档路径[%s]' % out_file_path)
        return send_from_directory(app.config['UPLOAD_FOLDER'] + '/out', convert_file_name, as_attachment=True)

    except Exception as e:
        print('文档转换时发生错误')
        print(traceback.format_exc())
        return {"success": False}

    finally:
        print('删除临时文件')
        if input_file_path is not None:
            remove_file(input_file_path)
        if out_file_path is not None:
            remove_file(out_file_path)


if __name__ == "__main__":
    # 单线程
    app.run(host="0.0.0.0", port=9000)
