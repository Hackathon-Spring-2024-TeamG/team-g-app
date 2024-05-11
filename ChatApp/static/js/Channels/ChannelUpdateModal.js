let channelId; // グローバル変数としてchannelIdを宣言

$(document).ready(function() {
    // モーダル表示イベントを捕捉
    $('#update-confirmation-modal').on('show.bs.modal', function (event) {
        // イベントを引き起こした要素（編集ボタンかどうか）を判定
        let button = $(event.relatedTarget); // 編集ボタンからのイベントの場合、その要素を取得
        channelId = button.data('channel-id'); // グローバル変数channelIdに値を代入
        let channelName = button.data('channel-name');
        let channelDescription = button.data('channel-description');

        // もし編集ボタンからのイベントなら、そのデータでフォームを更新
        if (channelId !== undefined) {
            let modal = $(this);
            modal.find('.modal-body #updateChannelName').val(channelName);
            modal.find('.modal-body #updateChannelDescription').val(channelDescription);
        }
    });

    // 更新ボタンがクリックされたときのイベント
    document.getElementById('update-channel-confirmation-button').addEventListener('click', function(event) {
        event.preventDefault(); // フォームのデフォルトの送信を防ぐ

        // FormDataを使用してフォームデータを取得
        const formData = new FormData(document.getElementById('updateChannelForm'));

        // Fetch APIを使用して非同期通信
        fetch(`/update_channel/${channelId}`, { // グローバル変数channelIdを参照
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // モーダルを閉じる
                $('#update-confirmation-modal').modal('hide');
                // ページをリロード
                window.location.reload();
            } else {
                throw new Error('更新に失敗しました。');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});