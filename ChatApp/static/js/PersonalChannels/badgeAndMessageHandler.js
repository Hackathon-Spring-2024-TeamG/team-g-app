  document.addEventListener('DOMContentLoaded', function () {
    // バッジ選択時のイベントリスナー設定
    document.querySelectorAll('.badge-select-option').forEach(function(btn) {
      btn.addEventListener('click', function() {
        const selectedBadgeURL = this.getAttribute('data-badge');
        const selectedBadgeType = this.getAttribute('data-badge-type');
        addSelectedBadge(selectedBadgeURL, selectedBadgeType);

        // モーダルを閉じる
        const badgeModal = bootstrap.Modal.getInstance(document.getElementById('badge-selection-modal'));
        badgeModal.hide();
      });
    });

    // 個人メッセージ選択時のイベントリスナー設定
    document.querySelectorAll('.personal-message-option').forEach(function(btn) {
      btn.addEventListener('click', function() {
        const personalMessageId = this.getAttribute('data-message-id');
        window.selectedPersonalMessageId = personalMessageId; // 選択されたメッセージIDをグローバル変数に設定
        window.selectedBadgeDisplayArea = this.querySelector('.user-selected-badge'); // この行を追加
      });
    });
  });

  // 選択されたバッジを表示し、サーバーへの送信を行う関数
  function addSelectedBadge(badgeURL, badgeType) {
    // badgeDisplayAreaをグローバル変数から取得するように修正
    const badgeDisplayArea = window.selectedBadgeDisplayArea; 
    if (!badgeDisplayArea) {
      console.error('バッジを表示する場所が選択されていません。');
      return;
    }

    const badgeImg = document.createElement('img');
    badgeImg.src = badgeURL;
    badgeImg.alt = 'Selected Badge';
    badgeImg.style = 'width: 24px; height: 24px; margin: 0 4px;';
    badgeDisplayArea.appendChild(badgeImg);

    if(window.selectedPersonalMessageId) {
      fetch('/add_personal_badge', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          associableId: window.selectedPersonalMessageId,
          badgeType: badgeType,
        }),
      })
      .then(response => response.json())
      .then(data => console.log('Success:', data))
      .catch(error => console.error('Error:', error));
    } else {
      console.error('個人メッセージが選択されていません。');
    }
	}
