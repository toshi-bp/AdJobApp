from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponse

import sys
import csv
import numpy as np
import pandas as pd
import sklearn

def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #ファイルが保存された時
            sys.stderr.write("*** file_upload *** aaa ***\n")
            handle_uploaded_file(request.FILES['file'])
            file_obj = request.FILES['file']
            sys.stderr.write(file_obj.name + "\n")
            return HttpResponseRedirect('/success/')
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})
    #settings.pyのINSTALLED_APPに'file_upload'を書いておくこと

def handle_uploaded_file(file_obj):
    sys.stderr.write("*** handle_uploaded_file *** aaa ***\n")
    sys.stderr.write(file_obj.name + "\n")
    file_path = 'media/documents/' + file_obj.name
    sys.stderr.write(file_path + "\n")
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            sys.stderr.write("*** handle_uploaded_file *** ccc ***\n")
            destination.write(chunk)
            sys.stderr.write("*** handle_uploaded_file *** eee ***\n")
    # データの読み込み
    AdJob = pd.read_csv("media/documents/train_x.csv")
    AdJob_test = pd.read_csv(file_path)
    AppSum = pd.read_csv("media/documents/train_y.csv")
    
    # 変数の定義
    y_train = AppSum["応募数 合計"]
    AdJob["（紹介予定）休日休暇"] = AdJob["（紹介予定）休日休暇"].str.strip("年間休日")
    AdJob["（紹介予定）休日休暇"] = AdJob["（紹介予定）休日休暇"].astype(float)
    AdJob["給与/交通費　備考"] = AdJob["給与/交通費　備考"].str.lstrip("【月収例】")
    AdJob["給与/交通費　備考"] = AdJob["給与/交通費　備考"].str.rstrip("<BR>【交通費】◆時給１６５０円の時は日額５００円まで交通費有／時給１７００円の時は交通費無。どちらか選択できます。")
    AdJob["給与/交通費　備考"] = AdJob["給与/交通費　備考"].str.rstrip("交通費】◆条件により交通費支給あり。詳細はお気軽にお問合せください")
    AdJob["給与/交通費　備考"] = AdJob["給与/交通費　備考"].str.rstrip("円＋残業代（21日勤務の場合）")

    AdJob["給与/交通費　備考"] = AdJob['給与/交通費　備考'].str.replace("万", ' * 10000 + ')
    
    AdJob = AdJob.fillna({"（紹介予定）入社後の雇用形態": 3,
                    "（派遣先）配属先部署　平均年齢": AdJob["（派遣先）配属先部署　平均年齢"].mean(),
                    "給与/交通費　給与上限": AdJob["給与/交通費　給与上限"].min(),
                    "（紹介予定）休日休暇": AdJob["（紹介予定）休日休暇"].mean()})
    # NaNが含まれている列を削除
    X_train = AdJob.dropna(axis=1)
    # 数値以外のデータを含む列を削除
    X_train = X_train.select_dtypes(include=['number'])
    X_train = X_train.drop(["お仕事No."], axis=1)

    AdJob_test["（紹介予定）休日休暇"] = AdJob_test["（紹介予定）休日休暇"].str.strip("年間休日")
    AdJob_test["（紹介予定）休日休暇"] = AdJob_test["（紹介予定）休日休暇"].astype(float)
    AdJob_test["給与/交通費　備考"] = AdJob_test["給与/交通費　備考"].str.lstrip("【月収例】")
    AdJob_test["給与/交通費　備考"] = AdJob_test["給与/交通費　備考"].str.rstrip("円＋残業代（21日勤務の場合）")

    AdJob_test["給与/交通費　備考"] = AdJob_test["給与/交通費　備考"].str.replace("万", '*10000+')
    AdJob_test = AdJob_test.fillna({"（紹介予定）入社後の雇用形態": 3,
                    "（派遣先）配属先部署　平均年齢": AdJob_test["（派遣先）配属先部署　平均年齢"].mean(),
                    "給与/交通費　給与上限": AdJob_test["給与/交通費　給与上限"].min(),
                    "（紹介予定）休日休暇": AdJob_test["（紹介予定）休日休暇"].mean()})
    
    X_test = AdJob_test.dropna(axis=1)
    X_test = X_test.select_dtypes(include=['number'])
    X_test = X_test.drop(["お仕事No."], axis=1)

    #モデルを作成
    from sklearn.ensemble import RandomForestRegressor
    rfr = RandomForestRegressor(random_state=0)
    rfr.fit(X_train, y_train)

    y_pred = rfr.predict(X_test)
    print(y_pred)

    X = AdJob["お仕事No."]
    y_pred = pd.DataFrame(y_pred, columns=["応募数 合計"])

    #y_pred = y_pred[:3391]
    #RMSEで評価を行う
    from sklearn.metrics import mean_squared_error
    rmse = np.sqrt(mean_squared_error(y_pred, y_train[:3391])) 
    print(rmse)

    #MAEで評価を行う
    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(y_pred, y_train[:3391])

    # この値が1.253になるべく近くなるようにする
    print(rmse / mae)

    y_pred = pd.concat([X, y_pred], axis=1)
    #y_pred = y_pred[:3391]
    y_pred.to_csv("media/documents/y_pred.csv", index=False)



def success(request):
    return render(request, 'file_upload/success.html')
