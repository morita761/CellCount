# Cell Count

## Calculate Transfection efficiency
培養細胞の面積とGFP蛍光の面積から導入効率を計算する
### 使用方法
```
cd CalcTrafecEff/
code config.txt                                 #パラメータを適宜修正
python cellsCount.py    [明視野の画像のパス]     # terminalに細胞の面積パーセントがでる
python gfpField.py      [GFPの画像のパス]       # terminalにGFPの面積パーセントがでる