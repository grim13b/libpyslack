# これはなに？
CloudWatchLogs の Filter に掛かった通知を Lambda 経由で Slack にメッセージをポストする function です。  

# 前提
1. KMS の設定が完了している必要があります。  
2. Lambda とその実行に関する IAM Role を設定する必要があります。  
3. libpyslack が Lambda Layer に登録されている必要があります。
4. あくまでもサンプルです。動作保証はありません。