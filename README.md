# saitamaict2024-api-server
## how to use
- 単語を合成する(op はplus or minus)
  
  実行例
  
```URL/merge_word/?str1=apple&str2=orange&op=plus```

```
{
  "status": 200,
  "str": [
    [
      "apples",
      0.803842008113861],
    [
      "pear",
      0.709553062915802],
    [
      "orchard",
      0.67687976360321],
    [
      "fruit",
      0.667434871196747],
    [
      "pippin",
      0.667427897453308],
    [
      "Apple",
      0.657411932945252],
    [
      "Apples",
      0.651072680950165],
    [
      "pears",
      0.650574862957001],
    [
      "peach",
      0.639158070087433],
    [
      "Honeycrisp",
      0.637626171112061]
  ]
}
```

- 単語に最も近い単語を取得(str1に最も近いものがえらばれる)

  実行例

```URL/merge_word/?str1=apple&op=similar```
```
{
  "status": 200,
  "str": [
    [
      "apples",
      0.803842008113861],
    [
      "pear",
      0.709553062915802],
    [
      "orchard",
      0.67687976360321],
    [
      "fruit",
      0.667434871196747],
    [
      "pippin",
      0.667427897453308],
    [
      "Apple",
      0.657411932945252],
    [
      "Apples",
      0.651072680950165],
    [
      "pears",
      0.650574862957001],
    [
      "peach",
      0.639158070087433],
    [
      "Honeycrisp",
      0.637626171112061]
  ]
}
```

- 問題を取得する

  実行例

```URL/get_problem/```

```{
  "status": 200,
  "start": [
    "Chalky",
    "WISEPC",
    "Muaz",
    "Llangyndeyrn",
    "Changma"
  ],
  "target": "unported"
}
```
