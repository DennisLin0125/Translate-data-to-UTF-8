import os
import re
import chardet
import json

# 取得當前目錄
current_directory = os.getcwd()

# JSON 檔案名
json_file_name = "config.json"  # 這裡請根據實際情況替換成你的 JSON 檔案名稱
configLanguageList = []
configFileList = []
# 檢查 JSON 檔案是否存在
json_file_path = os.path.join(current_directory, json_file_name)
if os.path.exists(json_file_path):
    # 打開 JSON 檔案並讀取資料
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        jsondata = json.load(json_file)
        configLanguageList = jsondata["config"]["language"]
        configFileList = jsondata["config"]["file_list"]
else:
    print(f"JSON 檔案 '{json_file_name}' 不存在")

print("03:翻譯語言:", configLanguageList)
print("03:origin data:", configFileList)

for lv_data in configFileList:
    index = 0
    for lang in configLanguageList:
        temp = lv_data.split(".")
        orgPath = current_directory + "\\org"
        langPath = current_directory + "\\" + lang

        # 指定要讀取的原始檔案名稱
        input_filename = lv_data
        input_file_path = os.path.join(orgPath, input_filename)

        # 指定要保存的新檔案名稱
        output_filename = f"{temp[0]}_utf8_{lang}.{temp[1]}"
        output_file_path = os.path.join(langPath, output_filename)

        tempPath1 = output_file_path

        # 確認原始檔案是否存在
        if os.path.exists(input_file_path):
            print(f"04:正在讀取檔案: {input_filename}")

            # 以二進制模式讀取原始檔案
            with open(input_file_path, "rb") as file:
                raw_data = file.read()

            # 使用 chardet 檢測編碼
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
            print(f"05:檢測到的編碼:  {encoding} ")

            # 將內容以檢測到的編碼解碼，然後寫入新的 UTF-8 檔案
            try:
                content = raw_data.decode(encoding)
                with open(output_file_path, "w", encoding="UTF-8") as file:
                    file.write(content)
                print(f"06:已將內容保存至 {output_filename}，使用 UTF-8 編碼。")
            except UnicodeDecodeError:
                print(f"07:無法使用檢測到的編碼 {encoding} 解碼檔案 {input_filename}。")
        else:
            print(f"08:檔案 {input_filename} 不存在於當前目錄中。")

        # =================================================================================
        print("=" * 30)
        # 指定要讀取的原始檔案名稱
        trans_filename = f"{temp[0]}_trans_{lang}.txt"
        trans_file_path = os.path.join(langPath, trans_filename)

        # 指定要保存的新檔案名稱
        trans_output_filename = f"{temp[0]}_tran_{lang}.csv"
        trans_output_file_path = os.path.join(langPath, trans_output_filename)

        tempPath2 = trans_output_file_path

        # 確認原始檔案是否存在
        if os.path.exists(trans_file_path):
            print(f"正在讀取檔案: {trans_filename}")

            # 以二進制模式讀取原始檔案
            with open(trans_file_path, "rb") as file:
                raw_data = file.read()

            # 使用 chardet 檢測編碼
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
            print(f"檢測到的編碼:  {encoding} ")

            # 將內容以檢測到的編碼解碼，然後寫入新的 UTF-8 檔案
            try:
                content = raw_data.decode(encoding)
                with open(trans_output_file_path, "w", encoding="UTF-8") as file:
                    file.write(content)
                print(f"已將內容保存至 {trans_output_filename}，使用 UTF-8 編碼。")
            except UnicodeDecodeError:
                print(f"無法使用檢測到的編碼 {encoding} 解碼檔案 {trans_filename}。")
        else:
            print(f"檔案 {trans_filename} 不存在於當前目錄中。")
        # ==================================================================================

        print("=" * 30)
        dic = {}

        # 確認檔案是否存在
        if os.path.exists(trans_output_file_path):
            print(f"10:正在讀取檔案: {trans_output_filename}")

            # 讀取檔案內容
            with open(trans_output_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                content1 = content.split("\n")
                content1.pop()

                for res in content1:
                    item = res.split("\t")
                    if len(item) != 1:
                        if item[0] != "ID" and item[2] != '':
                            # print(item)
                            dic[item[2]] = item[3]

        else:
            print(f"11:檔案 {trans_output_filename} 不存在於當前目錄中。")

        # 指定要讀取的檔案名稱
        file_path = output_file_path

        result_filename = f"{temp[0]}_{lang}_result.txt"
        output_file_path = os.path.join(langPath, result_filename)
        # 確認檔案是否存在
        if os.path.exists(file_path):
            print(f"13:正在讀取檔案: {output_filename}")

            # 讀取檔案內容
            with open(file_path, "r", encoding="utf-8") as file:

                content = file.read()
                for keyword in dic:
                    # 正則表達式模式，匹配 'ID=82' 且捕獲中間的所有內容直到 'menustrip'
                    pattern = f"(ID=82.*?>)({keyword})(<)"

                    def replace_func(match):
                        return f"{match.group(1)}{dic[keyword]}{match.group(3)}"

                    # 替換 'Play' 為 'abc'
                    content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

                # print(content)
                with open(output_file_path, "w", encoding="UTF-8") as file1:
                    file1.write(content)
                print(f"14:已將內容保存至 {result_filename}，使用 UTF-8 編碼。")

        else:
            print(f"15:檔案 {output_filename} 不存在於當前目錄中。")

        index += 1

        print("=" * 30)

        os.remove(tempPath1)
        print(f"已將檔案 {output_filename} 刪除")

        os.remove(tempPath2)
        print(f"已將檔案 {trans_output_filename} 刪除")

        print("=" * 30)
